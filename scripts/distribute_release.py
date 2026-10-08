"""CI-only registry reconciliation and immutable GitHub release uploads."""

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

from verify_release_artifacts import verify


def registry(manifest: dict, directory: Path) -> bool:
    url = f"https://pypi.org/pypi/{manifest['name']}/{manifest['version']}/json"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return False
        raise
    entries = {entry["filename"]: entry for entry in data["urls"]}
    if set(entries) != set(manifest["sha256"]):
        raise ValueError("registry file inventory mismatch")
    for filename, digest in manifest["sha256"].items():
        entry = entries[filename]
        if entry["digests"]["sha256"] != digest:
            raise ValueError("existing registry version has different bytes; never overwrite")
        with urllib.request.urlopen(entry["url"], timeout=30) as response:
            raw = response.read()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError("downloaded registry checksum mismatch")
        (directory / filename).write_bytes(raw)
    return True


def gh(*arguments: str) -> str:
    return subprocess.check_output(["gh", *arguments], text=True)


def release_upload(directory: Path, assets: Path, repository: str, tag: str) -> None:
    # API errors fail closed; only an explicit HTTP 404 permits creating a release.
    found = subprocess.run(
        ["gh", "api", f"repos/{repository}/releases/tags/{tag}"],
        capture_output=True,
        text=True,
    )
    if found.returncode:
        if "HTTP 404" not in found.stderr:
            raise RuntimeError(found.stderr)
        subprocess.run(
            [
                "gh",
                "release",
                "create",
                tag,
                "--repo",
                repository,
                "--verify-tag",
                "--title",
                tag,
                "--notes-file",
                "RELEASE_NOTES.md",
            ],
            check=True,
        )
        data = json.loads(gh("api", f"repos/{repository}/releases/tags/{tag}"))
    else:
        data = json.loads(found.stdout)
    existing = {entry["name"]: entry for entry in data["assets"]}
    files = [*sorted(directory.iterdir()), *sorted(assets.iterdir())]
    if set(existing) - {path.name for path in files}:
        raise ValueError("unexpected existing GitHub release asset inventory")
    for path in files:
        if path.name in existing:
            with tempfile.TemporaryDirectory() as temporary:
                subprocess.run(
                    [
                        "gh",
                        "release",
                        "download",
                        tag,
                        "--repo",
                        repository,
                        "--pattern",
                        path.name,
                        "--dir",
                        temporary,
                    ],
                    check=True,
                )
                if (Path(temporary) / path.name).read_bytes() != path.read_bytes():
                    raise ValueError(f"existing GitHub asset differs: {path.name}")
        else:
            subprocess.run(
                ["gh", "release", "upload", tag, str(path), "--repo", repository],
                check=True,
            )
    # Verify every uploaded byte, including checksums, after the write.
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.run(
            ["gh", "release", "download", tag, "--repo", repository, "--dir", temporary],
            check=True,
        )
        for path in files:
            if (Path(temporary) / path.name).read_bytes() != path.read_bytes():
                raise ValueError(f"uploaded GitHub asset differs: {path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["preflight", "registry", "github"])
    parser.add_argument("--directory", type=Path, default=Path("dist"))
    parser.add_argument("--manifest", type=Path, default=Path("release-assets/inventory.json"))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    verify(args.directory, args.manifest, manifest["name"], manifest["version"])
    if args.mode == "github":
        release_upload(
            args.directory,
            args.manifest.parent,
            os.environ["GITHUB_REPOSITORY"],
            os.environ["GITHUB_REF_NAME"],
        )
    else:
        found = registry(manifest, args.directory)
        if args.mode == "registry" and not found:
            raise ValueError("published registry version not visible")
        if args.mode == "preflight":
            with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as stream:
                stream.write(f"exists={str(found).lower()}\n")
    print("PASS: release distribution reconciliation")


if __name__ == "__main__":
    main()

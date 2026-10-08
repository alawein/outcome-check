"""CI-only registry reconciliation and immutable GitHub release uploads."""

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

from verify_release_artifacts import verify


def verify_published_file(manifest: dict, filename: str, path: Path) -> None:
    from verify_publish_provenance import verify_file

    verify_file(
        manifest,
        filename,
        path,
        os.environ["GITHUB_REPOSITORY"],
        os.environ["SOURCE_SHA"],
        os.environ["SOURCE_REF"],
    )


def registry(manifest: dict, directory: Path, *, require_complete: bool = False) -> set[str]:
    """Verify all existing files and return only the absent canonical filenames.

    Never change the retained canonical directory. A verified subset is resumable;
    extra files, different bytes, or a foreign/missing publisher fail closed.
    """
    expected = set(manifest["sha256"])
    url = f"https://pypi.org/pypi/{manifest['name']}/{manifest['version']}/json"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        data = {"urls": []}
    entries = {entry["filename"]: entry for entry in data["urls"]}
    if set(entries) - expected or len(entries) != len(data["urls"]):
        raise ValueError("registry file inventory mismatch")
    for filename, entry in entries.items():
        digest = manifest["sha256"][filename]
        if entry["digests"]["sha256"] != digest:
            raise ValueError("existing registry version has different bytes; never overwrite")
        with urllib.request.urlopen(entry["url"], timeout=30) as response:
            raw = response.read()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError("downloaded registry checksum mismatch")
        with tempfile.TemporaryDirectory(prefix="registry-verify-") as temporary:
            path = Path(temporary) / filename
            path.write_bytes(raw)
            verify_published_file(manifest, filename, path)
    missing = expected - set(entries)
    if require_complete and missing:
        raise ValueError("published registry inventory incomplete")
    return missing


def stage_missing(manifest: dict, directory: Path, staging: Path, missing: set[str]) -> None:
    """Copy only absent files into a fresh publisher-owned directory, never hard link."""
    if not missing <= set(manifest["sha256"]):
        raise ValueError("unexpected file requested for publishing")
    if staging.resolve().is_relative_to(directory.resolve()):
        raise ValueError("publisher staging cannot be inside the canonical directory")
    staging.mkdir()  # Existing staging (including publisher sidecars) fails closed.
    for filename in sorted(missing):
        raw = (directory / filename).read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest["sha256"][filename]:
            raise ValueError("canonical file changed before staging")
        (staging / filename).write_bytes(raw)


def release_body(manifest: dict, repository: str, sha: str, tag: str) -> str:
    """Called only after complete registry byte and publisher provenance verification."""
    lines = [
        f"# {manifest['name']} {manifest['version']}",
        "",
        f"Published on [PyPI](https://pypi.org/project/{manifest['name']}/{manifest['version']}/).",
        "Registry distribution bytes and publisher provenance were verified before this release.",
        f"Source: [{sha}](https://github.com/{repository}/commit/{sha}).",
        f"Tag: [{tag}](https://github.com/{repository}/tree/{tag}).",
        "",
        "## Verified distribution SHA-256",
        "",
    ]
    lines.extend(
        f"- `{filename}`: `{digest}`" for filename, digest in sorted(manifest["sha256"].items())
    )
    lines += [
        "",
        "Source changes and compatibility details: "
        f"[CHANGELOG.md](https://github.com/{repository}/blob/{sha}/CHANGELOG.md).",
        "",
    ]
    return "\n".join(lines)


def gh(*arguments: str) -> str:
    return subprocess.check_output(["gh", *arguments], text=True)


def release_upload(
    directory: Path, assets: Path, repository: str, tag: str, notes_file: Path
) -> None:
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
                str(notes_file),
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
    parser.add_argument("mode", choices=["preflight", "registry", "github", "build-provenance"])
    parser.add_argument("--directory", type=Path, default=Path("dist"))
    parser.add_argument("--manifest", type=Path, default=Path("release-assets/inventory.json"))
    parser.add_argument("--staging", type=Path, default=Path("publish-dist"))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]
    verify(args.directory, args.manifest, project["name"], project["version"])
    if args.mode == "github":
        registry(manifest, args.directory, require_complete=True)
        with tempfile.TemporaryDirectory(prefix="release-body-") as temporary:
            notes = Path(temporary) / "release.md"
            notes.write_text(
                release_body(
                    manifest,
                    os.environ["GITHUB_REPOSITORY"],
                    os.environ["SOURCE_SHA"],
                    os.environ["GITHUB_REF_NAME"],
                ),
                encoding="utf-8",
                newline="\n",
            )
            release_upload(
                args.directory,
                args.manifest.parent,
                os.environ["GITHUB_REPOSITORY"],
                os.environ["GITHUB_REF_NAME"],
                notes,
            )
    elif args.mode == "build-provenance":
        for filename in sorted(manifest["sha256"]):
            subprocess.run(
                [
                    "gh",
                    "attestation",
                    "verify",
                    str(args.directory / filename),
                    "--repo",
                    os.environ["GITHUB_REPOSITORY"],
                    "--signer-workflow",
                    os.environ["GITHUB_REPOSITORY"] + "/.github/workflows/release.yml",
                    "--source-digest",
                    os.environ["SOURCE_SHA"],
                    "--signer-digest",
                    os.environ["SOURCE_SHA"],
                    "--source-ref",
                    os.environ["SOURCE_REF"],
                    "--deny-self-hosted-runners",
                ],
                check=True,
            )
    else:
        missing = registry(manifest, args.directory, require_complete=args.mode == "registry")
        if args.mode == "preflight":
            stage_missing(manifest, args.directory, args.staging, missing)
            with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as stream:
                stream.write(f"exists={str(not missing).lower()}\n")
    print("PASS: release distribution reconciliation")


if __name__ == "__main__":
    main()

"""Verify a fixed wheel/sdist inventory before and after distribution."""

import argparse
import hashlib
import json
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path


def inventory(directory: Path, name: str, version: str) -> dict[str, str]:
    stem = name.replace("-", "_") + "-" + version
    expected = {stem + "-py3-none-any.whl", stem + ".tar.gz"}
    actual = {path.name for path in directory.iterdir()}
    if actual != expected:
        raise ValueError(f"distribution inventory mismatch: {sorted(actual)}")
    hashes = {}
    for filename in sorted(expected):
        path = directory / filename
        if path.suffix == ".whl":
            with zipfile.ZipFile(path) as archive:
                members = [n for n in archive.namelist() if n.endswith(".dist-info/METADATA")]
                if len(members) != 1:
                    raise ValueError("wheel metadata inventory mismatch")
                metadata = archive.read(members[0])
        else:
            with tarfile.open(path) as archive:
                stream = archive.extractfile(stem + "/PKG-INFO")
                if stream is None:
                    raise ValueError("missing sdist metadata")
                metadata = stream.read()
        fields = BytesParser().parsebytes(metadata)
        if fields["Name"] != name or fields["Version"] != version:
            raise ValueError("distribution metadata mismatch")
        hashes[filename] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def verify(directory: Path, manifest: Path, name: str, version: str) -> dict[str, str]:
    hashes = inventory(directory, name, version)
    expected = json.loads(manifest.read_text(encoding="utf-8"))
    if expected != {"name": name, "version": version, "sha256": hashes}:
        raise ValueError("distribution checksum mismatch")
    checksum_file = manifest.with_name("SHA256SUMS")
    checksum_bytes = "".join(
        f"{digest}  {filename}\n" for filename, digest in hashes.items()
    ).encode("ascii")
    if not checksum_file.is_file() or checksum_file.read_bytes() != checksum_bytes:
        raise ValueError("SHA256SUMS inventory mismatch")
    return hashes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--create", action="store_true")
    args = parser.parse_args()
    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]
    name, version = project["name"], project["version"]
    if args.create:
        hashes = inventory(args.directory, name, version)
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(
            json.dumps({"name": name, "version": version, "sha256": hashes}, indent=2) + "\n",
            encoding="utf-8",
        )
        args.manifest.with_name("SHA256SUMS").write_text(
            "".join(f"{digest}  {filename}\n" for filename, digest in hashes.items()),
            encoding="utf-8",
            newline="\n",
        )
    verify(args.directory, args.manifest, name, version)
    print("PASS: exact distribution inventory, metadata and SHA-256")


if __name__ == "__main__":
    main()

"""Verify PyPI signatures and exact GitHub publishing certificate claims."""

import base64
import json
import os
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from cryptography import x509
from cryptography.x509.oid import ObjectIdentifier


def extension_text(certificate: x509.Certificate, suffix: int) -> str:
    extension = certificate.extensions.get_extension_for_oid(
        ObjectIdentifier(f"1.3.6.1.4.1.57264.1.{suffix}")
    ).value
    if not isinstance(extension, x509.UnrecognizedExtension):
        raise ValueError("unexpected publishing certificate extension")
    raw = extension.value
    if raw[0] != 12:
        raise ValueError("certificate claim must be DER UTF8String")
    length, start = raw[1], 2
    if length & 128:
        width = length & 127
        length = int.from_bytes(raw[2 : 2 + width], "big")
        start += width
    if len(raw) != start + length:
        raise ValueError("invalid certificate claim length")
    return raw[start:].decode("utf-8")


def check_claims(certificate: x509.Certificate, repository: str, sha: str, ref: str) -> None:
    workflow = f"https://github.com/{repository}/.github/workflows/release.yml@{ref}"
    expected = {9: workflow, 10: sha, 11: "github-hosted", 13: sha, 14: ref}
    for suffix, value in expected.items():
        if extension_text(certificate, suffix) != value:
            raise ValueError(f"publishing certificate claim mismatch: {suffix}")
    names = certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
    if workflow not in names.get_values_for_type(x509.UniformResourceIdentifier):
        raise ValueError("publishing certificate workflow identity mismatch")


def main() -> None:
    manifest = json.loads(Path("release-assets/inventory.json").read_text(encoding="utf-8"))
    repository, sha, ref = (
        os.environ["GITHUB_REPOSITORY"],
        os.environ["SOURCE_SHA"],
        os.environ["SOURCE_REF"],
    )
    for filename in manifest["sha256"]:
        url = (
            f"https://pypi.org/integrity/{manifest['name']}/{manifest['version']}/"
            f"{filename}/provenance"
        )
        with urllib.request.urlopen(url, timeout=30) as response:
            raw = response.read()
        provenance = json.loads(raw)
        bundles = provenance.get("attestation_bundles", [])
        if not bundles:
            raise ValueError("no registry publish attestation")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "provenance.json"
            path.write_bytes(raw)
            subprocess.run(
                [
                    "pypi-attestations",
                    "verify",
                    "pypi",
                    "--repository",
                    f"https://github.com/{repository}",
                    "--provenance-file",
                    str(path),
                    str(Path("dist") / filename),
                ],
                check=True,
            )
        for bundle in bundles:
            if not bundle.get("attestations"):
                raise ValueError("empty registry attestation bundle")
            for attestation in bundle["attestations"]:
                der = base64.b64decode(attestation["verification_material"]["certificate"])
                check_claims(x509.load_der_x509_certificate(der), repository, sha, ref)
    print("PASS: PyPI signatures and exact workflow/source/tag/hosted-runner claims")


if __name__ == "__main__":
    main()

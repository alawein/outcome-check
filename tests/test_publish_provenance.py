import datetime
import importlib.util
from pathlib import Path

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID, ObjectIdentifier

spec = importlib.util.spec_from_file_location(
    "publish_verifier", Path(__file__).parents[1] / "scripts/verify_publish_provenance.py"
)
assert spec and spec.loader
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def certificate(change=None):
    sha, ref = "a" * 40, "refs/tags/v0.4.0"
    workflow = "https://github.com/owner/repo/.github/workflows/release.yml@" + ref
    claims = {9: workflow, 10: sha, 11: "github-hosted", 13: sha, 14: ref}
    if change in claims:
        claims[change] = "wrong"
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "synthetic test")])
    now = datetime.datetime.now(datetime.UTC)
    builder = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(1)
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(minutes=1))
    )
    for suffix, text in claims.items():
        raw = text.encode()
        builder = builder.add_extension(
            x509.UnrecognizedExtension(
                ObjectIdentifier(f"1.3.6.1.4.1.57264.1.{suffix}"), bytes([12, len(raw)]) + raw
            ),
            critical=False,
        )
    builder = builder.add_extension(
        x509.SubjectAlternativeName(
            [x509.UniformResourceIdentifier("https://wrong" if change == "identity" else workflow)]
        ),
        critical=False,
    )
    return builder.sign(key, hashes.SHA256())


def test_exact_registry_certificate_claims():
    # This tests claim binding only; synthetic certificates are not trusted signatures.
    verifier.check_claims(certificate(), "owner/repo", "a" * 40, "refs/tags/v0.4.0")


@pytest.mark.parametrize("claim", [9, 10, 11, 13, 14, "identity"])
def test_wrong_workflow_commit_runner_or_tag_fails(claim):
    with pytest.raises(ValueError, match="mismatch"):
        verifier.check_claims(certificate(claim), "owner/repo", "a" * 40, "refs/tags/v0.4.0")

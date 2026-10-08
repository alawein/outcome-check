import base64
from copy import deepcopy

import pytest
from test_checks_v2 import baseline_packet, v2

from outcome_check.contract import InputError
from outcome_check.core import check_packet
from outcome_check.signatures import (
    Ed25519Verifier,
    canonical_json,
    sign_observation,
    signature_status,
)


def test_canonical_vectors_and_utf16_key_order():
    assert (
        canonical_json({"b": [True, None], "a": "\n€"})
        == b'{"a":"\\n\xe2\x82\xac","b":[true,null]}'
    )
    assert canonical_json({"\ue000": 1, "\U0001f600": 2}) == '{"😀":2,"\ue000":1}'.encode()
    assert canonical_json({"n": 9007199254740991}) == b'{"n":9007199254740991}'


@pytest.mark.parametrize("value", [1.0, 9007199254740992, "\ud800", {"\udfff": 1}])
def test_canonical_unsupported_values_rejected(value):
    with pytest.raises(InputError):
        canonical_json(value)


def signed_packet():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    key = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
    public = key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    p = v2()
    p["observations"][0] = sign_observation(p["observations"][0], "fixture", bytes(range(32)))
    return p, Ed25519Verifier({"fixture": public})


def test_signatures_verified_tamper_and_missing():
    p, verifier = signed_packet()
    p["require_signatures"] = True
    report = check_packet(p, verifier)
    assert report["exit_code"] == 0
    assert report["results"][0]["signature"] == "verified"
    unsigned = deepcopy(p)
    unsigned["observations"][0].pop("signature")
    assert check_packet(unsigned, verifier)["exit_code"] == 1
    assert check_packet(p)["exit_code"] == 1
    p["observations"][0]["state"]["unused"] = "tampered"
    assert check_packet(p, verifier)["results"][0]["signature"] == "invalid"
    assert check_packet(p, verifier)["exit_code"] == 1


def test_unsigned_nonfailure_and_unverified_label():
    assert check_packet(v2())["results"][0]["signature"] == "unsigned"
    p, _ = signed_packet()
    assert check_packet(p)["results"][0]["signature"] == "unverified"
    assert check_packet(p)["exit_code"] == 0
    assert check_packet(p, Ed25519Verifier({}))["exit_code"] == 1


@pytest.mark.parametrize("value", ["", "not-base64!", base64.b64encode(b"x" * 63).decode()])
def test_invalid_signature_never_confirms(value):
    p, verifier = signed_packet()
    p["observations"][0]["signature"]["signature"] = value
    assert check_packet(p, verifier)["exit_code"] == 1


def test_required_baseline_signature():
    p = baseline_packet(before="08:00")
    p["require_signatures"] = True
    signed, verifier = signed_packet()
    p["observations"] = signed["observations"]
    assert check_packet(p, verifier)["exit_code"] == 1
    p["baselines"][0] = sign_observation(p["baselines"][0], "fixture", bytes(range(32)))
    assert check_packet(p, verifier)["exit_code"] == 0
    assert signature_status(p["baselines"][0], verifier) == "verified"


def test_verifier_runs_once_per_observation_and_report_agrees():
    p, real = signed_packet()

    class Once:
        calls = 0

        def verify(self, *args):
            self.calls += 1
            assert self.calls == 1
            return real.verify(*args)

    verifier = Once()
    p["require_signatures"] = True
    report = check_packet(p, verifier)
    assert report["exit_code"] == 0
    assert report["results"][0]["signature"] == "verified"

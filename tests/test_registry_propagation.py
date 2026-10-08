"""Only incomplete version metadata may retry; every delivered file needs proof."""

import io
import json
import urllib.error

import pytest
from test_distribution_retry import distribution
from test_release_artifacts import artifacts


def entries(manifest, names):
    return [
        {
            "filename": name,
            "digests": {"sha256": manifest["sha256"][name]},
            "url": "https://files.pythonhosted.org/" + name,
        }
        for name in names
    ]


def test_complete_registry_recovers_404_then_partial_then_complete(tmp_path, monkeypatch):
    directory, inventory = artifacts(tmp_path)
    manifest = json.loads(inventory.read_text())
    names = sorted(manifest["sha256"])
    metadata_calls, proofs, sleeps = [], [], []

    def request(url, **kwargs):
        if url.endswith("/json"):
            metadata_calls.append(url)
            if len(metadata_calls) == 1:
                raise urllib.error.HTTPError(url, 404, "not propagated", {}, None)
            selected = names[:1] if len(metadata_calls) == 2 else names
            return io.BytesIO(json.dumps({"urls": entries(manifest, selected)}).encode())
        return io.BytesIO((directory / url.rsplit("/", 1)[1]).read_bytes())

    def proof(data, filename, path):
        assert data == manifest
        assert path.read_bytes() == (directory / filename).read_bytes()
        proofs.append(filename)

    monkeypatch.setattr(distribution.urllib.request, "urlopen", request)
    monkeypatch.setattr(distribution, "verify_published_file", proof)
    assert distribution.complete_registry(manifest, directory, sleep=sleeps.append) == set()
    assert len(metadata_calls) == 3
    assert proofs == [names[0], *names]
    assert sleeps == [2, 5]


def test_complete_registry_exhaustion_is_bounded(tmp_path, monkeypatch):
    directory, inventory = artifacts(tmp_path)
    manifest = json.loads(inventory.read_text())
    calls, sleeps = [], []

    def request(url, **kwargs):
        calls.append(url)
        return io.BytesIO(b'{"urls": []}')

    def proof(*args):
        pytest.fail("missing artifacts have no proof and must never be accepted")

    monkeypatch.setattr(distribution.urllib.request, "urlopen", request)
    monkeypatch.setattr(distribution, "verify_published_file", proof)
    with pytest.raises(distribution.MissingPublishedArtifacts, match="incomplete"):
        distribution.complete_registry(manifest, directory, sleep=sleeps.append)
    assert len(calls) == 5
    assert sleeps == [2, 5, 10, 20]
    assert sum(sleeps) == 37 <= 60


@pytest.mark.parametrize(
    "failure",
    [
        "extra",
        "duplicate",
        "digest",
        "download",
        "download_404",
        "foreign_proof",
        "missing_proof",
        "metadata_403",
    ],
)
def test_unsafe_registry_failure_never_retries(tmp_path, monkeypatch, failure):
    directory, inventory = artifacts(tmp_path)
    manifest = json.loads(inventory.read_text())
    name = sorted(manifest["sha256"])[0]
    records = entries(manifest, [name])
    if failure == "extra":
        records[0]["filename"] = "foreign.whl"
    if failure == "duplicate":
        records.append(records[0].copy())
    if failure == "digest":
        records[0]["digests"]["sha256"] = "0" * 64
    calls, sleeps = [], []

    def request(url, **kwargs):
        if url.endswith("/json"):
            calls.append(url)
            if failure == "metadata_403":
                raise urllib.error.HTTPError(url, 403, "forbidden", {}, None)
            return io.BytesIO(json.dumps({"urls": records}).encode())
        if failure == "download_404":
            raise urllib.error.HTTPError(url, 404, "artifact unavailable", {}, None)
        return io.BytesIO(b"changed" if failure == "download" else (directory / name).read_bytes())

    def proof(*args):
        if failure == "foreign_proof":
            raise ValueError("foreign publisher")
        if failure == "missing_proof":
            raise urllib.error.HTTPError("provenance", 404, "no proof", {}, None)
        pytest.fail("unsafe files must fail before publisher proof is considered")

    monkeypatch.setattr(distribution.urllib.request, "urlopen", request)
    monkeypatch.setattr(distribution, "verify_published_file", proof)
    error = (
        urllib.error.HTTPError
        if failure in ("missing_proof", "metadata_403", "download_404")
        else ValueError
    )
    with pytest.raises(error):
        distribution.complete_registry(manifest, directory, sleep=sleeps.append)
    assert len(calls) == 1
    assert sleeps == []

import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import urllib.error
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
spec = importlib.util.spec_from_file_location(
    "distribution", Path(__file__).parents[1] / "scripts/distribute_release.py"
)
assert spec and spec.loader
distribution = importlib.util.module_from_spec(spec)
spec.loader.exec_module(distribution)


def test_registry_only_404_is_absent(tmp_path, monkeypatch):
    manifest = {"name": "example", "version": "1"}

    def fail(code):
        def request(*args, **kwargs):
            raise urllib.error.HTTPError("url", code, "failure", {}, None)

        return request

    monkeypatch.setattr(distribution.urllib.request, "urlopen", fail(404))
    assert distribution.registry(manifest, tmp_path) is False
    monkeypatch.setattr(distribution.urllib.request, "urlopen", fail(403))
    with pytest.raises(urllib.error.HTTPError):
        distribution.registry(manifest, tmp_path)


@pytest.mark.parametrize("change", [None, "inventory", "digest", "download"])
def test_registry_existing_version_requires_exact_downloaded_bytes(tmp_path, monkeypatch, change):
    raw = b"canonical"
    digest = hashlib.sha256(raw).hexdigest()
    manifest = {"name": "example", "version": "1", "sha256": {"file.whl": digest}}
    entry = {
        "filename": "extra.whl" if change == "inventory" else "file.whl",
        "digests": {"sha256": "0" * 64 if change == "digest" else digest},
        "url": "https://files.pythonhosted.org/file.whl",
    }

    def request(url, **kwargs):
        if url.endswith("/json"):
            return io.BytesIO(json.dumps({"urls": [entry]}).encode())
        return io.BytesIO(b"corrupted" if change == "download" else raw)

    monkeypatch.setattr(distribution.urllib.request, "urlopen", request)
    if change:
        with pytest.raises(ValueError):
            distribution.registry(manifest, tmp_path)
    else:
        assert distribution.registry(manifest, tmp_path)
        assert (tmp_path / "file.whl").read_bytes() == raw


def test_github_existing_conflicting_asset_is_never_replaced(tmp_path, monkeypatch):
    directory, assets = tmp_path / "dist", tmp_path / "assets"
    directory.mkdir()
    assets.mkdir()
    (directory / "file.whl").write_bytes(b"canonical")
    uploads = []

    def run(arguments, **kwargs):
        if arguments[1] == "api":
            return subprocess.CompletedProcess(
                arguments, 0, json.dumps({"assets": [{"name": "file.whl"}]}), ""
            )
        if arguments[2] == "download":
            Path(arguments[-1], "file.whl").write_bytes(b"old different bytes")
        if arguments[2] == "upload":
            uploads.append(arguments)
        return subprocess.CompletedProcess(arguments, 0)

    monkeypatch.setattr(distribution.subprocess, "run", run)
    with pytest.raises(ValueError, match="existing GitHub asset differs"):
        distribution.release_upload(directory, assets, "owner/repo", "v1")
    assert uploads == []

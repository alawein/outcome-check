"""Publisher integration regression: its real sidecar layout must stay out of dist."""

import json
import re
from pathlib import Path

import pytest
from test_distribution_retry import distribution
from test_release_artifacts import artifacts, verifier


def test_workflow_routes_sidecar_producing_publisher_away_from_canonical_dist(tmp_path):
    workflow = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    publisher = workflow.split("uses: pypa/gh-action-pypi-publish@", 1)[1]
    publisher = publisher.split("\n      - ", 1)[0]
    match = re.search(r"^\s+packages-dir:\s*([^\s]+)\s*$", publisher, re.MULTILINE)
    assert match is not None, "publisher must receive an explicit writable staging directory"
    assert match[1].strip("/\"'") != "dist"
    assert "skip-existing: true" not in publisher and "skip_existing: true" not in publisher

    directory, manifest = artifacts(tmp_path)
    original = {path.name: path.read_bytes() for path in directory.iterdir()}
    staging = tmp_path / match[1].strip("/\"'")
    metadata = json.loads(manifest.read_text())
    distribution.stage_missing(metadata, directory, staging, set(original))
    # Pinned attestations.py compose_attestation_mapping/attest_dist use this exact path.
    for path in list(staging.iterdir()):
        path.with_suffix(f"{path.suffix}.publish.attestation").write_text("{}")
    metadata = json.loads(manifest.read_text())
    verifier.verify(directory, manifest, metadata["name"], metadata["version"])
    assert {path.name: path.read_bytes() for path in directory.iterdir()} == original
    assert len(list(staging.glob("*.publish.attestation"))) == 2
    # Strict canonical inventory must still reject sidecars if routed incorrectly.
    (directory / (next(iter(original)) + ".publish.attestation")).write_text("{}")
    with pytest.raises(ValueError, match="inventory mismatch"):
        verifier.verify(directory, manifest, metadata["name"], metadata["version"])

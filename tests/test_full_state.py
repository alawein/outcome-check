import importlib.util
from copy import deepcopy
from pathlib import Path

import pytest


def protocol():
    spec = importlib.util.spec_from_file_location(
        "full_state", Path("studies/tau-full-state/run.py")
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trial():
    return {
        "task_id": "synthetic",
        "trial_id": "0",
        "reported_success": True,
        "baseline": {"observed_at": "2026-10-04T11:58:00Z", "state": {"target": 1, "other": 0}},
        "final": {"observed_at": "2026-10-04T11:59:00Z", "state": {"target": 1, "other": 0}},
        "goal": {"state": {"target": 1, "other": 0}, "mutation_paths": []},
    }


@pytest.mark.parametrize(
    "change,expected",
    [
        ("unchanged", "confirmed"),
        ("required_unchanged", "unconfirmed"),
        ("changed", "confirmed"),
        ("unrelated", "unconfirmed"),
        ("no_baseline", "unobserved"),
        ("same_time", "unobserved"),
        ("future_baseline", "unobserved"),
        ("contradiction", "contradicted"),
        ("no_final", "unobserved"),
        ("no_goal", "unobserved"),
    ],
)
def test_full_state_protocol(change, expected):
    record = trial()
    if change == "required_unchanged":
        record["goal"]["mutation_paths"] = [["target"]]
    elif change == "changed":
        record["goal"]["mutation_paths"] = [["target"]]
        record["baseline"]["state"]["target"] = 0
    elif change == "unrelated":
        record["goal"]["mutation_paths"] = [["target"]]
        record["baseline"]["state"]["other"] = 2
    elif change == "no_baseline":
        record.pop("baseline")
    elif change == "same_time":
        record["baseline"]["observed_at"] = record["final"]["observed_at"]
    elif change == "future_baseline":
        record["baseline"]["observed_at"] = "2026-10-04T12:00:00Z"
    elif change == "contradiction":
        record["final"]["state"]["target"] = 2
    elif change == "no_final":
        record.pop("final")
    elif change == "no_goal":
        record.pop("goal")
    before = deepcopy(record)
    result = protocol().evaluate(record)
    assert result["status"] == expected
    assert record == before


def test_coverage_and_upstream_cross_tab():
    first, second = trial(), trial()
    second.update(task_id="missing", reported_success=False)
    second.pop("baseline")
    result = protocol().summarize([first, second])
    assert result["coverage"] == {"baseline": 1, "final": 2, "goal": 2, "complete": 1}
    assert result["by_reported_success"]["true"]["confirmed"] == 1
    assert result["by_reported_success"]["false"]["unobserved"] == 1

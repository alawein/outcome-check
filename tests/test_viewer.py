import json

import pytest
from test_outcomes import packet as make_packet

from outcome_check.cli import main
from outcome_check.contract import InputError, validate
from outcome_check.core import check_packet
from outcome_check.report import render_html


def test_help_mentions_example_exit_codes_and_docs(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "examples/packet.json" in out
    assert "exit" in out.lower()
    assert "contract" in out.lower()


def test_contract_errors_include_row_index():
    bad = make_packet()
    bad["requirements"][0]["max_age_seconds"] = -1
    with pytest.raises(InputError) as excinfo:
        validate(bad)
    assert "1" in str(excinfo.value)

    dup = make_packet()
    dup["observations"].append(dict(dup["observations"][0]))
    with pytest.raises(InputError) as excinfo:
        validate(dup)
    assert "2" in str(excinfo.value) or "row" in str(excinfo.value).lower()


def test_age_equal_to_max_is_confirmed():
    p = make_packet()
    # observed 60 s before as_of; max exactly 60 keeps it fresh.
    p["requirements"][0]["max_age_seconds"] = 60
    result = check_packet(p)
    assert result["results"][0]["outcome"] == "confirmed"
    assert result["results"][0]["status"] == "confirmed"


def test_fractional_as_of_age():
    p = make_packet()
    p["as_of"] = "2026-10-04T12:00:00.5Z"
    p["requirements"][0]["max_age_seconds"] = 61
    result = check_packet(p)
    assert result["results"][0]["outcome"] == "confirmed"
    p["requirements"][0]["max_age_seconds"] = 60
    result = check_packet(p)
    assert result["results"][0]["reason"] == "stale observation"


def test_cli_missing_input_returns_two(capsys, tmp_path):
    missing = tmp_path / "does-not-exist.json"
    assert main([str(missing)]) == 2
    assert "outcome-check" in capsys.readouterr().err


def test_cli_missing_output_dir_returns_two(tmp_path):
    source = tmp_path / "in.json"
    source.write_text(json.dumps(make_packet()), encoding="utf-8")
    target = tmp_path / "no-such-dir" / "out.json"
    assert main([str(source), "--json", str(target)]) == 2
    assert not target.exists()


def test_html_viewer_has_table_how_to_read_and_evidence():
    p = make_packet()
    report = check_packet(p)
    page = render_html(report, p)
    assert "<table" in page
    assert "How to read" in page
    assert "action receipt" in page.lower()
    assert "confirmed" in page.lower()
    # Evidence echo: expected path/value and observed value plus age vs max.
    assert "time" in page
    assert "07:00" in page
    assert "max" in page.lower()
    assert "<script>" not in page


def test_html_escapes_malicious_evidence():
    p = make_packet()
    p["requirements"][0]["id"] = "<script>alert(1)</script>"
    p["requirements"][0]["expected"] = "<b>bold</b>"
    report = check_packet(p)
    page = render_html(report, p)
    assert "<script>" not in page
    assert "&lt;script&gt;" in page
    assert "&lt;b&gt;" in page


def test_html_truncates_large_state_with_marker():
    p = make_packet()
    big = "X" * 5000
    p["observations"][0]["state"] = {"time": big}
    p["requirements"][0]["expected"] = big
    report = check_packet(p)
    page = render_html(report, p)
    assert "truncat" in page.lower()
    assert big not in page

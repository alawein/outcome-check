import json

from outcome_check.convert import main


def test_converter_atomic_output_and_input_identity(tmp_path):
    source = tmp_path / "result.json"
    source.write_text('{"instance_id":"x","resolved":true}')
    argv = [
        "swebench",
        str(source),
        "--as-of",
        "2026-10-13T12:00:00Z",
        "--observed-at",
        "2026-10-13T12:00:00Z",
        "--max-age-seconds",
        "0",
    ]
    assert main([*argv, "--output", str(source), "--force"]) == 2
    assert json.loads(source.read_text())["resolved"] is True
    target = tmp_path / "packet.json"
    assert main([*argv, "--output", str(target)]) == 0
    assert main([*argv, "--output", str(target)]) == 2


def test_converter_duplicate_keys_fail(tmp_path):
    source = tmp_path / "result.json"
    source.write_text('{"instance_id":"x","resolved":true,"resolved":false}')
    assert (
        main(
            [
                "swebench",
                str(source),
                "--as-of",
                "2026-10-13T12:00:00Z",
                "--observed-at",
                "2026-10-13T12:00:00Z",
                "--max-age-seconds",
                "0",
            ]
        )
        == 2
    )

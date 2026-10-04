import argparse
import sys
from pathlib import Path

from outcome_check.contract import InputError, load_packet, require
from outcome_check.core import check_packet
from outcome_check.report import render_html, render_json


def same_location(left: Path, right: Path) -> bool:
    if left.resolve() == right.resolve():
        return True
    return left.exists() and right.exists() and left.samefile(right)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check supplied agent outcome receipts.",
        epilog=(
            "packet shape: schema_version 1 with as_of, requirements, actions, "
            "observations; see docs/contract.md. "
            "example: outcome-check examples/packet.json --html report.html. "
            "exit 0 all confirmed; exit 1 needs review; exit 2 invalid input or I/O."
        ),
    )
    parser.add_argument("packet", type=Path, help="input packet JSON file")
    parser.add_argument("--json", type=Path, help="write the JSON report to PATH")
    parser.add_argument("--html", type=Path, help="write the HTML report to PATH")
    parser.add_argument("--force", action="store_true", help="overwrite existing output files")
    args = parser.parse_args(argv)
    try:
        packet, digest = load_packet(args.packet)
        report = check_packet(packet) | {"input_sha256": digest}
        targets = [(args.json, render_json(report)), (args.html, render_html(report, packet))]
        outputs = [path for path, content in targets if path is not None]
        inputs = [args.packet]
        for index, path in enumerate(outputs):
            require(
                not any(same_location(path, prior) for prior in outputs[:index]),
                "output paths must differ",
            )
            require(
                not any(same_location(path, source) for source in inputs),
                "output cannot replace input",
            )
        for path, _content in targets:
            if path is not None:
                require(args.force or not path.exists(), f"output exists: {path}")
                require(path.parent.is_dir(), f"missing output directory: {path.parent}")
        for path, content in targets:
            if path is not None:
                with path.open(
                    "w" if args.force else "x", encoding="utf-8", newline="\n"
                ) as stream:
                    stream.write(content)
        if args.json is None:
            sys.stdout.write(render_json(report))
        return report["exit_code"]
    except (InputError, OSError, OverflowError, RecursionError) as exc:
        print(f"outcome-check: {exc}", file=sys.stderr)
        return 2

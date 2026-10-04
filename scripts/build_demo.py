from pathlib import Path

from outcome_check.contract import load_packet
from outcome_check.core import check_packet
from outcome_check.report import render_html, render_json


def main() -> None:
    packet, digest = load_packet(Path("examples/packet.json"))
    report = check_packet(packet) | {
        "input_sha256": digest,
        "provenance": "Synthetic, AI-assisted, non-client",
    }
    target = Path("site")
    target.mkdir(exist_ok=True)
    (target / "index.html").write_text(render_html(report), encoding="utf-8")
    (target / "report.json").write_text(render_json(report), encoding="utf-8")


if __name__ == "__main__":
    main()

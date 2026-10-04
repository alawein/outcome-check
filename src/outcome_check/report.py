import html
import json


def render_json(report: dict) -> str:
    return json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n"


def render_html(report: dict) -> str:
    content = html.escape(render_json(report))
    cards = "".join(
        f'<div class="card"><strong>{html.escape(str(v))}</strong>'
        f"<span>{html.escape(k.replace('_', ' '))}</span></div>"
        for k, v in report.get("counts", {}).items()
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>Outcome check | outcome report</title><style>"
        "body{margin:0;background:#f4f6f5;color:#142c2a;font:17px/1.6 system-ui}"
        "main{max-width:980px;margin:auto;padding:36px 20px}h1{font-size:2.8rem}"
        ".cards{display:flex;flex-wrap:wrap;gap:12px}.card{background:white;"
        "border:1px solid #baccc6;border-radius:12px;padding:16px;flex:1 1 110px}"
        ".card strong{display:block;font-size:2rem}.card span{display:block}"
        "pre{background:#fff;padding:20px;border:1px solid #baccc6;"
        "white-space:pre-wrap;overflow-wrap:anywhere}a{color:#075851}"
        "</style></head><body><main><p>LOCAL EVIDENCE / REFERENCED OBSERVATIONS</p>"
        "<h1>Outcome check</h1><p>Checks supplied evidence, not authenticated execution.</p>"
        '<div class="cards">'
        + cards
        + "</div><h2>Inspectable report</h2><pre>"
        + content
        + "</pre>"
        "<p>Hashes bind bytes, not authenticity. This is a static executed example.</p>"
        '<p><a href="https://github.com/alawein/outcome-check">Source and installation</a>'
        "</p></main></body></html>"
    )

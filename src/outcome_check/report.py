import html
import json
from fractions import Fraction


def render_json(report: dict) -> str:
    return json.dumps(report, sort_keys=True, indent=2, allow_nan=False) + "\n"


def _truncate_text(value: str, limit: int = 400) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + f"… [truncated {len(value) - limit} chars]"


def _short_json(value: object, limit: int = 400) -> str:
    try:
        raw = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        raw = str(value)
    return _truncate_text(raw, limit)


def _walk(state: object, path: list) -> tuple[bool, object]:
    value = state
    for key in path:
        if type(value) is not dict or key not in value:
            return False, None
        value = value[key]
    return True, value


def _evidence_cells(result: dict, packet: dict | None) -> tuple[str, str, str]:
    """Return (expected, observed, freshness) display strings, unescaped."""
    if not isinstance(packet, dict):
        return "—", "—", "—"
    requirements = (
        packet.get("requirements") if isinstance(packet.get("requirements"), list) else []
    )
    observations = (
        packet.get("observations") if isinstance(packet.get("observations"), list) else []
    )
    req = next(
        (r for r in requirements if isinstance(r, dict) and r.get("id") == result.get("id")),
        None,
    )
    if req is None:
        return "—", "—", "—"
    path = req.get("path") if isinstance(req.get("path"), list) else []
    dotted = ".".join(str(k) for k in path)
    expected = _short_json(req.get("expected"))
    expected_cell = f"{dotted} = {expected}" if dotted else expected
    obs = next(
        (
            o
            for o in observations
            if isinstance(o, dict) and o.get("id") == req.get("observation_id")
        ),
        None,
    )
    if obs is None:
        return expected_cell, "missing observation", "no observation; needs a fresh receipt"
    state = obs.get("state")
    found, value = _walk(state, path if isinstance(path, list) else [])
    observed = _short_json(value) if found else "missing object path"
    observed_cell = f"{observed} (observation {obs.get('id')})"
    max_age = req.get("max_age_seconds")
    try:
        from outcome_check.contract import age_seconds

        age: Fraction = age_seconds(str(packet.get("as_of")), str(obs.get("observed_at")))
        freshness = f"age {age} s / max {max_age} s (observed at {obs.get('observed_at')})"
    except Exception:
        freshness = f"max {max_age} s (observed at {obs.get('observed_at')})"
    return expected_cell, observed_cell, freshness


def render_html(report: dict, packet: dict | None = None) -> str:
    content = html.escape(render_json(report))
    cards = "".join(
        f'<div class="card"><strong>{html.escape(str(v))}</strong>'
        f"<span>{html.escape(k.replace('_', ' '))}</span></div>"
        for k, v in report.get("counts", {}).items()
    )
    results = report.get("results") if isinstance(report.get("results"), list) else []
    if results:
        head = (
            "<thead><tr>"
            '<th scope="col">Requirement</th>'
            '<th scope="col">Action receipt</th>'
            '<th scope="col">Outcome</th>'
            '<th scope="col">Status</th>'
            '<th scope="col">Reason</th>'
            '<th scope="col">Expected</th>'
            '<th scope="col">Observed</th>'
            '<th scope="col">Freshness</th>'
            "</tr></thead>"
        )
        rows = ""
        for item in results:
            if not isinstance(item, dict):
                continue
            expected, observed, freshness = _evidence_cells(item, packet)
            rows += (
                "<tr>"
                f"<td>{html.escape(str(item.get('id', '')))}</td>"
                f"<td>{html.escape(str(item.get('action', '')))}</td>"
                f"<td>{html.escape(str(item.get('outcome', '')))}</td>"
                f"<td>{html.escape(str(item.get('status', '')))}</td>"
                f"<td>{html.escape(str(item.get('reason', '')))}</td>"
                f"<td>{html.escape(expected)}</td>"
                f"<td>{html.escape(observed)}</td>"
                f"<td>{html.escape(freshness)}</td>"
                "</tr>"
            )
        table = (
            "<h2>Results by requirement</h2>"
            '<div style="overflow-x:auto">'
            f"<table>{head}<tbody>{rows}</tbody></table>"
            "</div>"
        )
    else:
        table = ""
    how_to = (
        "<h2>How to read this report</h2>"
        "<ul>"
        "<li>Action receipt keeps what the agent reported: confirmed means the named "
        "action succeeded, contradicted means it failed, unobserved means it is unknown "
        "or missing, and not_required means no action was needed.</li>"
        "<li>Outcome keeps what the supplied observation shows: confirmed means the "
        "expected value was observed fresh, contradicted means a different value was "
        "observed, and unobserved means the evidence is missing, stale, future, "
        "wrong-subject, or off-path.</li>"
        "<li>Status merges the two: contradicted if either side contradicts, confirmed "
        "only when the outcome confirms and the action confirms or is not required, "
        "otherwise unobserved.</li>"
        "<li>Expected echoes the requirement path and value; Observed echoes the value "
        "at that path in the named observation; Freshness echoes observed age versus "
        "max_age_seconds. Large values are truncated with an explicit marker.</li>"
        "</ul>"
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
        "table{border-collapse:collapse;width:100%;background:#fff}"
        "th,td{border:1px solid #baccc6;padding:10px;text-align:left;"
        "vertical-align:top;overflow-wrap:anywhere}"
        "th{background:#e7f1ec}"
        "pre{background:#fff;padding:20px;border:1px solid #baccc6;"
        "white-space:pre-wrap;overflow-wrap:anywhere}a{color:#075851}"
        "</style></head><body><main><p>LOCAL EVIDENCE / REFERENCED OBSERVATIONS</p>"
        "<h1>Outcome check</h1><p>Checks supplied evidence, not authenticated execution.</p>"
        '<div class="cards">'
        + cards
        + "</div>"
        + table
        + how_to
        + "<h2>Inspectable report</h2><pre>"
        + content
        + "</pre>"
        "<p>Hashes bind bytes, not authenticity. This is a static executed example.</p>"
        '<p><a href="https://github.com/alawein/outcome-check">Source and installation</a>'
        "</p></main></body></html>"
    )

import html
import json

from outcome_check.contract import InputError, age_seconds


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


def _index(rows: object, key: str = "id") -> dict:
    if not isinstance(rows, list):
        return {}
    return {row.get(key): row for row in rows if isinstance(row, dict) and key in row}


def _evidence_cells(
    result: dict,
    requirements: dict,
    observations: dict,
    as_of: object,
) -> tuple[str, str, str]:
    """Return (expected, observed, freshness) display strings, unescaped."""
    req = requirements.get(result.get("id"))
    if req is None:
        return "—", "—", "—"
    path = req.get("path") if isinstance(req.get("path"), list) else []
    dotted = ".".join(str(k) for k in path)
    expected = _short_json(req.get("expected"))
    if req.get("check", "equal") != "equal":
        expected = f"{req['check']} {expected}"
    expected_cell = _truncate_text(f"{dotted} = {expected}") if dotted else expected
    if req.get("baseline_id") is not None:
        expected_cell += f"; baseline {req['baseline_id']}"
    if req.get("requires_change"):
        expected_cell += "; change required"
    obs = observations.get(req.get("observation_id"))
    if obs is None:
        return expected_cell, "missing observation", "no observation; needs a fresh receipt"
    state = obs.get("state")
    found, value = _walk(state, path)
    observed = _short_json(value) if found else "missing object path"
    observed_cell = f"{observed} (observation {obs.get('id')})"
    max_age = req.get("max_age_seconds")
    try:
        age = age_seconds(str(as_of), str(obs.get("observed_at")))
        shown = f"{float(age):g}"
        freshness = f"age {shown} s / max {max_age} s (observed at {obs.get('observed_at')})"
    except (InputError, ValueError):
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
    packet_map = packet if isinstance(packet, dict) else {}
    requirements = _index(packet_map.get("requirements"))
    observations = _index(packet_map.get("observations"))
    as_of = packet_map.get("as_of")
    if results:
        signed = report.get("schema_version") in (2, 3)
        signature_header = '<th scope="col">Signature</th>' if signed else ""
        head = (
            "<thead><tr>"
            '<th scope="col">Requirement</th>'
            '<th scope="col">Action receipt</th>'
            '<th scope="col">Outcome</th>' + signature_header + '<th scope="col">Status</th>'
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
            expected, observed, freshness = _evidence_cells(item, requirements, observations, as_of)
            status_value = str(item.get("status", ""))
            chip = (
                status_value
                if status_value in ("confirmed", "contradicted", "unobserved", "unconfirmed")
                else ""
            )
            signature_cell = (
                f"<td>{html.escape(str(item.get('signature', 'unsigned')))}</td>" if signed else ""
            )
            rows += (
                "<tr>"
                f"<td>{html.escape(str(item.get('id', '')))}</td>"
                f"<td>{html.escape(str(item.get('action', '')))}</td>"
                f"<td>{html.escape(str(item.get('outcome', '')))}</td>"
                + signature_cell
                + f'<td class="st st-{chip}">'
                f"{html.escape(status_value)}</td>"
                f"<td>{html.escape(str(item.get('reason', '')))}</td>"
                f"<td>{html.escape(expected)}</td>"
                f"<td>{html.escape(observed)}</td>"
                f"<td>{html.escape(freshness)}</td>"
                "</tr>"
            )
        table = (
            "<h2>Results by requirement</h2>"
            '<div style="overflow-x:auto">'
            "<table><caption>Per-requirement action receipt, outcome, status and "
            "evidence echo</caption>"
            f"{head}<tbody>{rows}</tbody></table>"
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
        "requested check was satisfied by fresh evidence, unconfirmed means a required "
        "change was not observed, contradicted means a different value was "
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
    if report.get("schema_version") in (2, 3):
        how_to = how_to.replace(
            "otherwise unobserved.</li>",
            "unconfirmed if the outcome needs an observed change, otherwise unobserved.</li>",
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="description" content="Supplied-evidence outcome checks: action '
        'receipt, observed outcome and merged status per requirement.">'
        '<meta name="theme-color" content="#f4f6f5">'
        "<title>Outcome check | outcome report</title><style>"
        ":root{color-scheme:light}"
        "body{margin:0;background:#f4f6f5;color:#142c2a;font:17px/1.6 system-ui;"
        "-webkit-tap-highlight-color:transparent}"
        "main{max-width:980px;margin:auto;padding:36px 20px}"
        "h1{font-size:2.8rem;text-wrap:balance}h2,h3{text-wrap:balance}"
        ".eyebrow{letter-spacing:.12em;font-size:.85rem}"
        ".cards{display:flex;flex-wrap:wrap;gap:12px}.card{background:white;"
        "border:1px solid #baccc6;border-radius:12px;padding:16px;flex:1 1 110px}"
        ".card strong{display:block;font-size:2rem;font-variant-numeric:tabular-nums}"
        ".card span{display:block}"
        "table{border-collapse:collapse;width:100%;background:#fff}"
        "caption{caption-side:top;text-align:left;font-weight:650;padding:8px 0}"
        "th,td{border:1px solid #baccc6;padding:10px;text-align:left;"
        "vertical-align:top;overflow-wrap:anywhere}"
        "th{background:#e7f1ec}"
        "tbody tr:nth-child(even){background:#f4f8f6}"
        ".st{font-weight:650}"
        ".st-confirmed{background:#e7f1ec}"
        ".st-contradicted{background:#f9e7e7}"
        ".st-unobserved{background:#f6f0dd}"
        "pre{background:#fff;padding:20px;border:1px solid #baccc6;"
        "white-space:pre-wrap;overflow-wrap:anywhere}"
        "a{color:#075851}a:hover{text-decoration:underline}"
        ":focus-visible{outline:3px solid #075851;outline-offset:3px}"
        '</style></head><body><main><p class="eyebrow">LOCAL EVIDENCE / '
        "REFERENCED OBSERVATIONS</p>"
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

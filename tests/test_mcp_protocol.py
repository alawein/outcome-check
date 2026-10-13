import io
import json

from outcome_check.mcp import serve


def reply(value):
    out = io.StringIO()
    serve(io.StringIO(value + "\n"), out)
    return json.loads(out.getvalue())


def test_mcp_error_codes():
    assert reply("{")["error"]["code"] == -32700
    assert reply('{"jsonrpc":"2.0","id":1,"method":"unknown"}')["error"]["code"] == -32601
    assert reply('{"jsonrpc":"1.0","id":1,"method":"ping"}')["error"]["code"] == -32600
    assert (
        reply('{"jsonrpc":"2.0","id":1,"method":"tools/list","params":[]}')["error"]["code"]
        == -32602
    )


def test_mcp_supported_version_negotiation():
    response = reply(
        '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2099-01-01"}}'
    )
    assert response["result"]["protocolVersion"] == "2025-06-18"

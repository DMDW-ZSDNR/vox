"""ComfyUI execution errors should be compact and actionable (issue #615).

The raw ``status.messages`` payload embeds the full traceback, current
inputs, and outputs. Surface node, exception type, and the first line of
the exception message; keep ``prompt_id`` for resume. Truncate anything
that still runs long.
"""

import json

import pytest

from tools._comfyui.client import ComfyUIClient, ComfyUIError, _compact_execution_error


EXECUTION_ERROR = {
    "type": "execution_error",
    "data": {
        "prompt_id": "p-1",
        "node_id": "9",
        "node_type": "KSampler",
        "exception_type": "ValueError",
        "exception_message": "expected float tensor\nstack line 2\nstack line 3",
        "traceback": ["line 1", "line 2"],
        "current_inputs": {"seed": 42},
        "current_outputs": {},
    },
}


def test_history_messages_are_compacted():
    # ComfyUI stores history messages as (event, data) pairs, serialized as
    # JSON arrays — not as {"type", "data"} objects.
    summary = _compact_execution_error(
        [["execution_start", {}], ["execution_error", EXECUTION_ERROR["data"]]]
    )

    assert summary == "KSampler: ValueError: expected float tensor"
    assert "traceback" not in summary
    assert "current_inputs" not in summary


def test_websocket_payload_is_compacted():
    summary = _compact_execution_error(EXECUTION_ERROR["data"])

    assert summary == "KSampler: ValueError: expected float tensor"


def test_dict_style_message_list_is_tolerated():
    summary = _compact_execution_error(
        [{"type": "execution_start", "data": {}}, EXECUTION_ERROR]
    )

    assert summary == "KSampler: ValueError: expected float tensor"


def test_unknown_payload_falls_back_to_json():
    summary = _compact_execution_error({"unexpected": True})

    assert json.loads(summary) == {"unexpected": True}


def test_long_summary_is_truncated():
    payload = dict(EXECUTION_ERROR["data"])
    payload["exception_message"] = "x" * 5000

    summary = _compact_execution_error(payload)

    assert len(summary) == 1500
    assert summary.endswith("...")


def test_history_entry_raises_compact_error_and_keeps_prompt_id(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "p-1": {
                    "status": {
                        "status_str": "error",
                        "messages": [
                            ["execution_start", {}],
                            ["execution_error", EXECUTION_ERROR["data"]],
                        ],
                    }
                }
            }

    monkeypatch.setattr(
        "tools._comfyui.client.requests.get", lambda *a, **k: FakeResponse()
    )

    with pytest.raises(ComfyUIError) as excinfo:
        ComfyUIClient("http://127.0.0.1:18188")._history_entry("p-1")

    assert str(excinfo.value) == "Execution error: KSampler: ValueError: expected float tensor"
    assert excinfo.value.prompt_id == "p-1"

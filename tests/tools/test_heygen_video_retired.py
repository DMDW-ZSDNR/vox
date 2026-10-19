"""heygen_video ran on HeyGen's v1 Workflows API, removed on 2026-10-31 with no
v3 replacement: it must never be selected, even with HEYGEN_API_KEY set."""

from tools.base_tool import ToolStatus
from tools.video.heygen_video import HeyGenVideo


def test_heygen_video_is_unavailable_even_with_key(monkeypatch):
    monkeypatch.setenv("HEYGEN_API_KEY", "test-key")
    tool = HeyGenVideo()

    assert tool.get_status() == ToolStatus.UNAVAILABLE
    result = tool.execute({"prompt": "p"})
    assert not result.success
    assert "2026-10-31" in result.error

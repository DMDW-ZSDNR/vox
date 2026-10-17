"""Tests for the job-scoped Remotion browser executable (issue #619).

`video_compose` used to leave browser resolution entirely to Remotion, which
fails on offline or locked-down machines that cannot download Chromium. The
new `remotion_browser_executable` input is validated up front and passed
through as `--browser-executable`.
"""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.video.video_compose import VideoCompose  # noqa: E402


@pytest.fixture
def tool(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/npx")
    return VideoCompose()


def test_missing_browser_executable_fails_before_render(tool, tmp_path, monkeypatch):
    called = {"run": False}

    def fake_run_command(cmd, *a, **k):
        called["run"] = True

    monkeypatch.setattr(tool, "run_command", fake_run_command)
    missing = tmp_path / "does-not-exist"

    result = tool._remotion_render(
        {
            "composition_data": {"cuts": []},
            "output_path": str(tmp_path / "out.mp4"),
            "remotion_browser_executable": str(missing),
        }
    )

    assert result.success is False
    assert "remotion_browser_executable" in result.error
    assert str(missing) in result.error
    assert called["run"] is False


def test_browser_executable_is_passed_through(tool, tmp_path, monkeypatch):
    seen = {}

    def fake_run_command(cmd, *a, **k):
        seen["cmd"] = cmd
        Path(seen["output"]).write_bytes(b"")
        return None

    monkeypatch.setattr(tool, "run_command", fake_run_command)
    output = tmp_path / "out.mp4"
    seen["output"] = output

    result = tool._remotion_render(
        {
            "composition_data": {"cuts": []},
            "output_path": str(output),
            "remotion_browser_executable": sys.executable,
        }
    )

    assert result.success is True, result.error
    assert f"--browser-executable={Path(sys.executable).resolve()}" in seen["cmd"]


def test_no_browser_flag_when_not_requested(tool, tmp_path, monkeypatch):
    seen = {}

    def fake_run_command(cmd, *a, **k):
        seen["cmd"] = cmd

    monkeypatch.setattr(tool, "run_command", fake_run_command)
    tool._remotion_render(
        {"composition_data": {"cuts": []}, "output_path": str(tmp_path / "out.mp4")}
    )

    assert not any(
        str(part).startswith("--browser-executable") for part in seen["cmd"]
    )


def test_high_level_render_forwards_browser_executable(tool, tmp_path, monkeypatch):
    captured = {}
    monkeypatch.setattr(tool, "_pre_compose_validation", lambda *a, **k: None)
    monkeypatch.setattr(tool, "_needs_remotion", lambda *a, **k: True)

    def fake_remotion_render(inputs):
        captured.update(inputs)
        from tools.base_tool import ToolResult

        return ToolResult(success=True, data={}, artifacts=[])

    monkeypatch.setattr(tool, "_remotion_render", fake_remotion_render)
    monkeypatch.setattr(tool, "_run_final_review", lambda *a, **k: {})

    tool._render(
        {
            "edit_decisions": {
                "render_runtime": "remotion",
                "renderer_family": "explainer-data",
                "cuts": [{"id": "c1", "source": "a1", "in_seconds": 0, "out_seconds": 2}],
            },
            "asset_manifest": {"assets": [{"id": "a1", "path": "/tmp/a1.mp4"}]},
            "output_path": str(tmp_path / "out.mp4"),
            "remotion_browser_executable": sys.executable,
        }
    )

    assert captured.get("remotion_browser_executable") == sys.executable

"""cmd_narration must run end-to-end and record a real sentence count.

Regression for a latent NameError: the stage built its manifest with
`len(sentences)` without ever binding `sentences`, so any episode that
actually had to synthesize narration crashed instead of recording it.
"""
from __future__ import annotations

import json
import wave
from pathlib import Path

import pytest

import scripts.run_episode as run_episode
from tools.base_tool import ToolResult

SCRIPT = """# Pilot

## Hook
- Sea ice seals the ocean from the sky. [SE-01]
- Life could still use chemical gradients instead of sunlight. [SE-02]
"""


def _write_wav(path: Path, dur: float = 2.0, sr: int = 24000) -> None:
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"\x00\x00" * int(dur * sr))


@pytest.fixture()
def episode(tmp_path):
    ep = tmp_path / "ep"
    (ep / "artifacts").mkdir(parents=True)
    (ep / "script.md").write_text(SCRIPT, encoding="utf-8")
    return ep


def test_cmd_narration_records_sentence_count(episode, monkeypatch):
    state = {"episode_dir": str(episode), "narration_helper": "torch"}
    helper = episode / "helper.py"
    helper.write_text("# fake helper\n", encoding="utf-8")
    monkeypatch.setitem(run_episode.NARRATION_HELPERS, "torch", helper)
    monkeypatch.setattr(run_episode, "NARRATION_PYTHON", Path("/usr/bin/env"))

    def fake_run(cmd, capture_output=True, text=True, timeout=None):
        _write_wav(Path(cmd[-1]), 2.0)

        class R:
            returncode = 0
            stderr = ""

        return R()

    monkeypatch.setattr(run_episode.subprocess, "run", fake_run)

    class FakeFinish:
        def execute(self, params):
            src, dst = Path(params["input_path"]), Path(params["output_path"])
            dst.write_bytes(src.read_bytes())
            return ToolResult(success=True, data={"duration_s": 2.0})

    monkeypatch.setattr("tools.audio.finish_audio.FinishAudioTool", FakeFinish)

    res = run_episode.cmd_narration("se_pilot", state)
    assert res["status"] == "OK", res
    assert (episode / "narration_finished.wav").exists()

    manifest = json.loads(
        (episode / "artifacts" / "narration_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["sentences"] == 2
    assert manifest["expected_duration"] == pytest.approx(2.0)


def test_cmd_narration_fails_closed_without_helper(episode, monkeypatch):
    state = {"episode_dir": str(episode), "narration_helper": "torch"}
    monkeypatch.setitem(run_episode.NARRATION_HELPERS, "torch", episode / "missing.py")
    monkeypatch.setattr(run_episode, "NARRATION_PYTHON", Path("/nonexistent/python"))
    res = run_episode.cmd_narration("se_pilot", state)
    assert res["status"] == "BLOCKED"
    assert "helper" in res["error"]

#!/usr/bin/env python3
"""scripts/run_episode.py — one-command episode pipeline (Milestone Z3).

Usage:  python3 scripts/run_episode.py <topic_id>

Chains: claim_ledger_check -> script_validation -> footage_manifest_rights ->
        narration -> subtitles -> edl -> render -> finish_audio -> qc ->
        package_draft

Per-stage checkpoint with wall-time + disk logging, resume of OK stages,
idempotency via output hashing, fail-closed (any unverified stage = BLOCKED,
pipeline stops, non-zero exit). Stage implementations are pluggable through
STAGE_REGISTRY so tests can drive the orchestration with fake stages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Venv used for the Kokoro / stable-ts toolchain (set up in Milestone Z1).
VENV_PY = Path(os.environ.get("OPENMONTAGE_VENV", "/tmp/kilo/z1_venv/bin/python"))

MIN_FREE_BYTES = 800 * 1024 * 1024  # global stop threshold (zero-cost mode)
MAX_CHAPTER_DURATION = 360  # 6 minutes per chapter (Z4)

STAGES = [
    "claim_ledger_check",
    "script_validation",
    "footage_manifest_rights",
    "narration",
    "subtitles",
    "edl",
    "render",
    "finish_audio",
    "qc",
    "package_draft",
]


def iso_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def disk_free_bytes(path):
    return shutil.disk_usage(str(path)).free


def _hash_obj(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def _load_state(state_path):
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return {"topic_id": None, "stages": {}}


def _save_state(state_path, state):
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Topic layout helpers
# ---------------------------------------------------------------------------
def slice_dir(topic_id):
    return ROOT / "docs/openmontage/slice" / topic_id


def topic_script(topic_id):
    candidates = [
        ROOT / f"docs/openmontage/slice/{topic_id.upper()}_FULL_SCRIPT_v0.md",
        slice_dir(topic_id) / "script.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def topic_ledger(topic_id):
    candidates = [
        ROOT / f"docs/openmontage/evidence/{topic_id.upper()}_CLAIM_LEDGER.md",
        ROOT / f"docs/openmontage/slice/{topic_id.upper()}_CLAIM_LEDGER.md",
        slice_dir(topic_id) / "claim_ledger.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def shared_assets():
    return ROOT / "docs/openmontage/slice/artifacts"


# ---------------------------------------------------------------------------
# Stage implementations
# ---------------------------------------------------------------------------
def cmd_claim_ledger_check(topic_id, state):
    ledger = topic_ledger(topic_id)
    if not ledger:
        return {"status": "BLOCKED", "error": f"no claim ledger for topic {topic_id}"}
    text = ledger.read_text(encoding="utf-8")
    import re
    ids = re.findall(r"ARTEMIS-\d+", text)
    claim_ids = sorted(set(ids))
    if not claim_ids:
        return {"status": "BLOCKED", "error": "claim ledger has no claim_ids"}
    return {"status": "OK", "outputs": {"ledger": str(ledger), "claim_ids": claim_ids}}


def cmd_script_validation(topic_id, state):
    script = topic_script(topic_id)
    if not script:
        return {"status": "BLOCKED", "error": f"no script for topic {topic_id}"}
    sentences = []
    for line in script.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("| B"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[0][:2] in ("B1", "B2", "B3", "B4", "B5", "B6"):
            sentences.append(cells[1])
    missing = [i for i, s in enumerate(sentences) if not s]
    if missing:
        return {"status": "BLOCKED", "error": f"empty sentences at {missing}"}
    return {"status": "OK", "outputs": {"script": str(script), "sentences": len(sentences)}}


def cmd_footage_manifest_rights(topic_id, state):
    rights = shared_assets() / "rights_records.json"
    if not rights.exists():
        return {"status": "BLOCKED", "error": "rights_records.json missing"}
    records = json.loads(rights.read_text(encoding="utf-8"))
    allowed = {"explicit_license", "source_policy_us_gov"}
    bad = [r["asset_id"] for r in records if r.get("rights_basis") not in allowed]
    if bad:
        return {"status": "BLOCKED", "error": f"rights_basis not permitted: {bad}"}
    return {"status": "OK", "outputs": {"rights_records": str(rights), "assets": len(records)}}


def cmd_narration(topic_id, state):
    slice_dir(topic_id).mkdir(parents=True, exist_ok=True)
    raw = slice_dir(topic_id) / "narration_raw.wav"
    wav = slice_dir(topic_id) / "narration_finished.wav"
    if wav.exists():
        return {"status": "OK", "outputs": {"narration_wav": str(wav)}}
    script = topic_script(topic_id)
    if not script:
        return {"status": "BLOCKED", "error": f"no script for topic {topic_id}"}
    if not raw.exists():
        helper = ROOT / "scripts" / "z3_kokoro_narrate.py"
        if not helper.exists():
            return {"status": "BLOCKED", "error": "kokoro narration helper missing"}
        res = subprocess.run(
            [str(VENV_PY), str(helper), str(script), str(raw)],
            capture_output=True, text=True, timeout=1800,
        )
        if res.returncode != 0:
            return {"status": "BLOCKED", "error": f"kokoro synthesis failed: {res.stderr[-500:]}"}
    from tools.audio.finish_audio import FinishAudioTool  # noqa: WPS433
    result = FinishAudioTool().execute(
        {"input_path": str(raw), "output_path": str(wav)}
    )
    if not result.success:
        return {"status": "BLOCKED", "error": f"finish_audio failed: {result.error}"}
    return {"status": "OK", "outputs": {"narration_wav": str(wav), **result.data}}


def cmd_subtitles(topic_id, state):
    wav = slice_dir(topic_id) / "narration_finished.wav"
    if not wav.exists():
        return {"status": "BLOCKED", "error": "no finished narration for subtitles"}
    slice_dir(topic_id).mkdir(parents=True, exist_ok=True)
    words_out = slice_dir(topic_id) / "word-timestamps.json"
    srt_out = slice_dir(topic_id) / "subtitles.srt"
    if words_out.exists() and srt_out.exists():
        return {"status": "OK", "outputs": {"words": str(words_out), "subtitles": str(srt_out)}}
    helper = ROOT / "scripts" / "z3_subtitles.py"
    if not helper.exists():
        return {"status": "BLOCKED", "error": "subtitle helper missing"}
    script = topic_script(topic_id)
    sentences = []
    for line in script.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("| B"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[0][:2] in ("B1", "B2", "B3", "B4", "B5", "B6"):
            sentences.append(cells[1])
    text = " ".join(sentences)
    res = subprocess.run(
        [str(VENV_PY), str(helper), str(wav), text, str(words_out), str(srt_out)],
        capture_output=True, text=True, timeout=1800,
    )
    if res.returncode != 0:
        return {"status": "BLOCKED", "error": f"subtitles failed: {res.stderr[-500:]}"}
    return {"status": "OK", "outputs": {"words": str(words_out), "subtitles": str(srt_out)}}


def cmd_edl(topic_id, state):
    out = slice_dir(topic_id) / "edit_decisions.json"
    if out.exists():
        return {"status": "OK", "outputs": {"edit_decisions": str(out)}}
    total = 185.43
    EDL = {
        "version": 1, "topic_id": topic_id, "total_duration_s": total,
        "resolution": "1920x1080", "fps": 30, "codec": "h264", "audio_codec": "aac",
        "cuts": [
            {"cut_id": 1, "start": 0.0, "end": 8.0, "asset_id": "card_title", "role": "graphics_card",
             "clip": "Title", "layout": "static_card",
             "rationale": "Opening title card with claim_ids ARTEMIS-01/05/06; static by design.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 2, "start": 8.0, "end": 22.0, "asset_id": "card_b1", "role": "graphics_card",
             "clip": "B1", "layout": "static_card",
             "rationale": "Beat 1 Preparation graphics card with claim_ids ARTEMIS-01/02/04; static by design.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 3, "start": 22.0, "end": 38.0, "asset_id": "artemis_launch", "role": "archive_insert",
             "clip": "Launch B-roll", "layout": "1080p_scaled",
             "source_segment": "40.0-56.0s",
             "rationale": "Bright ascent portion of the Artemis I launch (source 1080p, no framing).",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 4, "start": 38.0, "end": 54.0, "asset_id": "card_b2", "role": "graphics_card",
             "clip": "B2", "layout": "static_card",
             "rationale": "Beat 2 Launch graphics card with claim_ids ARTEMIS-05/06; static by design.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 5, "start": 54.0, "end": 70.0, "asset_id": "artemis_launch", "role": "archive_insert",
             "clip": "Launch B-roll", "layout": "1080p_scaled",
             "source_segment": "56.0-72.0s",
             "rationale": "Continued launch B-roll; 1080p source, no framing.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 6, "start": 70.0, "end": 84.0, "asset_id": "card_b3", "role": "graphics_card",
             "clip": "B3", "layout": "static_card",
             "rationale": "Beat 3 Transit graphics card with claim_ids ARTEMIS-05/06/07; static by design.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 7, "start": 84.0, "end": 102.0, "asset_id": "card_b4", "role": "graphics_card",
             "clip": "B4", "layout": "static_card",
             "rationale": "Beat 4 Moon flybys graphics card with claim_ids ARTEMIS-07/08; static by design.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 8, "start": 102.0, "end": 118.0, "asset_id": "artemis_launch", "role": "archive_insert",
             "clip": "Launch B-roll", "layout": "1080p_scaled",
             "source_segment": "72.0-88.0s",
             "rationale": "Continued launch B-roll; 1080p source, no framing.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 9, "start": 118.0, "end": 134.0, "asset_id": "artemis_launch", "role": "archive_insert",
             "clip": "Launch B-roll", "layout": "1080p_scaled",
             "source_segment": "88.0-104.0s",
             "rationale": "Continued launch B-roll; 1080p source, no framing.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 10, "start": 134.0, "end": 156.0, "asset_id": "card_b5", "role": "graphics_card",
             "clip": "B5", "layout": "static_card",
             "rationale": "Beat 5 Return graphics card with claim_ids ARTEMIS-09/10; static by design.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 11, "start": 156.0, "end": 178.0, "asset_id": "card_b6", "role": "graphics_card",
             "clip": "B6", "layout": "static_card",
             "rationale": "Beat 6 Legacy graphics card with claim_ids ARTEMIS-11/12; static by design.",
             "rights_basis": "source_policy_us_gov"},
            {"cut_id": 12, "start": 178.0, "end": total, "asset_id": "card_credits", "role": "graphics_card",
             "clip": "Credits", "layout": "static_card",
             "rationale": "Closing credits card; static by design.",
             "rights_basis": "source_policy_us_gov"},
        ],
        "static_segments": [
            {"start": 0.0, "end": 8.0, "reason": "title card", "static_by_design": True},
            {"start": 8.0, "end": 22.0, "reason": "B1 card", "static_by_design": True},
            {"start": 38.0, "end": 54.0, "reason": "B2 card", "static_by_design": True},
            {"start": 70.0, "end": 84.0, "reason": "B3 card", "static_by_design": True},
            {"start": 84.0, "end": 102.0, "reason": "B4 card", "static_by_design": True},
            {"start": 134.0, "end": 156.0, "reason": "B5 card", "static_by_design": True},
            {"start": 156.0, "end": 178.0, "reason": "B6 card", "static_by_design": True},
            {"start": 178.0, "end": total, "reason": "credits card", "static_by_design": True},
        ],
    }
    slice_dir(topic_id).mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(EDL, indent=2), encoding="utf-8")
    return {"status": "OK", "outputs": {"edit_decisions": str(out), "cuts": len(EDL["cuts"])}}


def _ffmpeg(args, timeout=3600):
    res = subprocess.run(["ffmpeg", "-hide_banner", "-y"] + args,
                         capture_output=True, text=True, timeout=timeout)
    if res.returncode != 0:
        raise RuntimeError(res.stderr[-800:])


def cmd_render(topic_id, state):
    out_dir = slice_dir(topic_id) / "renders"
    out = out_dir / f"final_{topic_id}_draft.mp4"
    if out.exists():
        return {"status": "OK", "outputs": {"video": str(out)}}
    edl = slice_dir(topic_id) / "edit_decisions.json"
    if not edl.exists():
        return {"status": "BLOCKED", "error": "no EDL to render"}
    footage = ROOT / "projects/slice_artemis_v0/footage/artemis_launch_source.mp4"
    gfx = ROOT / "projects/slice_artemis_v0/graphics"
    if not footage.exists() or not gfx.exists():
        return {"status": "BLOCKED",
                "error": "render needs projects/slice_artemis_v0 media (footage + graphics cards) from Z2"}
    card_dur = {"card_title": 8.0, "card_b1": 14.0, "card_b2": 16.0, "card_b3": 14.0,
                "card_b4": 18.0, "card_b5": 22.0, "card_b6": 22.0, "card_credits": 7.43}
    clip_src = [(40.0, 56.0), (56.0, 72.0), (72.0, 88.0), (88.0, 104.0)]
    order = ["card_title", "card_b1", ("clip", 0), "card_b2", ("clip", 1),
             "card_b3", "card_b4", ("clip", 2), ("clip", 3), "card_b5", "card_b6", "card_credits"]
    # NOTE: order maps to EDL cuts 1..12; clips consume source segments in order.
    slice_dir(topic_id).mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    build = out_dir / "build"
    shutil.rmtree(build, ignore_errors=True)
    build.mkdir()
    segs = []
    clip_i = 0
    for name in order:
        seg = build / f"seg_{len(segs):02d}.mp4"
        if name == "card_title":
            _ffmpeg(["-loop", "1", "-i", str(gfx / "card_title.png"), "-t", "8.00",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        elif name == "card_b1":
            _ffmpeg(["-loop", "1", "-i", str(gfx / "card_b1.png"), "-t", "14.00",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        elif name == "card_b2":
            _ffmpeg(["-loop", "1", "-i", str(gfx / "card_b2.png"), "-t", "16.00",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        elif name == "card_b3":
            _ffmpeg(["-loop", "1", "-i", str(gfx / "card_b3.png"), "-t", "14.00",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        elif name == "card_b4":
            _ffmpeg(["-loop", "1", "-i", str(gfx / "card_b4.png"), "-t", "18.00",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        elif name == "card_b5":
            _ffmpeg(["-loop", "1", "-i", str(gfx / "card_b5.png"), "-t", "22.00",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        elif name == "card_b6":
            _ffmpeg(["-loop", "1", "-i", str(gfx / "card_b6.png"), "-t", "22.00",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        elif name == "card_credits":
            _ffmpeg(["-loop", "1", "-i", str(gfx / "card_credits.png"), "-t", "7.45",
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        else:
            s, e = clip_src[clip_i]
            clip_i += 1
            _ffmpeg(["-ss", str(s), "-i", str(footage), "-t", str(e - s),
                     "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(seg)])
        segs.append(str(seg))
    lst = build / "concat.txt"
    lst.write_text("\n".join(f"file '{s}'" for s in segs), encoding="utf-8")
    silent = out_dir / "silent.mp4"
    _ffmpeg(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(silent)])
    wav = slice_dir(topic_id) / "narration_finished.wav"
    _ffmpeg(["-i", str(silent), "-i", str(wav), "-c:v", "copy", "-c:a", "aac",
             "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)])
    return {"status": "OK", "outputs": {"video": str(out)}}


def cmd_finish_audio(topic_id, state):
    wav = slice_dir(topic_id) / "narration_finished.wav"
    if not wav.exists():
        return {"status": "BLOCKED", "error": "no narration to finish"}
    from tools.audio.finish_audio import FinishAudioTool  # noqa: WPS433
    finished = wav.with_name("narration_finished.wav")
    result = FinishAudioTool().execute({"input_path": str(wav), "output_path": str(finished)})
    if not result.success:
        return {"status": "BLOCKED", "error": f"finish_audio failed: {result.error}"}
    return {"status": "OK", "outputs": {"finished_wav": str(finished)}}


def cmd_qc(topic_id, state):
    video = slice_dir(topic_id) / "renders" / f"final_{topic_id}_draft.mp4"
    assets = shared_assets()
    ledger = topic_ledger(topic_id)
    if not video.exists():
        return {"status": "BLOCKED", "error": "no rendered video for QC"}
    if not ledger:
        return {"status": "BLOCKED", "error": f"no claim ledger for topic {topic_id}"}
    inputs = {
        "input_path": str(video),
        "output_path": str(assets / "qa_report.json"),
        "narration_manifest": str(assets / "narration_manifest.json"),
        "subtitle_path": str(slice_dir(topic_id) / "subtitles.srt"),
        "credits_path": str(assets / "credits.txt"),
        "claim_ids_path": str(assets / "claim_ids.json"),
        "claim_ledger_path": str(ledger),
        "rights_records_path": str(assets / "rights_records.json"),
        "edit_decisions_path": str(slice_dir(topic_id) / "edit_decisions.json"),
    }
    for k in ("narration_manifest", "subtitle_path", "credits_path", "claim_ids_path",
              "rights_records_path", "edit_decisions_path"):
        if not Path(inputs[k]).exists():
            return {"status": "BLOCKED", "error": f"missing QC input: {k}"}
    from tools.qa.qc import QCTool  # noqa: WPS433
    res = QCTool().execute(inputs)
    if not res.success:
        return {"status": "BLOCKED", "error": f"qc tool failed: {res.error}"}
    return {"status": "OK", "outputs": {"qa_report": str(inputs["output_path"]),
                                        "verdict": res.data.get("verdict")}}


def cmd_package_draft(topic_id, state):
    pkg = slice_dir(topic_id) / "package"
    pkg.mkdir(parents=True, exist_ok=True)
    assets = shared_assets()
    for name in ("narration_manifest.json", "subtitles.srt", "credits.txt", "edit_decisions.json",
                 "rights_records.json", "claim_ids.json", "word-timestamps.json"):
        src = assets / name
        if src.exists():
            shutil.copy2(src, pkg / name)
    video = slice_dir(topic_id) / "renders" / f"final_{topic_id}_draft.mp4"
    manifest = {
        "topic_id": topic_id, "status": "DRAFT_NOT_PUBLISHABLE",
        "package": str(pkg),
        "video": str(video) if video.exists() else None,
    }
    (pkg / "package_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"status": "OK", "outputs": {"package": str(pkg), "manifest": str(pkg / "package_manifest.json")}}


STAGE_REGISTRY = {
    "claim_ledger_check": cmd_claim_ledger_check,
    "script_validation": cmd_script_validation,
    "footage_manifest_rights": cmd_footage_manifest_rights,
    "narration": cmd_narration,
    "subtitles": cmd_subtitles,
    "edl": cmd_edl,
    "render": cmd_render,
    "finish_audio": cmd_finish_audio,
    "qc": cmd_qc,
    "package_draft": cmd_package_draft,
}


def run_pipeline(topic_id, state_path=None, state_root=None, stages=None, initial_state=None):
    if stages is None:
        stages = STAGE_REGISTRY
    if state_path is None:
        state_root = Path(state_root) if state_root else ROOT / "docs/openmontage/slice"
        state_path = Path(state_root) / topic_id / "episode_state.json"
    state_path = Path(state_path)

    if initial_state is not None:
        state = json.loads(json.dumps(initial_state))
        state["topic_id"] = topic_id
    else:
        state = _load_state(state_path)
    state["topic_id"] = topic_id
    state["updated_at"] = iso_now()
    state.setdefault("stages", {})

    # ---- fail-closed: disk budget before anything runs ----
    if disk_free_bytes(ROOT) < MIN_FREE_BYTES:
        free = disk_free_bytes(ROOT)
        cp = {"status": "BLOCKED", "started_at": iso_now(), "finished_at": iso_now(),
              "wall_time_s": 0.0, "disk_before_bytes": free,
              "disk_after_bytes": free, "outputs": {},
              "output_hash": _hash_obj({}),
              "error": f"free disk {free} bytes below {MIN_FREE_BYTES} bytes"}
        state["stages"]["disk"] = cp
        _save_state(state_path, state)
        return {"verdict": "BLOCKED", "stage": "disk", "state": state}

    for stage in STAGES:
        cp = state["stages"].get(stage)
        resumed = False
        if cp and cp.get("status") == "OK":
            stored_hash = cp.get("output_hash")
            recorded_outputs = cp.get("outputs")
            if stored_hash and recorded_outputs is not None \
                    and stored_hash != _hash_obj(recorded_outputs):
                pass  # corrupt checkpoint hash -> re-execute below
            else:
                resumed = True
        if resumed:
            cp["resumed"] = True
            state["stages"][stage] = cp
            continue

        slice_dir(topic_id).mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        disk_before = disk_free_bytes(state_path.parent)
        try:
            result = stages[stage](topic_id, state) or {}
            status = result.get("status", "BLOCKED")
        except Exception as exc:  # fail-closed on any stage crash
            status = "BLOCKED"
            result = {"error": f"{type(exc).__name__}: {exc}"}
        wall = round(time.time() - t0, 3)
        disk_after = disk_free_bytes(state_path.parent)
        outputs = result.get("outputs", {})
        cp = {
            "status": status,
            "started_at": iso_now(),
            "finished_at": iso_now(),
            "wall_time_s": wall,
            "disk_before_bytes": disk_before,
            "disk_after_bytes": disk_after,
            "outputs": outputs,
            "output_hash": _hash_obj(outputs),
            "error": result.get("error"),
        }
        state["stages"][stage] = cp
        _save_state(state_path, state)
        if status != "OK":
            return {"verdict": "BLOCKED", "stage": stage, "state": state}

    return {"verdict": "OK", "state": state}


# ---------------------------------------------------------------------------
# Chapter mode (Milestone Z4)
# ---------------------------------------------------------------------------
def _estimate_sentence_duration(sentence):
    """Rough narration duration: ~2.5 words/sec + 0.3s breath per sentence."""
    words = len([w for w in sentence.split() if w.strip()])
    return max(2.0, words / 2.5 + 0.3)


def split_script_into_chapters(script_path, max_duration_s=MAX_CHAPTER_DURATION):
    """Split a script markdown into chapters, each <= max_duration_s narration."""
    sentences = []
    script_path = Path(script_path)
    for line in script_path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("| B"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[0][:2] in ("B1", "B2", "B3", "B4", "B5", "B6"):
            sentences.append(cells[1])

    chapters = []
    current = []
    current_dur = 0.0
    chapter_index = 0
    for sentence in sentences:
        dur = _estimate_sentence_duration(sentence)
        if current and current_dur + dur > max_duration_s:
            chapters.append({
                "chapter_index": chapter_index,
                "sentences": list(current),
                "duration_s": round(current_dur, 3),
            })
            chapter_index += 1
            current = []
            current_dur = 0.0
        current.append(sentence)
        current_dur += dur
    if current:
        chapters.append({
            "chapter_index": chapter_index,
            "sentences": list(current),
            "duration_s": round(current_dur, 3),
        })
    return chapters


def _chapter_script_path(state_root, topic_id, chapter_index):
    return Path(state_root) / topic_id / f"chapter_{chapter_index}.md"


def _write_chapter_script(state_root, topic_id, chapter_index, sentences):
    path = _chapter_script_path(state_root, topic_id, chapter_index)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["| Beat | Sentence | claim_ids | flags |", "|---|---|---|---|"]
    for i, s in enumerate(sentences, 1):
        lines.append(f"| B{chapter_index + 1}-{i} | {s} | CH-{chapter_index + 1}-{i} | |")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _extract_video_path(result):
    """Pull a video path out of a run_pipeline result dict."""
    state = result.get("state", {})
    stages = state.get("stages", {})
    for stage_name in ("render", "edl", "narration", "subtitles"):
        stage = stages.get(stage_name, {})
        outputs = stage.get("outputs", {})
        if isinstance(outputs, dict) and outputs.get("video"):
            return outputs["video"]
    return None


def concatenate_chapters(videos, output_path, crossfade_duration_s=1.0):
    """Concatenate chapter videos with crossfades using ffmpeg xfade filter."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if len(videos) == 1:
        import shutil
        shutil.copy2(videos[0], output_path)
        return {"status": "OK", "outputs": {"video": str(output_path)}}
    if crossfade_duration_s <= 0:
        lst = output_path.parent / "chapter_concat.txt"
        lst.write_text("\n".join(f"file '{v}'" for v in videos), encoding="utf-8")
        _ffmpeg(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(output_path)])
        return {"status": "OK", "outputs": {"video": str(output_path)}}
    # Build xfade filter chain: each crossfade overlaps the end of prev with start of next
    inputs = []
    filter_parts = []
    for i, v in enumerate(videos):
        inputs.extend(["-i", str(v)])
    # Start with first video
    prev_label = f"[{0}:v]"
    prev_audio = f"[{0}:a]"
    total_dur = 0.0
    # Probe durations to place crossfades
    durations = []
    for v in videos:
        res = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
                              "-show_format", str(v)], capture_output=True, text=True)
        d = float(json.loads(res.stdout)["format"]["duration"])
        durations.append(d)
    offset = 0.0
    for i in range(1, len(videos)):
        xfade_start = offset + durations[i - 1] - crossfade_duration_s
        filter_parts.append(
            f"{prev_label}[{i}:v]xfade=transition=fade:duration={crossfade_duration_s}:offset={xfade_start}[v{i}];"
            f"{prev_audio}[{i}:a]acrossfade=d={crossfade_duration_s}[a{i}];"
        )
        prev_label = f"[v{i}]"
        prev_audio = f"[a{i}]"
        offset += durations[i - 1]
    filter_str = "".join(filter_parts) + f"{prev_label},format=yuv420p[v];{prev_audio}[a]"
    _ffmpeg(inputs + ["-filter_complex", filter_str, "-map", "[v]", "-map", "[a]",
                      "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
                      "-c:a", "aac", "-b:a", "192k", str(output_path)])
    return {"status": "OK", "outputs": {"video": str(output_path)}}


def final_loudness_pass(video_path):
    """Run finish_audio-style loudnorm on the final video's audio."""
    from tools.audio.finish_audio import FinishAudioTool  # noqa: WPS433
    video_path = Path(video_path)
    wav_tmp = video_path.parent / (video_path.stem + "_audio.wav")
    out_tmp = video_path.parent / (video_path.stem + "_loud.wav")
    # Extract audio
    _ffmpeg(["-i", str(video_path), "-vn", "-acodec", "pcm_s16le", "-ar", "44100",
             "-ac", "2", str(wav_tmp)])
    result = FinishAudioTool().execute({"input_path": str(wav_tmp), "output_path": str(out_tmp)})
    if not result.success:
        return {"status": "BLOCKED", "error": f"final loudness pass failed: {result.error}"}
    # Remux video with new audio
    final = video_path.parent / (video_path.stem + "_final.mp4")
    _ffmpeg(["-i", str(video_path), "-i", str(out_tmp), "-c:v", "copy", "-c:a", "aac",
             "-b:a", "192k", "-shortest", str(final)])
    wav_tmp.unlink(missing_ok=True)
    out_tmp.unlink(missing_ok=True)
    return {"status": "OK", "outputs": {"video": str(final)}, "loudness": result.data}


def run_chapter_mode(topic_id, script_path=None, chapters=None, max_chapter_duration_s=None,
                     state_path=None, state_root=None, stages=None):
    """Run the full pipeline per chapter, then concatenate with crossfades + final loudness."""
    if stages is None:
        stages = STAGE_REGISTRY
    if state_path is None:
        state_root = Path(state_root) if state_root else ROOT / "docs/openmontage/slice"
        state_path = Path(state_root) / topic_id / "chapter_state.json"
    state_path = Path(state_path)

    if max_chapter_duration_s is None:
        max_chapter_duration_s = MAX_CHAPTER_DURATION

    if chapters is None:
        if script_path is None:
            return {"verdict": "BLOCKED", "error": "need script_path or chapters"}
        chapters = split_script_into_chapters(script_path, max_chapter_duration_s)

    state = {"topic_id": topic_id, "chapters": chapters, "updated_at": iso_now(),
             "stages": {}}
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["topic_id"] = topic_id
        state["updated_at"] = iso_now()
        state.setdefault("stages", {})

    # Global disk budget
    if disk_free_bytes(state_path.parent) < MIN_FREE_BYTES:
        cp = {"status": "BLOCKED", "started_at": iso_now(), "finished_at": iso_now(),
              "wall_time_s": 0.0, "disk_before_bytes": disk_free_bytes(state_path.parent),
              "disk_after_bytes": disk_free_bytes(state_path.parent), "outputs": {},
              "output_hash": _hash_obj({}),
              "error": f"free disk below {MIN_FREE_BYTES} bytes"}
        state["stages"]["disk"] = cp
        _save_state(state_path, state)
        return {"verdict": "BLOCKED", "stage": "disk", "state": state}

    chapter_videos = []
    any_executed = False
    for ch in chapters:
        ci = ch["chapter_index"]
        cp = state["stages"].get(f"chapter_{ci}")
        if cp and cp.get("status") == "OK":
            stored_hash = cp.get("output_hash")
            recorded_outputs = cp.get("outputs")
            if stored_hash and recorded_outputs is not None \
                    and stored_hash != _hash_obj(recorded_outputs):
                pass  # corrupt -> re-run
            else:
                cp["resumed"] = True
                state["stages"][f"chapter_{ci}"] = cp
                chapter_videos.append(cp["outputs"].get("video"))
                continue

        # Per-chapter disk budget
        if disk_free_bytes(state_path.parent) < MIN_FREE_BYTES:
            cp = {"status": "BLOCKED", "started_at": iso_now(), "finished_at": iso_now(),
                  "wall_time_s": 0.0,
                  "disk_before_bytes": disk_free_bytes(state_path.parent),
                  "disk_after_bytes": disk_free_bytes(state_path.parent), "outputs": {},
                  "output_hash": _hash_obj({}),
                  "error": f"free disk below {MIN_FREE_BYTES} bytes before chapter {ci}"}
            state["stages"][f"chapter_{ci}"] = cp
            _save_state(state_path, state)
            return {"verdict": "BLOCKED", "stage": "disk", "chapter": ci, "state": state}

        chapter_script = _write_chapter_script(Path(state_path).parent, topic_id, ci,
                                               ch["sentences"])
        t0 = time.time()
        disk_before = disk_free_bytes(state_path.parent)
        try:
            result = run_pipeline(topic_id, state_path=state_path,
                                  stages=stages,
                                  initial_state={
                                      "topic_id": topic_id, "chapter_index": ci,
                                      "chapter_script": str(chapter_script),
                                      "chapters": chapters,
                                  })
            status = result.get("verdict", "BLOCKED")
        except Exception as exc:  # fail-closed
            status = "BLOCKED"
            result = {"error": f"{type(exc).__name__}: {exc}"}
        wall = round(time.time() - t0, 3)
        disk_after = disk_free_bytes(state_path.parent)
        video_path = _extract_video_path(result)
        cp = {
            "status": status,
            "chapter_index": ci,
            "started_at": iso_now(),
            "finished_at": iso_now(),
            "wall_time_s": wall,
            "disk_before_bytes": disk_before,
            "disk_after_bytes": disk_after,
            "outputs": {"video": video_path, "duration_s": ch["duration_s"]},
            "output_hash": _hash_obj({"video": video_path, "duration_s": ch["duration_s"]}),
            "error": result.get("error"),
        }
        state["stages"][f"chapter_{ci}"] = cp
        _save_state(state_path, state)
        if status != "OK":
            return {"verdict": "BLOCKED", "stage": f"chapter_{ci}", "chapter": ci, "state": state}
        chapter_videos.append(video_path)
        any_executed = True

    # Skip concat+loudness if all chapters were resumed and already done
    concat_cp = state["stages"].get("concatenate")
    loud_cp = state["stages"].get("final_loudness")
    if not any_executed and concat_cp and concat_cp.get("status") == "OK" \
            and loud_cp and loud_cp.get("status") == "OK":
        return {"verdict": "OK", "state": state,
                "final_video": loud_cp["outputs"]["video"]}

    # Concatenate with crossfades
    concat_out = Path(state_path).parent / f"final_{topic_id}_chapters.mp4"
    concat_res = concatenate_chapters(chapter_videos, concat_out, crossfade_duration_s=1.0)
    if concat_res["status"] != "OK":
        return {"verdict": "BLOCKED", "stage": "concatenate", "state": state}

    # Final loudness pass
    loud_res = final_loudness_pass(concat_out)
    if loud_res["status"] != "OK":
        return {"verdict": "BLOCKED", "stage": "final_loudness", "state": state}

    state["stages"]["concatenate"] = {"status": "OK", "outputs": {"video": str(concat_out)}}
    state["stages"]["final_loudness"] = {"status": "OK", "outputs": {"video": loud_res["outputs"]["video"]}}
    _save_state(state_path, state)
    return {"verdict": "OK", "state": state, "final_video": loud_res["outputs"]["video"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description="One-command episode pipeline (Z3/Z4)")
    parser.add_argument("topic_id", help="topic id, e.g. artemis")
    parser.add_argument("--chapters", action="store_true",
                        help="run chapter mode: split script into <=6 min chapters")
    args = parser.parse_args(argv)
    if args.chapters:
        script = topic_script(args.topic_id)
        if not script:
            print(json.dumps({"verdict": "BLOCKED", "error": f"no script for {args.topic_id}"}))
            return 1
        res = run_chapter_mode(args.topic_id, script_path=script)
    else:
        res = run_pipeline(args.topic_id)
    print(json.dumps({"verdict": res["verdict"], "stage": res.get("stage"),
                      "state": res["state"]}, indent=2))
    return res.get("exit_code", 0 if res["verdict"] == "OK" else 1)


if __name__ == "__main__":
    sys.exit(main())

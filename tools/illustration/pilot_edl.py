#!/usr/bin/env python3
"""tools/illustration/pilot_edl.py — EDL for an all-illustration episode.

Maps every labelled AI still to exactly one cut, spreads cuts across the
script's sentences in proportion to their length, assigns each cut the
sentence's claim_ids, and rotates motion (move/easing/direction) so no two
consecutive cuts repeat a move.

Deterministic: same inputs -> same EDL. No network, no media I/O.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

SPECULATIVE_LABEL = "Speculative illustration"

# (move, easing, direction) — zoompan-expressible moves only.
MOTION_CYCLE = [
    ("pan", "easeinout", "left"),
    ("zoom", "easein", "in"),
    ("detail_crop", "easeout", "right"),
    ("parallax", "easeinout", "up"),
    ("pan", "easeout", "right"),
    ("zoom", "easeinout", "out"),
    ("detail_crop", "easein", "left"),
    ("parallax", "easeout", "down"),
]


def _as_list(value: Any) -> List[Any]:
    return list(value or [])


def _split_ids(raw: Any) -> List[str]:
    text = str(raw or "").replace(";", ",")
    return [p.strip() for p in text.split(",") if p.strip()]


def _assign_images(sentences: Sequence[Dict[str, Any]], n_images: int) -> List[int]:
    """How many images each sentence gets (base + one for the first `extra`)."""
    n = len(sentences)
    base, extra = divmod(n_images, n)
    counts = [base + (1 if i < extra else 0) for i in range(n)]
    if any(c == 0 for c in counts):
        # Fewer images than sentences: give one image to the longest sentences.
        order = sorted(range(n), key=lambda i: -len(str(sentences[i]["sentence"])))
        counts = [0] * n
        for i in order[:n_images]:
            counts[i] = 1
    return counts


def build_illustration_edl(
    images: Iterable[Dict[str, Any]],
    sentences: Iterable[Dict[str, Any]],
    *,
    total_duration: float,
    topic: str,
    episode: str,
    motion_cycle: Sequence[Sequence[str]] | None = None,
    out_path: str | Path | None = None,
) -> Dict[str, Any]:
    imgs = _as_list(images)
    rows = [r for r in _as_list(sentences) if str(r.get("sentence", "")).strip()]
    if not imgs:
        raise ValueError("no images for the EDL")
    if not rows:
        raise ValueError("no sentences for the EDL")
    total = float(total_duration)
    if total <= 0:
        raise ValueError("total_duration must be > 0")

    cycle = [tuple(m) for m in (motion_cycle or MOTION_CYCLE)]
    counts = _assign_images(rows, len(imgs))

    # Sentence durations proportional to spoken length.
    weights = [max(1, len(str(r["sentence"]))) for r in rows]
    wsum = sum(weights)
    sent_durs = [total * w / wsum for w in weights]
    sent_durs[-1] = total - sum(sent_durs[:-1])

    cuts: List[Dict[str, Any]] = []
    motion_segments: List[Dict[str, Any]] = []
    cursor = 0.0
    idx = 0
    for row, dur, count in zip(rows, sent_durs, counts):
        if count == 0:
            continue
        ids = _split_ids(row.get("claim_id"))
        per = dur / count
        for k in range(count):
            img = imgs[idx]
            move, easing, direction = cycle[idx % len(cycle)]
            cut_dur = round(per, 3)
            start = round(cursor, 3)
            end = round(start + cut_dur, 3) if k < count - 1 else round(cursor + dur, 3)
            cut = {
                "cut_id": len(cuts) + 1,
                "start": start,
                "end": end,
                "duration": round(end - start, 3),
                "asset_id": f"ill_{img.get('scene_id', 'scene')}_{Path(str(img['file'])).stem}",
                "source": str(img["file"]),
                "source_sha256": str(img.get("sha256", "")),
                "role": "illustration",
                "kind": "ai_illustration",
                "generator": "AI",
                "label": SPECULATIVE_LABEL,
                "description": f"Speculative illustration for: {row['sentence'].strip()}",
                "rationale": (
                    f"AI illustration ({img.get('scene_id', 'scene')}) illustrating "
                    f"the narration sentence; invented design, labelled on screen."
                ),
                "claim_ids": ", ".join(ids),
                "rights_basis": "ai_generated_illustration",
                "move": move,
                "easing": easing,
                "direction": direction,
                "scene_id": img.get("scene_id", ""),
            }
            cuts.append(cut)
            motion_segments.append({
                "start": start, "end": end, "move": move, "easing": easing,
                "direction": direction, "cut_id": cut["cut_id"],
            })
            cursor = end
            idx += 1

    # Absorb rounding into the final cut so the timeline equals the narration.
    drift = round(total - cursor, 3)
    if cuts and abs(drift) > 0:
        cuts[-1]["end"] = round(cuts[-1]["end"] + drift, 3)
        cuts[-1]["duration"] = round(cuts[-1]["end"] - cuts[-1]["start"], 3)
        motion_segments[-1]["end"] = cuts[-1]["end"]

    edl = {
        "version": 1,
        "episode_id": episode,
        "topic_id": topic,
        "total_duration_s": round(total, 3),
        "resolution": "1280x720",
        "fps": 30,
        "codec": "h264",
        "audio_codec": "aac",
        "source": "illustration manifest + script sentences",
        "cuts": cuts,
        "motion_segments": motion_segments,
    }
    if out_path:
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(edl, indent=2), encoding="utf-8")
    return edl


def sentence_rows(script_path: str | Path) -> List[Dict[str, str]]:
    """Parse a bullet/table script into {sentence, claim_id} rows."""
    import re

    text = Path(script_path).read_text(encoding="utf-8")
    marker = re.compile(r"\s*\[([^\]]*)\]\s*$")
    rows: List[Dict[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            raw = stripped[2:].strip()
            ids = ", ".join(re.findall(r"\[([^\]]*)\]", raw))
            sentence = marker.sub("", raw).strip()
            if sentence:
                rows.append({"sentence": sentence, "claim_id": ids})
        elif stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 3 and re.match(r"^B\d+(?:-\d+)?$", cells[0]) and cells[1]:
                rows.append({"sentence": cells[1], "claim_id": cells[2]})
    return rows


def images_from_manifest(manifest_path: str | Path) -> List[Dict[str, Any]]:
    """Read the labelled illustration manifest into EDL image records."""
    data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    out = []
    for ent in data.get("images", []):
        out.append({
            "file": ent["file"],
            "sha256": ent.get("sha256", ""),
            "scene_id": ent.get("scene_id", ""),
        })
    return out

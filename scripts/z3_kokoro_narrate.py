#!/usr/bin/env python3
"""scripts/z3_kokoro_narrate.py — synthesize a script's sentences with Kokoro-82M CPU."""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline

INTRO_S = 1.0
PAUSE_S = 0.5
TRAIL_S = 1.3
SR = 24000


def parse_script(path):
    sentences = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("| B"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 4 and cells[0][:2] in ("B1", "B2", "B3", "B4", "B5", "B6"):
            sentences.append(cells[1])
    return sentences


def main():
    script_path, out_wav = sys.argv[1], sys.argv[2]
    sentences = parse_script(script_path)
    pipeline = KPipeline(lang_code="a")
    pipeline.load_voice("af_heart")
    silence = lambda sec: np.zeros(int(sec * SR), dtype=np.float32)
    parts = [silence(INTRO_S)]
    full = []
    for text in sentences:
        chunks = []
        for _, _, audio in pipeline(text, voice="af_heart", speed=1.0):
            chunks.append(np.asarray(audio, dtype=np.float32))
        seg = np.concatenate(chunks) if len(chunks) > 1 else chunks[0]
        parts.append(np.asarray(seg, dtype=np.float32))
        parts.append(silence(PAUSE_S))
        full.append(text)
    parts[-1] = silence(TRAIL_S)
    narration = np.concatenate(parts)
    Path(out_wav).parent.mkdir(parents=True, exist_ok=True)
    sf.write(out_wav, narration, SR)
    print(json_out := __import__("json").dumps({
        "sentences": len(sentences),
        "duration_s": round(len(narration) / SR, 6),
        "sample_rate": SR,
        "wav": out_wav,
        "full_text": " ".join(full),
    }))


if __name__ == "__main__":
    main()

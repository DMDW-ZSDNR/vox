#!/usr/bin/env bash
#
# scripts/rebuild_slice_assets.sh — OpenMontage CID slice rebuild (G1 portability)
#
# Purpose: Rebuild every media asset used in the slice from the committed manifest
#          (docs/openmontage/assets/CID_SLICE_MANIFEST.json), using curl -L and
#          sha256 verification. Media itself is gitignored (projects/); this script
#          regenerates it from source URLs.
#
# Usage:   bash scripts/rebuild_slice_assets.sh [assets_dir]
#          Default assets_dir: projects/slice_cid_v0
#
# Non-git dependencies (must be installed in the new account):
#   - curl      (download; follows archive.org HTTP 302 redirects via -L)
#   - sha256sum (verify downloaded file integrity)
#   - ffmpeg    (rebuild slice: scale, pad, zoompan, concat, mix narration)
#   - ffprobe   (probe duration/resolution/fps)
#   - python3   (Kokoro TTS + finish_audio + qc.py; see HANDOFF_NEW_ACCOUNT.md)
#   - kokoro + misaki Python packages (~313 MB weights from Hugging Face)
#   - espeak-ng (Kokoro text frontend)
#
# Secrets the new account must recreate (name only, never values):
#   - KAGGLE_API_TOKEN  (Codespaces secret; name only)
#
# Exit codes: 0 = all assets OK; 1 = any download/verify failure.
set -euo pipefail

ASSETS_DIR="${1:-projects/slice_cid_v0}"
MANIFEST="docs/openmontage/assets/CID_SLICE_MANIFEST.json"
STILL_DIR="$ASSETS_DIR/stills"

echo "[rebuild] manifest: $MANIFEST"
echo "[rebuild] assets dir: $ASSETS_DIR"

mkdir -p "$ASSETS_DIR" "$STILL_DIR"

# Parse manifest with python3 (json). Output TSV: download_url<TAB>file_name<TAB>sha256<TAB>dest
mapfile -t ENTRIES < <(python3 -c "
import json, sys
m = json.load(open('$MANIFEST'))
for a in m['assets']:
    url = a['download_url']
    name = a['file_name']
    sha = a['sha256']
    if a['role'] == 'still_primary':
        dest = '$STILL_DIR/' + name
    else:
        dest = '$ASSETS_DIR/' + name
    print(url + chr(9) + name + chr(9) + sha + chr(9) + dest)
")

failures=0
for entry in "${ENTRIES[@]}"; do
    IFS=$'\t' read -r url name sha dest <<< "$entry"
    echo "[rebuild] $name -> $dest"
    if [ -f "$dest" ]; then
        existing=$(sha256sum "$dest" | awk '{print $1}')
        if [ "$existing" = "$sha" ]; then
            echo "[rebuild]   $name already present and sha256 matches; skipping download"
            continue
        fi
        echo "[rebuild]   $name present but sha256 mismatch; re-downloading"
    fi
    # Download with curl -L (follows archive.org HTTP 302 redirects)
    if ! curl -s -L --max-time 120 --fail -o "$dest.part" "$url"; then
        echo "[rebuild]   FAILED: curl download of $url"
        failures=$((failures + 1))
        continue
    fi
    # Verify sha256
    got=$(sha256sum "$dest.part" | awk '{print $1}')
    if [ "$got" != "$sha" ]; then
        echo "[rebuild]   FAILED: $name sha256 mismatch (expected $sha, got $got)"
        rm -f "$dest.part"
        failures=$((failures + 1))
        continue
    fi
    mv "$dest.part" "$dest"
    echo "[rebuild]   OK: $name downloaded and sha256 verified"
done

echo "[rebuild] summary: failures=$failures"
if [ "$failures" -gt 0 ]; then
    echo "[rebuild] ABORT: $failures asset(s) failed download/verify"
    exit 1
fi
echo "[rebuild] DONE: all assets present and sha256-verified"
exit 0

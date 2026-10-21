# S5 State — 10-image 3-model bake-off (Kilo)

**Resume rule:** resume at the first phase not DONE. Never loop on Kaggle status:
submit once, record here, do other phases, ONE status call between phases.
STOP RULE: max 2 fix attempts per model → BLOCKED with the exact error, then move on.
Never commit media; no secrets printed; fp16 only; no bitsandbytes; no paid routes;
no CPU fallback; stop if free disk < 800 MB.

## Phase status

| Phase | Status | Evidence |
|---|---|---|
| S5-1 FIXED TEST SET | DONE | 10 scenes (s02 + s07 dropped as the 2 easiest), 1 seed/scene, 1024x1024, sdxl=A / zimage=B / klein=C, 3-scene identical-text neutral check: `docs/openmontage/image_gen/S5_TEST_SET.json` (39 renders), mapping `S5_TEST_SET_MAPPING.json` |
| S5-2 RUN ORDER | IN_PROGRESS | SDXL SUBMITTED `s5-sdxl-1` (13 renders); klein PENDING; zimage PENDING. S4 SDXL job could NOT be reused: it ended `ERROR` with 0 images (blanket `from diffusers import ZImagePipeline` in the S4 runner crashed the SDXL run) |
| S5-3 OBJECTIVE CHECKS | PENDING | scripts/s5_checks.py (laplacian blur, text-like artifact, phash dupes, resolution) |
| S5-4 BLIND PACK | PENDING | projects/s5_blind/ (gitignored) |
| S5-5 TALLY HELPER | PENDING | scripts/s5_tally.py + tests |
| S5-6 REPORT | PENDING | docs/openmontage/image_gen/BAKEOFF_S5.md |

## Run log

- 2026-10-21: S4 `forts845/openmontage-runner` status = ERROR (one status call).
  Fetched log: `ImportError: cannot import name 'ZImagePipeline'` — S4 runner imported
  all four pipelines for every model, so the released-diffusers SDXL run died too.
  S5 runner imports only the class the job needs.
- SDXL/klein use `diffusers>=0.36,<0.37` (released); Z-Image needs a release that
  ships `ZImagePipeline`, so its attempt 2 is `diffusers>=0.37` — both attempts are
  logged in the kernel's `install_log.json`.

## Notes

- `tools/prompting/` and `scripts/score_rubric.py` are OpenCode-owned: used read-only.
  Two cosmetic duplications found in builder output (see
  `docs/openmontage/OPENCODE_REQUESTS.md`) — not patched here.
- Disk: checked before each phase (stop below 800 MB free).

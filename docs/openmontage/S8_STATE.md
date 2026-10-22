# S8 state — 5-model image bake-off (Kilo)

**Rule:** resume at the first unfinished phase. Repository reality outranks this
file. S8 reuses the finished S7 runs (SDXL Base, FLUX.2-klein-4B) and adds up
to 3 new models; **Z-Image-Turbo is not submitted in S8**.

Scope: `docs/`, `tools/` (not `tools/prompting/`, not `scripts/score_rubric.py`),
`scripts/`, `tests/`, `.kilo/`. No secrets printed, no paid routes, no
bitsandbytes, no CPU fallback, **fp16 only**, released library versions pinned
in every manifest (**no git main**), one Kaggle status call between phases
(never a polling loop), stop if free disk < 800 MB, own paths only, no media in
git.

## Phases

| Phase | Status | Note |
|---|---|---|
| S8-1 LICENSE AND FIT GATE | DONE | `docs/openmontage/image_gen/CANDIDATES_S8.md` + evidence `S8_CANDIDATE_FACTS.json` (official HF cards only, no weights downloaded). Krea 2 Turbo = LICENSE_BLOCKED (gated auto, community licence PDF unreadable, 12.8 B params) -> NOT RUN. SDXL-Lightning, dreamshaper-xl-lightning, Sana Sprint 1.6B = FITS_T4. sdxl-turbo = LICENSE_BLOCKED (revenue cap). |
| S8-2 RUN THE NEW MODELS | IN_PROGRESS | sdxl-lightning attempt 1 crashed before any model was touched (RecursionError in the composed runner) -> attempt 2 RUNNING. dreamshaper-xl and sana-sprint-1.6b are queued. |
| S8-3 MEASURE + OBJECTIVE QC | PENDING | load time, steady s/image, usable img/min, peak VRAM, black/NaN/OOM, attempts, versions; per-image blur / text-like / pHash flags (text detector was unreliable in S7 - say so). |
| S8-4 AGENT SELF-ASSESSMENT | PENDING | advisory only, labelled "agent opinion, not independent, a vision model can miss anatomy errors". |
| S8-5 OWNER PACK (5 panels) | PENDING | `projects/s8_blind/` (gitignored), panels A-E per scene, `results.csv`, tally extended to 5 models (test-first). |
| S8-6 REPORT | PENDING | `docs/openmontage/image_gen/BAKEOFF_S8.md` + this file + LESSONS.md + commit. No winner declared by the agent. |

## Facts carried over from S7 (reuse, do not redo)

| model | job | load s | steady s/img | usable img/min | peak VRAM MB | black/NaN/OOM | notes |
|---|---|---|---|---|---|---|---|
| SDXL Base 1.0 + `madebyollin/sdxl-vae-fp16-fix` | `s7-sdxl-1` | 86.233 | 41.400 | 1.42 | 9169.58 | 0/0/0 | 10/10, bridge verify PASS. Media re-run `s7-sdxl-2` reproduced run 1 **bit-for-bit** (10/10 sha256 identical) -> the S8 reuse is verified against the same sha256 list. |
| FLUX.2-klein-4B | `s7-klein-1` | 133.852 | 24.691 | 2.17 | 7995.02 | 0/0/0 | 10/10, bridge verify PASS, `Flux2KleinPipeline` + CPU offload. |
| Z-Image-Turbo | `s7-zimage-4` | 277.644 | 51.908 | 0.00 | 12355.12 | **10**/0/0 | BLOCKED in S7 (fp16 NaN -> black frames). **Not submitted in S8.** |

S7 images that S8 reuses (gitignored cache, sha256 re-verified against the S7
manifests): `output/s7_cache/sdxl/`, `output/s7_cache/klein/`.

## Prompt variants for S8 (tools/prompting is OpenCode-owned: read/use only)

| model | target used in the builder | variant | why |
|---|---|---|---|
| SDXL Base (reused) | `sdxl` | A | structured phrases + short negative prompt |
| FLUX.2-klein-4B (reused) | `klein` | C | prose, anatomy first, no negative prompt |
| SDXL-Lightning | `sdxl` | A | SDXL family |
| DreamShaper XL Lightning | `sdxl` | A | SDXL family |
| SANA-Sprint 1.6B | `klein` | C | the card prescribes no negative-prompt behaviour -> prose, anatomy first, no negative prompt (same text as klein) |

## Attempt log

| model | attempt | what changed | result |
|---|---|---|---|
| sdxl-lightning | 1 | first attempt (vendor-card recipe, rung released_037_x4) | FAILED before any model call - `RecursionError: maximum recursion depth exceeded`: in the concatenated run.py the S8 additions' `def main()` shadowed the engine's `main()`, so `_ENGINE.main()` called itself. Traceback: `docs/openmontage/image_gen/logs/s8-sdxl-lightning-1/kernel.log` |
| sdxl-lightning | 2 | fixed the runner: the engine's `main` is captured as `_ENGINE_MAIN` before the S8 `main` is defined; same released stack (the stack was never exercised) | RUNNING (submitted 01:05Z) |
| dreamshaper-xl-lightning | - | - | not started |
| sana-sprint-1.6b | - | - | not started |

## Notes

- The Kaggle runner kernel keeps only the output of its **latest** version:
  fetch + verify + copy every run's output before pushing the next model.
- `/tmp` was wiped by a sandbox restart during S7; fetched images are mirrored
  to the gitignored `output/s7_cache/` (S8 will use `output/s8_cache/`).
- Install ladder (released versions only, no git main):
  `released_037_x4` = diffusers 0.37.0 + transformers 4.57.6 + hub<1.0 (first
  rung, ships `StableDiffusionXLPipeline`, `SanaSprintPipeline`,
  `Flux2KleinPipeline`), `released_037_x5` = diffusers 0.37.0 + transformers
  5.20.2 + hub 1.x, `released_036_x4` = diffusers 0.36.0 + transformers 4.57.6
  + hub<1.0. diffusers 0.41.0 is excluded: it needs hub>=1.32 (conflict with
  transformers 4.x) and its torchao import fails (`FqnToConfig`).
- Free disk at the start of S8: `/workspaces` 2.3 GB, `/tmp` 39 GB (stop if
  free disk < 800 MB).

## Exact next action

1. Build the S8 test set (same 10 scenes, same seeds, 5 models x 10 scenes =
  50 renders, new models only) and extend the runner + push script for the
   three new models.
2. Run the three new models back-to-back (one kernel each), fetch + verify
   each output before pushing the next one.
3. Measure, QC, self-assess, build the 5-panel owner pack, extend the tally to
   5 models, and write `BAKEOFF_S8.md`.

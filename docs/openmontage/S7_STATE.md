# S7 State — 3-model image bake-off, 10 images each (Kilo)

**Resume rule:** resume at the first phase not DONE. Never loop on Kaggle status:
submit once, record here, do other work, ONE status call between phases.
**STOP RULE:** per model up to 4 attempts, 90 min wall-time cap per model. After
each failure: save the full traceback, write a one-line diagnosis here, and
CHANGE something concrete before retrying (never an identical attempt). After
the cap -> BLOCKED with the exact error, versions and traceback path, then move
to the next model. The run ends only when all 3 models are DONE or BLOCKED.
Never commit media; no secrets printed; fp16 only; no bitsandbytes; no paid
routes; no CPU fallback (CPU *offload* is allowed: compute stays on the GPU).
Stop everything only if free disk < 800 MB.

**Supersedes S5:** S5's SDXL and klein kernel runs both ended ERROR with 0
images (fetched output proved it: the klein run died at `pipe.to("cuda")` with
`NotImplementedError: Cannot copy out of meta tensor`), so no S5 output is
reusable and nothing completed is redone.

## Phase status

| Phase | Status | Evidence |
|---|---|---|
| S7-1 FIXED TEST SET | DONE | 10 scenes (s02, s07 dropped as the 2 easiest), 1 seed/scene shared by all 3 models, 1024x1024, variants sdxl=A / zimage=B / klein=C, 30 renders: `docs/openmontage/image_gen/S7_TEST_SET.json` + `S7_TEST_SET_MAPPING.json` (built by `scripts/s7_build_testset.py` via tools/prompting.builder, read-only) |
| S7-2 RUNNER + PUSH | DONE | `tools/kaggle_bridge/s7_bakeoff_run.py` (install ladder, import probe, fp16, 90 min wall cap, full measurements), `scripts/s7_push_bakeoff.py`; 25 local tests pass (`tests/test_s7_runner.py`, `tests/test_s7_push_bakeoff.py`, `tests/test_s7_tally.py`) |
| S7-3 SDXL Base + madebyollin/sdxl-vae-fp16-fix | DONE | job `s7-sdxl-1` COMPLETE, 10/10 images, bridge verify PASS (all sha256/bytes match). Load 86.233 s, steady 41.4 s/img, 1.42 usable img/min, peak VRAM 9169.58 MB, black/NaN/OOM = 0, `StableDiffusionXLPipeline`. Versions: diffusers 0.36.0, transformers 4.57.6, huggingface_hub 0.36.2, torch 2.11.0+cu128, accelerate 1.14.0, safetensors 0.8.0, numpy 2.1.3, pillow 12.3.0, CUDA 12.8, Tesla T4, Python 3.13.15 |
| S7-4 FLUX.2-klein-4B | IN_PROGRESS | job `s7-klein-1` SUBMITTED 11:09:25Z (attempt 1, ladder released_037_x4 -> released_037_x5 -> released_041_x5_ao -> git_main_x5_ao, `Flux2KleinPipeline`, `enable_model_cpu_offload`, guidance 1.0) |
| S7-5 Z-Image-Turbo | PENDING | starts after klein is DONE or BLOCKED |
| S7-6 OBJECTIVE QC | PENDING | `scripts/s7_checks.py` (Laplacian blur, text-like heuristic, dHash duplicates, resolution, saturation/contrast outliers) |
| S7-7 BLIND PACK | PENDING | `scripts/s7_blind_pack.py` -> `projects/s7_blind/` (gitignored) |
| S7-8 TALLY HELPER | DONE | `scripts/s7_tally.py` (test-first, 13 tests) -> wins, anatomy-ok, speed/VRAM table, AGENT vs OWNER, TIE at <=1 win |
| S7-8b AGENT SCORE AGGREGATOR | DONE | `scripts/s7_agent_assessment.py` (rubric CSV -> severe artifacts / usable share / repair burden / ranking + `agent_pick`) |
| S7-9 AGENT SELF-ASSESSMENT | PENDING | 30 images viewed with the image Read capability, rubric 0-2 per category, advisory only |
| S7-10 REPORT | PENDING | `docs/openmontage/image_gen/BAKEOFF_S7.md` + LESSONS.md + commit |

## Run log

- 2026-10-21 10:49Z: S5 fetched output = `s5_bakeoff_klein` only, status
  `BLOCKED: model load failed: NotImplementedError: Cannot copy out of meta
  tensor; no data!` (traceback at `pipe.to("cuda")`). Root cause for the record:
  the S5 job used `Flux2Pipeline` (the FLUX.2-**dev** class) for
  FLUX.2-**klein**-4B, whose text encoder is Qwen3 -> the pipeline was left on
  the meta device. Fix for S7: use `Flux2KleinPipeline` (the class the vendor
  card and the HF model page use) + `enable_model_cpu_offload()`.
- 2026-10-21 10:52Z: S7 SDXL attempt 1 SUBMITTED (job `s7-sdxl-1`, 10 renders,
  install ladder released_041_x4 -> released_041_x5 -> released_036_x4 ->
  git_main_x4; fp16; VAE madebyollin/sdxl-vae-fp16-fix).
- 2026-10-21 10:55Z: one status call -> `KernelWorkerStatus.RUNNING`.
- 2026-10-21 11:05Z: SDXL attempt 1 -> DONE on internal rung 3 (`released_036_x4`).
  Rung 1 `released_041_x4` died in pip: `ResolutionImpossible` (diffusers 0.41.0
  needs huggingface_hub>=1.32,<2.0 but transformers 4.57.6 pins hub<1.0).
  Rung 2 `released_041_x5` installed but the import failed:
  `cannot import name 'FqnToConfig' from 'torchao.quantization'` (the kernel's
  torchao is too old). Rung 3 `released_036_x4` (diffusers 0.36.0, torchao
  0.15.0) worked. Attempt 1 succeeded, so 1 attempt was used.
- 2026-10-21 11:09Z: klein attempt 1 SUBMITTED (job `s7-klein-1`, 10 renders,
  ladder released_037_x4 -> released_037_x5 -> released_041_x5_ao ->
  git_main_x5_ao; `Flux2KleinPipeline` + `enable_model_cpu_offload`; guidance 1.0).
  The SDXL ladder was reworked afterwards: the dead rungs (041_x4 hub conflict,
  041_x5 torchao) are no longer tried first.

## Attempt log (per model)

| model | attempt | what changed | result |
|---|---|---|---|
| sdxl | 1 | released diffusers 0.41.0 + transformers 4.57.6 + hub<1.0 | DONE (10/10) via internal rung 3 `released_036_x4`; rungs 1-2 dead (hub conflict, torchao) |
| klein | 1 | `Flux2KleinPipeline` + `enable_model_cpu_offload` (fixes the S5 meta-tensor failure), ladder released_037_x4 -> released_037_x5 -> released_041_x5_ao -> git_main_x5_ao | RUNNING (submitted 11:09:25Z) |

## Notes

- `tools/prompting/` and `scripts/score_rubric.py` are OpenCode-owned: read
  only. Known cosmetic duplication in the builder output ("A flat-vector
  field-guide plate field-guide plate.") is reported, not patched.
- Vendor cards were checked before running (S4-1 PROMPTING_FACTS.md):
  klein = Flux2KleinPipeline, 4 steps, guidance 1.0, CPU offload;
  z-image = ZImagePipeline, 9 steps, guidance 0.0, low_cpu_mem_usage=False;
  SDXL = StableDiffusionXLPipeline, 50 steps, guidance 7.5 + short negative.
- fp16 is mandated by S7 even where the vendor card says bfloat16 (klein, and
  Z-Image): recorded as a deliberate deviation, not an oversight.
- Disk: 2.7 GB free on /workspaces (stop threshold 800 MB), 39 GB on /tmp.

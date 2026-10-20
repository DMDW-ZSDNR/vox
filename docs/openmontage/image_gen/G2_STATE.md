# G2 State — AI Image Generation Bake-off (Kilo)

**Kernel slug:** forts845/g2-image-bakeoff  
**Job id:** g2-bakeoff-1  
**Submit time:** 2026-10-20T08:45:00Z (v1), 2026-10-20T~16:15Z (v2 re-push)  
**Last known status:** KernelWorkerStatus.RUNNING (version 2 pushed OK; URL https://www.kaggle.com/code/forts845/g2-image-bakeoff)  
**Root cause (v1, from log):** all 3 models failed at fp16 load attempt 0; error swallowed; bitsandbytes 8-bit fallback NOT installed on Kaggle image → 0 images, 0.0 GPU min.  
**Fix applied (v2, run.py):** load_pipe now logs attempt-0 errors, skips bitsandbytes when unavailable, reaches CPU float32 fallback at reduced resolution (512px, steps/2) so generation completes even on CPU.  
**Next steps (resume when COMPLETE):**
1. `kaggle kernels status forts845/g2-image-bakeoff` (ONE call only)
2. If COMPLETE: `kaggle kernels output` / bridge `fetch_output` to projects/image_gen/g2/ (expect manifest.json + imgs/ + contact sheets)
3. Verify manifest job_id == g2-bakeoff-1; sha256+bytes of every file (non-zero exit on mismatch)
4. Record seconds/image, peak VRAM, GPU minutes; build contact sheets A/B/C + g2_model_mapping.json
5. Write docs/openmontage/image_gen/G2_REPORT.md with per-model verdicts (USEFUL|MARGINAL|NOT_USEFUL)
6. If ERROR: read log, report exact cause (no further re-push allowed — v2 was the one fix)

**If still queued/running at end of session:** finish with this G2_STATE.md + the exact resume command above; do NOT wait/loop on status.

## License pre-check (unchanged)
- SDXL-Lightning + SDXL base: OpenRAIL++ — commercial OK.
- Z-Image-Turbo: apache-2.0 — commercial OK.
- FLUX.2-klein-4B: apache-2.0, commercial OK.

## Constraints
- Outputs → gitignored projects/image_gen/g2/ only; never commit media.
- Disk < 800 MB free → STOP whole run.

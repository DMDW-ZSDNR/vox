# S1 State — Speculative Evolution / Alien Ecosystems (AI stills only) — Kilo

**Resume rule:** Resume at the first phase not DONE. Do not sleep or loop on Kaggle
status: submit once, record here, do other phases, check status with ONE call between
phases. Never commit media. KAGGLE_API_TOKEN: env check yes/no only (never print).

## Phase status

| Phase | Status | Evidence | Commit hash |
|-------|--------|----------|-------------|
| S1-1 IMAGE MODEL (Z-Image-Turbo) | IN_PROGRESS | job `s1-z-image-turbo-1` pushed to `forts845/openmontage-runner`; awaiting output fetch + manifest verify | — |
| S1-1 FLUX.2-klein-4B | PENDING | license clear per LICENSE_EVIDENCE.md; ~13 GB VRAM — memory-fit TBD on T4 | — |
| S1-2 BLIND COMPARISON | PENDING | needs S1-1 images | — |
| S1-3 STYLE BIBLE | PENDING | docs/openmontage/niches/speculative_evolution/STYLE_BIBLE.md + niche YAML | — |
| S1-4 PILOT SCRIPT + LEDGER | PENDING | topic "How could life survive beneath a frozen alien ocean?" 10-12 min | — |
| S1-5 BUILD | BLOCKED | requires S1-1 >= 1 USEFUL model | — |
| S1-6 CLOSE | PENDING | OWNER_ACTIONS.md, CHANGELOG.md, LESSONS.md, S1_STATE.md | — |

## S1-1 job records

| Model | Job id | Kernel slug | Prompts | Seeds | Seconds/image | Peak VRAM | GPU minutes | Revision | Manifest verified |
|-------|--------|-------------|---------|-------|---------------|-----------|-------------|----------|-------------------|
| Z-Image-Turbo | s1-z-image-turbo-1 | forts845/openmontage-runner | 12 (fixed) | fixed | TBD | TBD | TBD | TBD | NO |

## Notes

- LICENSE_EVIDENCE.md: Z-Image-Turbo (apache-2.0, commercial OK), FLUX.2-klein-4B (apache-2.0, commercial OK) — neither BLOCKED on license grounds (verified 2026-10-20 from official HF cards).
- G2 concluded FAILED (bitsandbytes missing, CPU fallback, dict-not-callable, FLUX OOM). S1-1: fp16 only, NO bitsandbytes, NO CPU fallback, non-zero exit if images < prompts, full tracebacks saved to output.
- Disk: 2.8 GB free on /workspaces (> 800 MB stop threshold).
- Kaggle kernels owned by forts845/FORTS_FACTORY; g2-image-bakeoff NOT reused (G-rules: no further re-push).

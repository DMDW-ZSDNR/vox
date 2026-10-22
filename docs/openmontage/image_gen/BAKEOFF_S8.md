# S8 — 5-model image bake-off (Kilo)

**Status: in progress.** This file is the final report; it is filled in when the
three new model runs are done. No winner is declared by the agent: the owner's
blind CSV decides.

Scope: `docs/`, `tools/` (not `tools/prompting/`, not `scripts/score_rubric.py`),
`scripts/`, `tests/`, `.kilo/`. fp16 only, released library versions pinned in
every manifest (no git main), no bitsandbytes, no CPU fallback, no paid routes,
no secrets printed, no media in git, one Kaggle status call between phases.

Models compared (5):

| # | model | source | licence | status |
|---|---|---|---|---|
| 1 | SDXL Base 1.0 + `madebyollin/sdxl-vae-fp16-fix` | S7 run `s7-sdxl-1` (reused, sha256 verified) | OpenRAIL++ | DONE in S7 |
| 2 | FLUX.2-klein-4B | S7 run `s7-klein-1` (reused, sha256 verified) | BFL card | DONE in S7 |
| 3 | SDXL-Lightning 8-step | `ByteDance/SDXL-Lightning` (new) | OpenRAIL++ | running |
| 4 | DreamShaper XL Lightning | `Lykon/dreamshaper-xl-lightning` (new) | OpenRAIL++ | queued |
| 5 | SANA-Sprint 1.6B 1024px | `Efficient-Large-Model/Sana_Sprint_1.6B_1024px_diffusers` (new) | Apache-2.0 | queued |

Not submitted: **Z-Image-Turbo** (S7 verdict: BLOCKED, fp16 NaN -> black
frames) and **Krea 2 Turbo** (S8-1 verdict: LICENSE_BLOCKED - gated auto with
a community licence whose commercial terms could not be verified, 12.8 B
params). See `CANDIDATES_S8.md`.

---

## 1. Observed vs assumed

<!-- FILLED -->

---

## 2. Licence and fit table

<!-- FILLED: pointer to CANDIDATES_S8.md + the three run models -->

---

## 3. Attempts log per model

<!-- FILLED -->

---

## 4. Speed / VRAM table

<!-- FILLED -->

---

## 5. Objective QC

<!-- FILLED -->

---

## 6. Advisory agent ranking

<!-- FILLED -->

---

## 7. BLOCKED causes

<!-- FILLED -->

---

## 8. Owner steps (exact)

<!-- FILLED -->

---

## 9. Winner (owner-decided)

**Not decided yet.**

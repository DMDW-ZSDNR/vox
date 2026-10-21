# OpenCode requests — Milestone S3 (speculative evolution build alongside Kilo)
**Created:** 2026-10-21 | **Branch:** factory/business-documentary-pilot (root) / aviation-test-history-demand (nested youtube-niche-finder)

## Commit hashes (OpenCode's own paths only; no git add -A, no media/secrets)
- Root repo (`/workspaces/OpenMontage`): `19d933c` — S3 prompt builder, rubric scorer, test plan, creature specs, fact packs, S3_STATE.md
- Nested repo (`youtube-niche-finder/`): `f788193` — reports/S3_STATE.md

## Open requests (owner decisions needed)
1. **Prompt test plan matrix (S3-2):** 12 scenes x 3 models x 3 variants = 108 renders
   (docs/openmontage/image_gen/prompt_test_matrix.json). Approve Kilo's bridge job to run it.
   **Note:** 108 renders ÷ 9 cells = 12 images per cell, which is BELOW the rubric scorer's
   24-image minimum, so the winner table will print "INSUFFICIENT" (directional only).
   Either (a) approve running as-is for directional signal, or (b) approve expanding scenes
   to reach ≥24 images per cell before Kilo runs the bridge.
   **UPDATE (S4, owner-directed):** Kilo expanded the matrix to 2 seeds per scene =
   12 scenes x 2 seeds x 3 models x 3 variants = 216 renders; 24 images per cell
   (docs/openmontage/image_gen/prompt_test_matrix.json schema 1.1, prompt_test_mapping.json
   regenerated). This meets the scorer's ≥24/cell minimum. OpenCode's
   tools/prompting.builder renders the prompts; Kilo's bridge job reads the matrix.
2. **No niche recommended yet (S2 carryover):** YouTube search quota exhausted
   (search.list rateLimitExceeded, project 255936762081). S1-S5 demand metrics are
   NOT_MEASURED, not NOISE. Re-run niche breakout/replication measurement after the search
   quota resets (midnight Pacific); no niche should be greenlit without measured numbers.
3. **S3-1 prompt builder** is complete and tested (19 pass). Model keys/endpoints are not
   configured in this repo; generation happens via Kilo's Kaggle bridge (not touched here).
4. **Nothing to change in Kilo's scope:** tools/kaggle_bridge, tools/qa, tools/audio,
   scripts/run_episode.py, .kilo/, AGENTS.md, .env* were not touched. Any needed change
   there should be submitted as a new entry in this file.

## Files OpenCode created/edited (commit 19d933c)
tools/prompting/{__init__.py,builder.py,SOURCES.md},
tests/prompting/{__init__.py,test_builder.py}, tests/test_score_rubric.py,
scripts/score_rubric.py,
docs/openmontage/niches/speculative_evolution/creatures/{vent_grazer,filter_drifter,ice_burrower,vent_chimney_field,under_ice_cavern,frozen_ocean_food_web}.yaml,
docs/openmontage/image_gen/{PROMPT_TEST_PLAN.md,prompt_test_matrix.json,prompt_test_mapping.json},
docs/openmontage/evidence/spec_evo/{pilot2_no_land_ocean_world,pilot3_low_gravity_flying_food_web}.md

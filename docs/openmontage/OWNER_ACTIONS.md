# Owner Actions — OpenMontage MASTER RUN

**Status:** F5 complete. Numbered, minimal steps for the owner.
**None of these are blocking for the demo slice (which is NOT_PUBLISHABLE), but all must be resolved before any publish.**

## 1. Voice license decision (REQUIRED before publish)

The slice uses Kokoro-82M (CPU local synthesis, Kaggle GPU bake-off BLOCKED).

- [ ] Review `docs/openmontage/VOICE_DECISION.md` and `docs/openmontage/VOICE_BAKEOFF_LICENSES.md`
- [ ] Decide: accept Kokoro-82M (Apache-2.0 weights, but CC BY training items + synthetic-data origin UNKNOWN) or select a different voice
- [ ] If accepting Kokoro: record the decision, note the CC BY attribution obligations (Koniwa `tnc`, SIWIS), and note the synthetic-data provenance gap
- [ ] Piper `en_US-lessac-medium` remains BLOCKED (license UNKNOWN) — do not use for publish

## 2. Clip rights review (REQUIRED before publish)

All 4 CID clips in the slice are `source_policy_us_gov` and have been owner-reviewed as `USABLE_FOR_SLICE` (viewed in final F5 video only, not every source frame):

- [ ] Review `docs/openmontage/audit/REVIEW_QUEUE.md` (F5 owner review section + CID section)
- [ ] For each clip, the owner has confirmed: no identifiable persons, no logo/insignia visible, no third-party credit
- [ ] Full video (all source frames) still needs full-clip review before publish — this is the open item
- [ ] All 4 clips currently have NO third-party credit in metadata (passes this check)

## 3. Single-source claims (REQUIRED before publish)

CID-13 (load-bearing: "modified fuel ineffective; FAA requirements cancelled") has only one source (NASA Facts FS-2009-02-003-CID).

- [ ] Find a second source for CID-13, or
- [ ] Remove/S8 from the script (S8 is BLOCKED until CID-13 has a second source), or
- [ ] Accept single-source risk with owner sign-off

Other single-source claims (CID-06, CID-10, CID-12, CID-14, CID-15) should also be reviewed.

## 4. NASA insignia clearance (OWNER DECISION)

CID footage may show NASA insignia on vehicles/facilities. Per NASA Media Usage Guidelines, insignia use is protected by law; incidental appearance does not convey rights.

- [ ] Decide: does the slice's incidental insignia require separate clearance?
- [ ] If yes, contact NASA media usage for approval before publish

## 5. Monetization / publishing readiness (NOT ASSESSED)

- [ ] No monetization eligibility review has been performed
- [ ] No AdSense/YouTube partnership review
- [ ] Content ID / music policy: no music used (MUSIC_POLICY.md: no music unless license evidence exists)
- [ ] Narration uses Kokoro-82M synthetic voice — confirm commercial-use rights before publish

## 6. Kaggle GPU quota (UNVERIFIED — blocks P3)

- [ ] Verify phone number in Kaggle settings (may be required for GPU/internet)
- [ ] Check GPU quota (30 h/week limit, unverified)
- [ ] Retry the Kaggle voice bake-off (P3) — 1 retry attempt remains (max 2)

## Quick reference — slice artifacts (gitignored, in projects/slice_cid_v0/)

| File | Purpose |
|---|---|
| `final_slice.mp4` | 46.0s, 1920x1080, 30fps, h264/aac (NOT_PUBLISHABLE) |
| `qa_report.json` | 12/12 QC checks PASS (freezedetect REVIEW on static title cards) |
| `edit_decisions.json` | EDL with per-cut rationale + static_segments[] |
| `credits.txt` | All clip credits + rights_basis |
| `subtitles.srt` | 7 caption cues from Kokoro narration (S1-S7, S8 omitted) |
| `contact_sheet_f5.jpg` | ~12 frames of final video |
| `rights_records.json` | Per-clip rights_basis (9 clips, all source_policy_us_gov, 4 clips USABLE_FOR_SLICE) |
| `narration_manifest.json` | Narration duration 46.0s + tolerance 1.0s |

## 7. Slice rebuild / portability (G1)

- [ ] Review `scripts/rebuild_slice_assets.sh` and `docs/openmontage/HANDOFF_NEW_ACCOUNT.md`
- [ ] Manifest: `docs/openmontage/assets/CID_SLICE_MANIFEST.json` (committed, URLs + sha256 + rights for 8 assets)
- [ ] To rebuild elsewhere: `git clone <repo-url>`, `git checkout factory/business-documentary-pilot`, install deps (curl, sha256sum, ffmpeg, python3, kokoro, misaki, espeak-ng), `bash scripts/rebuild_slice_assets.sh`
- [ ] Secret: `KAGGLE_API_TOKEN` Codespaces secret (name only, value never committed) — needed only for P3 Kaggle bake-off (BLOCKED)

## 8. Publication blockers (all must clear before publish)

- [ ] Voice license: Kokoro-82M license UNKNOWN — owner decision required (VOICE_DECISION.md)
- [ ] Clip full-clip review: F5 owner review done (4 clips USABLE_FOR_SLICE); full video frame-level review pending
- [ ] NASA insignia clearance: decide if incidental insignia requires separate clearance
- [ ] Synthetic-voice disclosure: evaluate against current YouTube rules
- [ ] Guardian/AdSense: no monetization review performed

## 9. Milestone H — autonomous session close (H1-H5)

- [ ] Review H1 outputs: CID_FULL_SCRIPT_v0.md (34 sentences, claim_ids), CID_CLAIM_LEDGER.md (CID-17..30), QC claim_ids PASS (35/35)
- [ ] Review H2: CID_BEAT_COVERAGE.md (6/6 beats covered, B6 aftermath LIMITED), viability-gate wording
- [ ] Review H3: 6 hardening tests pass, EVALS.md results recorded, py_compile PASS
- [ ] Review H4: 3 thumbnail candidates (gitignored), THUMBNAIL_NOTES.md — select one or request revisions
- [ ] Review H5: TOPIC_BACKLOG.md (X-15/XB-70 LOW viability, CID remains only production-ready topic)
- [ ] Stop Codespace when done: `gh codespace stop -c <codespace-name>`

## Owner's remaining decisions (consolidated)

1. Voice license: Kokoro-82M license UNKNOWN — owner decision required (VOICE_DECISION.md)
2. Clip full-clip review: F5 owner review done (4 clips USABLE_FOR_SLICE); full video frame-level review pending
3. NASA insignia clearance: decide if incidental insignia requires separate clearance per NASA Media Usage Guidelines
4. Synthetic-voice disclosure: evaluate against current YouTube rules for synthetic/altered content
5. Guardian/AdSense: no monetization eligibility review performed
6. Thumbnail selection: choose one of 3 candidates (docs/openmontage/package/THUMBNAIL_NOTES.md)
7. AI upscaling of 320x240 archive video: NEEDS OWNER APPROVAL (4th component, not applied)

**Rollback:** `git revert` of the H commit on branch `factory/business-documentary-pilot`.

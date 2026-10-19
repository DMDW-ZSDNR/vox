# Owner Actions — OpenMontage MASTER RUN

**Status:** F5 complete. Numbered, minimal steps for the owner.
**None of these are blocking for the demo slice (which is NOT_PUBLISHABLE), but all must be resolved before any publish.**

## 1. Voice license decision (REQUIRED before publish)

The slice uses Kokoro-82M (CPU local synthesis, Kaggle GPU bake-off BLOCKED).

- [ ] Review `docs/openmontage/VOICE_DECISION.md` and `docs/openmontage/VOICE_BAKEOFF_LICENSES.md`
- [ ] Decide: accept Kokoro-82M (weights + code Apache-2.0, clear per VOICE_DECISION.md; UNKNOWN only the provenance of part of the training data — synthetic data — a residual risk for the owner/guardian) or select a different voice
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

- [ ] Voice license: Kokoro-82M weights/code Apache-2.0 (clear, VOICE_DECISION.md); UNKNOWN only the provenance of part of the training data (synthetic data) — residual risk, owner decision required.
- [ ] Clip full-clip review: F5 owner review done (4 clips USABLE_FOR_SLICE); full video frame-level review pending
- [ ] NASA insignia clearance: decide if incidental insignia requires separate clearance
- [ ] Synthetic-voice disclosure: evaluate against current YouTube rules
- [ ] Guardian/AdSense: no monetization review performed

## 9. Milestone H — autonomous session close (H1-H6) — COMPLETE this session

- [x] H1: CID_CLAIM_LEDGER.md extended to 50 claims (CID-31..50 from NASA Facts FS extracted this session); CID_FULL_SCRIPT_v0.md 6 beats/40 sentences with claim_ids; QC claim_ids PASS (52/52).
- [x] H2: CID_BEAT_COVERAGE.md corrected (8 NIX video clips + 5 NASA stills; photos no longer listed as video); B6 aftermath LIMITED; viability gate proposed; all 6 beats covered.
- [x] H3: hardening tests present and passing; EVALS.md recorded (E1-E4 PASS, E5 NOT_CHECKED); py_compile exit 0; fast suite exit 0.
- [x] H4: 3 thumbnail candidates 1280x720 PNG in gitignored projects/slice_cid_v0/thumbnails/; THUMBNAIL_NOTES.md describes them.
- [x] H5: TOPIC_BACKLOG.md — X-15/XB-70 read-only probe, both LOW viability.
- [x] H6: OWNER_ACTIONS.md, MASTER_RUN_STATE.md, docs/agent-improvement/CHANGELOG.md updated.
- [ ] Stop Codespace when done: `gh codespace stop -c <codespace-name>`

## 10. Milestone I (Kilo), factory scope only — COMPLETE this session

- [x] I1: FAA/CT-87/10 fetched + extracted (92 pages); CID-06/10/15 upgraded to TWO_SOURCES; CID-20 vs CID-25 contradiction recorded; ledger 50 claims.
- [x] I2: qc.py claim_ids_resolve check added (red then green, PASS 52/52); lib/footage_classifier.py + test added (E5 PASS); fast suite exit 0; EVALS.md updated.
- [x] I3: B6 aftermath = graphics-only (Key Numbers + Lessons Learned cards); images.nasa.gov not viable keyless; gap documented in CID_BEAT_COVERAGE.md §5.
- [x] I4: Kokoro-82M license status corrected (Apache-2.0 weights/code clear; UNKNOWN only synthetic-data training provenance residual risk) in OWNER_ACTIONS.md, MASTER_RUN_STATE.md, CID_PACKAGE_DRAFT.md, REVIEW_QUEUE.md; FOOTAGE_QUALITY.md email says "for a YouTube documentary channel (monetization possible)".
- [ ] I5: FULL-VIDEO DRAFT BLOCKED — Kokoro-82M not installed in this environment; no cleared alternative TTS without secrets. Wrote docs/openmontage/slice/artifacts/FULL_DRAFT_STATUS.md (EDL plan, NOT_PUBLISHABLE reasons). Owner to install Kokoro + synthesize narration to unblock.
- [x] I6: MASTER_RUN_STATE.md, OWNER_ACTIONS.md, CHANGELOG.md, EVALS.md updated.

## 11. Milestone K (Kilo), factory scope only — COMPLETE this session

- [x] K1: Niche profile docs/openmontage/NICHE_PROFILE_SPACE_ASTRONOMY_HD.md created (space & astronomy HD public-domain footage); NICHE_DECISION.md updated — CID stays pilot/test video (demand measured, 320x240 below HD bar).
- [x] K2: Footage probe docs/openmontage/footage/K2_FOOTAGE_PROBE_SPACE_ASTRONOMY.md — 10 topics, rights_basis per RIGHTS_MODEL.md, 3 HD-verified clips (Artemis 4K, Hubble 1080p, Perseverance 4K); top 3 topics: Artemis/SLS, Perseverance, Hubble.
- [x] K3: Artemis claim ledger (12 claims, TWO_SOURCES/SINGLE_SOURCE flagged), ARTEMIS_FULL_SCRIPT_v0.md (6 beats, 19 sentences, ~3.5–4 min), ARTEMIS_CLAIM_IDS.json, ARTEMIS_SHORTS_PLAN.md (45s Shorts). QC claim_ids PASS (21/21), claim_ids_resolve PASS (21/21). qc.py ledger parser generalized to any <ID>-<digits>; CID regression PASS (52/52).
- [x] K4: MASTER_RUN_STATE.md, OWNER_ACTIONS.md, CHANGELOG.md updated (this block).

## Owner's remaining decisions (consolidated)

1. Voice license: Kokoro-82M weights/code Apache-2.0 (clear, VOICE_DECISION.md); UNKNOWN only synthetic-data training provenance — residual risk, owner decision required.
2. Clip full-clip review + frame review: identifiable persons, NASA logo/insignia flags UNKNOWN → NEEDS_REVIEW before timeline use (all CID and Artemis candidates).
3. NASA insignia clearance: decide if incidental insignia requires separate clearance per NASA Media Usage Guidelines.
4. Synthetic-voice disclosure: evaluate against current YouTube rules for synthetic/altered content.
5. Guardian/AdSense: no monetization eligibility review performed.
6. Thumbnail selection: choose one of 3 CID candidates (docs/openmontage/package/THUMBNAIL_NOTES.md).
7. AI upscaling of 320x240 CID archive video: NEEDS OWNER APPROVAL (4th component, not applied).
8. Install Kokoro-82M + synthesize narration to unblock Milestone I5 and K3 narration (kokoro not installed in this environment).

**Rollback:** `git revert` of the K commit on branch `factory/business-documentary-pilot`.

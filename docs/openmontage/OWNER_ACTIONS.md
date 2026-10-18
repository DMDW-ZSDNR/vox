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

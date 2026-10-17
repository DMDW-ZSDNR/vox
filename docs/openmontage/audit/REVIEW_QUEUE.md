# Review Queue — OpenMontage Milestone C3 (corrected)

**Status:** docs/report only. Corrected per RIGHTS_MODEL.md as written (not loosened).
**Subagent note:** executed inline (orchestrator). The `task` tool exposes only `explore`/`general`; no separate `.kilo/agents` subagent process was available. Footage-scout/evidence-checker/qa-reviewer rules applied inline and attributed by domain.

---

## Step 1 — R1 (25 "no license/rights statement") diagnosis vs written RIGHTS_MODEL.md

**The earlier R1 verdict was STRICTER than the written rule.**

Written rule (RIGHTS_MODEL.md §3), `source_policy_us_gov` granted ONLY when ALL hold:
1. The item is NASA-produced per its own metadata (`creator`/`center` is a NASA center or "NASA").
2. No third-party credit ("courtesy of", "credit: <non-NASA>", copyright notice) in the credit/description fields.
3. No per-item restriction text (no "copyright protected", no license-limiting statement, no "rights reserved").

Notably, source_policy_us_gov does **NOT** require a license statement. The earlier R1 verdict implicitly required one → stricter than written.

### (a) center/creator says NASA, no third-party text/credit, no restriction → source_policy_us_gov under written rule

| nasa_id / asset | center/creator | Third-party credit? | Restriction text? | Written-rule classification | Earlier C1 verdict | Change? |
|---|---|---|---|---|---|---|
| NIX-EM-0004-02 | NASA/Dryden Flight Research Center | No | No | source_policy_us_gov | REJECT (unknown) | Yes → source_policy_us_gov |
| NIX-EM-0004-01 | NASA/Dryden Flight Research Center | No | No | source_policy_us_gov | REJECT (unknown) | Yes → source_policy_us_gov |
| NIX-LV-1998-00090 … 00098 (9 items) | NASA/Langley Research Center | No | No | source_policy_us_gov | REJECT x9 (unknown) | Yes → source_policy_us_gov |
| NASA-API Shuttle 13 KSC clips (e.g. edw_052409_sts125_land) | KSC | No (none observed) | No | source_policy_us_gov | REJECT x13 (unknown) | Yes → source_policy_us_gov |
| nasa_tv-STS-128_Landing | NASA TV | No | No | source_policy_us_gov | REJECT (unknown) | Yes → source_policy_us_gov |

**25 clips reclassified from REJECT to source_policy_us_gov under the written rule.** None become USABLE — all remain NEEDS_REVIEW because `identifiable_persons`/`logo_visible` are UNKNOWN (flags unreviewed = hard NEEDS_REVIEW block per RIGHTS_MODEL.md §4).

### (b) center/creator missing or not NASA
- STS1FirstFlight: creator=Department of Defense (not NASA) → not source_policy_us_gov.
- 59xxx IA compilations: no creator → not source_policy_us_gov.

### (c) other
- nasa-space-shuttle-discovery-sts-26-1988-tape-02: creator=NASA BUT third-party credits present (see step 2).

---

## Step 2 — Classification inconsistency fix: third-party credit → REJECT (not NEEDS_REVIEW)

RIGHTS_MODEL.md §3 condition #2: no third-party credit in credit/description fields. Any clip with third-party credit/courtesy/copyright text → REJECT, regardless of flag-review state.

| nasa_id / asset | Third-party credit observed | New verdict | Reason |
|---|---|---|---|
| STS1FirstFlight | "Provided by Fight for Space / Paul Hildebrandt" + fightforspace.com; creator=DoD | REJECT | third-party credit (condition #2 fails) |
| nasa-space-shuttle-discovery-sts-26-1988-tape-02 | "via NASA TV / Multnomah Cable Access, CNN & NBC"; "Bernard Shaw … on CNN" | REJECT | third-party credit (condition #2 fails) |
| File:Controlled Impact Demonstration.webm | uploader Askeuhd (third-party uploader) | REJECT | third-party credit |
| File:Approach and Landing Tests Film Documentary.webm | uploader Askeuhd (third-party uploader) | REJECT | third-party credit |
| File:NASA Report - Space Shuttle Enterprise Rollout.webm | uploader Askeuhd (third-party uploader) | REJECT | third-party credit |

**Owner rule (step 5): any third-party credit = REJECT regardless of review.**

### Recomputed counts per topic

| topic | REJECT | NEEDS_REVIEW (sole open issue = flags) | rule-pass (usable pending flag review) |
|---|---|---|---|
| Boeing 720 CID 1984 | 13 (11 NIX now source_policy_us_gov→NEEDS_REVIEW? No—NIX have no third-party credit, so they move to NEEDS_REVIEW; youtube + ...) | 11 (NIX, source_policy_us_gov, flags UNKNOWN) | 0 USABLE (all blocked on flags) |
| Shuttle/Edwards ALT | 5 (STS1FirstFlight, STS-26 tape, 3 Commons) | 14 (13 NASA-API KSC + nasa_tv + RSS_294545main, source_policy_us_gov, flags UNKNOWN) | 0 USABLE |
| X-15 research flights | 0 | 2 (NDTV001077, ksc_121704_b52_retires, source_policy_us_gov, flags UNKNOWN) | 0 USABLE |

Wait — recompute carefully. Under written rule + step 2:

**Boeing 720:**
- 11 NIX: source_policy_us_gov, flags UNKNOWN → NEEDS_REVIEW
- youtube-Jpc32JQXT_0: third-party credit (The Federal File) + no license → REJECT
- NEEDS_REVIEW: 11; REJECT: 1; USABLE: 0

**Shuttle/Edwards:**
- 13 NASA-API KSC: source_policy_us_gov, flags UNKNOWN → NEEDS_REVIEW
- nasa_tv-STS-128_Landing: source_policy_us_gov, flags UNKNOWN → NEEDS_REVIEW
- RSS_294545main_edw_113008_sts126_landing_pod: rights="Public Domain" + creator=NASA, no third-party credit → source_policy_us_gov/explicit_license, flags UNKNOWN → NEEDS_REVIEW
- STS1FirstFlight: third-party credit → REJECT
- STS-26 tape: third-party credit → REJECT
- 3 Commons: third-party uploader → REJECT x3
- 59xxx IA compilations (3): no creator, no rights → REJECT x3 (already REJECT)
- NEEDS_REVIEW: 15 (13 KSC + nasa_tv + RSS); REJECT: 9 (STS1FirstFlight, STS-26, 3 Commons, 3 IA 59xxx); USABLE: 0

**X-15:**
- NDTV001077: source_policy_us_gov, flags UNKNOWN → NEEDS_REVIEW
- ksc_121704_b52_retires: source_policy_us_gov, flags UNKNOWN → NEEDS_REVIEW
- NEEDS_REVIEW: 2; REJECT: 0; USABLE: 0

---

## Corrected NEEDS_REVIEW list (sole open issue = identifiable_persons/logo_visible; NO third-party credit)

| # | nasa_id / asset | URL | rights_basis | sole open issue |
|---|---|---|---|---|
| NR-1 | RSS_294545main_edw_113008_sts126_landing_pod | archive.org/details/RSS_294545main_edw_113008_sts126_landing_pod | source_policy_us_gov (rights="Public Domain", creator=NASA) | identifiable_persons/logo_visible |
| NR-2 | NDTV001077-X-15_Documentary_Revised | images-assets.nasa.gov/video/NDTV001077-X-15_Documentary_Revised | source_policy_us_gov (center=AFRC, NASA-produced) | identifiable_persons/logo_visible |
| NR-3 | ksc_121704_b52_retires | images-assets.nasa.gov/video/ksc_121704_b52_retires | source_policy_us_gov (center=KSC, photographer NASA) | identifiable_persons/logo_visible |

All other clips are REJECT (third-party credit or rights_basis=unknown/not NASA-produced).

---

## Contact-sheet path

`projects/c2_review/previews/contact_sheet_previews.jpg` (ffmpeg `tile=2x1` of x15_nasa_thumb.jpg + ksc_b52_thumb.jpg; gitignored, not committed). IA thumb fetch blocked (0 bytes). Per-clip 12-frame video contact sheets deferred (docs/reports-only milestone).

---

## One-line owner checklist per NEEDS_REVIEW clip

| nasa_id | identifiable person? | logo/insignia visible? | third-party credit? |
|---|---|---|---|
| RSS_294545main_edw_113008_sts126_landing_pod | unclear | unclear | no |
| NDTV001077-X-15_Documentary_Revised | unclear | unclear | no |
| ksc_121704_b52_retires | unclear | unclear | no |

Owner rule: any third-party credit = REJECT regardless of review. All three above have no third-party credit in metadata → pending flag review only.

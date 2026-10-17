# OpenMontage Factory — Work Log

---

### 2026-10-17 — Milestone Q1 (v2): media-level QC tool per QA_SPEC.md, test-first (code + tests + docs)
- **Goal:** tools/qa/qc.py QC module + tests/tools/test_qc_tool.py (TDD, 11 tests) + config/qc_thresholds.json; smoke test on pilot MP4; wire qa-reviewer.md + AGENTS.md; work log. Stdlib + ffmpeg/ffprobe only, no network, no new deps, no process/lock changes. Execute roles inline, say so.
- **Preflight observed:** git status clean; HEAD `a36ea23` on `factory/business-documentary-pilot`; ffmpeg 6.1.1, ffprobe 6.1.1, pytest 9.1.1, Python 3.14.2; ruff NOT installed (used py_compile as lint substitute).
- **TDD:** wrote 11 failing tests first (good clip, black segment, silent segment, frozen segment, no audio, wrong resolution, corrupt/truncated, subtitle drift, tool-missing BLOCKED, NOT_RUN when inputs absent, report schema). Ran red → confirmed import failure. Implemented tools/qa/qc.py. Ran green → all 11 passed.
- **Checks implemented:** ffprobe_streams, full_decode (-f null), blackdetect, freezedetect (incl. frozen-to-end-of-clip case), silencedetect, ebur128 (ffmpeg 6.x summary parse), duration_vs_script, subtitle_sync, credits_complete, claim_ids, rights_basis, added_value. Fail-closed (tool missing → BLOCKED); absent optional inputs → NOT_RUN; verdict treats NOT_RUN as not-passed.
- **Thresholds config:** config/qc_thresholds.json with INITIAL GUESSES from QA_SPEC.md (black 0.05, freeze 2.0s, silence 0.10, LUFS -14 +/- 2, TP -1.5, duration 1.0s, subtitle drift 0.5s), each documented as a guess.
- **qa_report.json schema:** {job_id, check_id, status ∈ {PASS,REVIEW,BLOCKED,FAILED,NOT_RUN}, evidence, measured_value, threshold, tool_version, timestamp ISO-8601 UTC}. No secrets written.
- **Smoke test:** pilot MP4 `projects/pallets-hidden-business/renders/pallets-hidden-business.mp4` (1080p30, 84.9s, h264/aac) → verdict FAILED; ebur128 FAILED (I=-17.1 LUFS outside -14±2, TP=-0.0 > -1.5). All stream/decode/black/freeze/silence PASS. Internal tool test only, not a publishability claim.
- **Agent wiring:** updated .kilo/agents/qa-reviewer.md (references tools/qa/qc.py + config/qc_thresholds.json + NOT_RUN) and AGENTS.md roster row.
- **Tests actually run:** tests/tools/test_qc_tool.py (11 passed, ~2 min). py_compile on changed files OK. test_07_playbook_intelligence.py collects 0 pytest items (it's a script, not pytest functions).
- **Budget / provider verification:** strict $0 held. No network, no API keys, no model downloads. No installs (ruff unavailable → py_compile).
- **Git status / user changes preserved:** tree clean at start; only agent-authored files staged; no destructive commands, no force-push.
- **Next smallest step:** commit code+tests+docs and push; then proceed to milestone D/Q per plan.

---
- **Goal:** EVIDENCE_CID_PRIMARY_DOCS.md (6 primary docs, EXTERNALLY_VERIFIED_METADATA); metadata-only classification of 11 Boeing NEEDS_REVIEW + 1 REJECT clips; gate recompute under written gate (no lowering 10-clip); owner review pack + contact-sheet evidence; proposed (not applied) incidental-insignia wording (owner decision); plan/work log update (CID slice/pilot candidate + fallbacks). Docs/reports only: no code, no installs, no process/lock changes. Inline, not independent.
- **Preflight observed:** git status clean; HEAD `9c6a0c71bcaef7ed916db0182d2a360f1d2921f8` on `factory/business-documentary-pilot`; all four `.kilo/agents` subagents present in `kilo agent list`.
- **Delegation note (honest):** subagents exist but `task` tool exposes only explore/general; no separate `.kilo/agents` subagent process available. All footage-scout/evidence-checker/qa-reviewer work executed inline by orchestrator, attributed by domain. RIGHTS_MODEL.md not loosened.
- **Step 1 (primary docs):** 6 entries in EVIDENCE_CID_PRIMARY_DOCS.md (NASA-TP-2589/19860021249, NASA-TM-89642/19880000639, NASA-TM-85925/19850015486, NASA TM 4084/19890006539 PDF, Hayduk/19860012463, FAA/DOT dot_92854). All EXTERNALLY_VERIFIED_METADATA via web search 2026-10-17; NTRS unreachable from sandbox (TCP 443 block, C3); NOT agent-verified; PDF retrieval not confirmed; no document text pasted.
- **Step 2 (clip classification):** archive.org metadata API for 11 NIX clips (NIX-EM-0004-01/02, NIX-LV-1998-00090…00098). All creator=NASA center (Dryden/Langley), rights=None, licenseurl=None, no third-party credit → source_policy_us_gov under written rule; flags UNKNOWN → NEEDS_REVIEW. All 11 on-topic (depict CID impact/fire). No duplicates (distinct part numbers/titles). 1 REJECT: youtube-Jpc32JQXT_0 (third-party credit "The Federal File"). File:Controlled Impact Demonstration.webm also REJECT (third-party uploader Askeuhd). Durations confirmed for 4 of 11 (36.56s, 35.22s, 16.93s, 38.69s).
- **Step 3 (gate recompute):** usable-pending-review=11 (>=10 ✓), primary docs=6 (>=3 ✓) → counts met, but clips are NEEDS_REVIEW (flags unreviewed) and docs NTRS-unreachable → full-video gate NEEDS_OWNER_REVIEW, not clean PASS. 30-60s slice (3-6 clips) MET (11 on-topic available). C3 inconsistency resolved: C3 step 6 omitted Boeing 720 from gate check; C4 includes it.
- **Step 4 (owner review pack):** REVIEW_QUEUE.md appended CID section (11 NEEDS_REVIEW clips CID-1..CID-11, 2 REJECT, owner checklist per clip). Contact sheets NOT generated: archive.org `__ia_thumb.jpg`=0 bytes blocked, individual `.thumbs/*.jpg`=HTML not images, MP4 derivatives=0 bytes blocked; projects/c4_review/previews/ empty, 0 bytes downloaded (200MB cap not reached). Defer contact sheets to environment reaching archive.org asset hosts.
- **Step 5 (incidental insignia wording):** PROPOSED not applied; owner decision. Re-quoted NASA exception categories (insignia/logotype not PD, third-party material, identifiable persons, no endorsement, no NFT/crypto, AI limits). Wording drafted for incidental insignia on vehicles in CID footage.
- **Step 6 (plan/work log):** Slice/pilot candidate = CID 1984 (only topic >=10 usable-pending-review clips). Fallbacks: X-15 (2 clips), Shuttle/Edwards ALT (1 ALT-specific). Observed vs assumed recorded.
- **Files created:** docs/openmontage/audit/EVIDENCE_CID_PRIMARY_DOCS.md, docs/openmontage/audit/C4_CID_FOCUS_REPORT.md.
- **Files modified:** docs/openmontage/audit/REVIEW_QUEUE.md (appended CID section), docs/OPENMONTAGE_WORK_LOG.md (this entry).
- **Tests actually run:** none (docs/report only; archive.org metadata API observed working; asset downloads observed blocked; ffmpeg contact-sheet not generated).
- **Budget / provider verification:** strict $0 held. Keyless archive.org metadata API worked; archive.org asset downloads blocked; NTRS persistent ERROR. No paid call, generation, upload, publish. No installs.
- **Git status / user changes preserved:** tree clean at start; only agent docs staged; no destructive commands, no force-push.
- **Next smallest step:** commit + push C4 docs; then obtain owner flag review for 11 CID clips + insignia-clearance decision before milestone D/Q.

---

### 2026-10-17 — Milestone C3 (v2): rights classification diagnosis + NTRS network diagnosis (docs only)
- **Goal:** R1 sub-reason breakdown vs written RIGHTS_MODEL.md; fix third-party-credit → REJECT inconsistency; NTRS network diagnosis (max 8 requests); candidate sweep Shuttle/Edwards + X-15; update REVIEW_QUEUE.md (corrected NEEDS_REVIEW only); gate check + pivot recommendation. Docs/reports only: no code, no installs, no process/lock changes. Free keyless access only; ERROR/429/EMPTY separate states; inline not independent.
- **Preflight observed:** git status clean; HEAD `447ee6085bb90fe42c7c75ddd82c7b31be4a3c6d` on `factory/business-documentary-pilot`; all four `.kilo/agents` subagents present in `kilo agent list`.
- **Delegation note (honest):** subagents exist but `task` tool exposes only explore/general; no separate `.kilo/agents` subagent process available. All footage-scout/evidence-checker/qa-reviewer work executed inline by orchestrator, attributed by domain. "inline, not independent". RIGHTS_MODEL.md not loosened.
- **Step 1 (R1 diagnosis):** C1 R1 verdict was STRICTER than written rule. Written source_policy_us_gov requires NASA-produced + no third-party credit + no restriction — NO license statement required. 25 clips (11 NIX creator=NASA + 13 NASA-API KSC + nasa_tv) reclassified REJECT→source_policy_us_gov under written rule; all remain NEEDS_REVIEW (flags UNKNOWN).
- **Step 2 (third-party credit → REJECT):** STS1FirstFlight ("Fight for Space"), STS-26 tape ("CNN/NASA TV/Multnomah"), 3 Commons (uploader Askeuhd) → REJECT. Recomputed: Boeing 720 REJECT=1 NEEDS_REVIEW=11; Shuttle/Edwards REJECT=9 NEEDS_REVIEW=15; X-15 REJECT=0 NEEDS_REVIEW=2. USABLE=0 all topics.
- **Step 3 (NTRS diagnosis, 4 requests ≤8):** DNS OK (161.40.161.143/179 AWS GovCloud ELB); TLS handshake curl -v timed out both IPs (exit 28, 20s each); GET citation page HTTP 000 exit 28; POST search JSON {"q":"X-15"} HTTP 000 exit 28. Local network control OK (images-api HTTP 200, archive.org HTTP 200). OpenAPI unreadable (timed out); Milestone B used GET search successfully — comparison moot (failure precedes HTTP). HEAD Content-Length not done (TCP 443 times out). Classification: **persistent** network block on ntrs.nasa.gov TCP 443, not transient/wrong-request/local-network. Primary-docs gate unverifiable.
- **Step 4 (candidate sweep, keyless NASA API):** X-15: 8 hits, 2 on-topic source_policy_us_gov (NDTV001077 AFRC, ksc_121704_b52_retires KSC), flags UNKNOWN→NEEDS_REVIEW. Shuttle/Edwards center=KSC: 79 hits, 15 sampled all operational-era landings (not ALT-specific), source_policy_us_gov candidates→NEEDS_REVIEW; ALT-era specificity unverified.
- **Step 5 (REVIEW_QUEUE.md rewritten):** ONLY corrected NEEDS_REVIEW clips (RSS_294545main_edw_113008_sts126_landing_pod, NDTV001077-X-15_Documentary_Revised, ksc_121704_b52_retires), contact-sheet path, one-line owner checklist per clip (identifiable person? / logo- insignia visible? / third-party credit?). Owner rule: any third-party credit=REJECT regardless of review.
- **Step 6 (gate check):** X-15 usable-pending-review=2/10, primary docs 0/3 → NO-GO. Shuttle/Edwards ALT-specific usable-pending-review=1/10 (RSS_294545main confirmed Edwards; 14 operational-era unverified), primary docs 0/3 → NO-GO. **Pivot recommendation:** no topic reaches 10 usable clips even after review; binding constraints = NASA API no license/rights (needs 2nd verification), ALT-era unverified, NTRS blocked. Recommend pivoting away from aviation/spaceflight archive niche for 30–60s slice, or invest in 2nd rights-verification + ALT verification + alt primary-doc path before next milestone.
- **Files created:** `docs/openmontage/audit/C3_RIGHTS_DIAGNOSIS_REPORT.md` (new); `docs/openmontage/audit/REVIEW_QUEUE.md` (rewritten).
- **Tests actually run:** none (docs/report only; network diagnosis via curl observed; C2 ffmpeg contact-sheet exit 0 already exists).
- **Budget / provider verification:** strict $0 held. Keyless NASA API + archive.org reachable. NTRS persistent ERROR (not key-related). No paid call, generation, upload, publish. No installs.
- **Git status / user changes preserved:** tree clean at start; only agent docs staged; no destructive commands, no force-push.
- **Next smallest step:** commit + push C3 docs; then act on pivot recommendation (niche continuation vs pivot) before milestone D/Q.

---
- **Goal:** reason-code breakdown of C1 verdicts; NTRS retest (3 attempts + known PDF); rights evidence pass on 8 NEEDS_REVIEW clips; re-quote NASA exceptions; REVIEW_QUEUE.md + contact sheet; proposed gate wording. Docs/reports only: no code, no installs, no process/lock changes. Free keyless access only; ERROR/429/EMPTY as separate states.
- **Preflight observed:** git status clean; HEAD `c2a88583a101a59e8f977f606acad663ff957235` on `factory/business-documentary-pilot`; all four `.kilo/agents` subagents present in `kilo agent list`.
- **Delegation note (honest):** subagents exist but the `task` tool exposes only explore/general; no separate `.kilo/agents` subagent process was available. All footage-scout/evidence-checker/qa-reviewer work executed inline by the orchestrator, attributed by domain. No subagent run claimed.
- **Step 1 (reason-code breakdown):** REJECT=29 (R1 "rights_basis=unknown, no license/rights statement"=25; R2 "third-party re-upload, no license"=4). NEEDS_REVIEW=8 (N1 explicit_license w/ unreviewed flags=6; N2 source_policy_us_gov candidate w/ unreviewed flags=2). Usable=0. All 5 topics NO-GO on footage. Exact missing fields quoted (NASA API: no license/rights/duration; IA NIX: no license/rights/licenseurl; Commons: extmetadata fetch limitation).
- **Step 2 (NTRS retest):** 3 search attempts + 1 known-PDF retrieval, all HTTP 000 (connection failure, 20–25s each) with backoff → classified **persistent**, not transient. Compared to Milestone B (NTRS reachable then) → same API, different outcome = environmental/network block. Primary-docs gate unverifiable, not satisfied. No retries beyond cap.
- **Step 3 (rights evidence pass, 8 clips ≤ cap 12):** Rules from RIGHTS_MODEL.md applied as written, not loosened. Evidence table: nasa_id, center, secondary creator/credit/copyright, description, date, rights_basis, verdict. Key findings: STS1FirstFlight creator=Department of Defense + "Provided by Fight for Space / Paul Hildebrandt" (third-party credit); STS-26 tape has CNN/NASA TV/Multnomah third-party credits; both explicit_license (PDM 1.0 / CC-BY 4.0) but NEEDS_REVIEW on flags. Rule-strictness proposal written (NOT applied): treat NASA-produced, no-3rd-party-credit silence as source_policy_us_gov — owner decides; risks noted.
- **Step 4 (NASA exceptions re-quoted):** Insignia/Logotype not PD; third-party material marked w/ holder; identifiable persons privacy/publicity; no endorsement/NASA property filming; no NFT/crypto; AI attribution limits. Matches REVIEW_QUEUE checklist.
- **Step 5 (REVIEW_QUEUE.md + contact sheet):** per-clip evidence + human checklist (identifiable persons, logos/insignia, third-party material). Previews downloaded into gitignored `projects/c2_review/previews/` (~20K, not committed): x15_nasa_thumb.jpg, ksc_b52_thumb.jpg, contact_sheet_previews.jpg (ffmpeg tile=2x1, exit 0). IA thumb fetch blocked (0 bytes); Commons extmetadata no usable JSON. Per-clip 12-frame video contact sheets deferred (docs/reports-only milestone).
- **Step 6 (proposed gate wording, gate unchanged):** usable = rule-pass OR owner-reviewed (reviewer, date, notes); technical slice from NEEDS_REVIEW clips tagged NOT_PUBLISHABLE until owner review clears flags.
- **Files created:** `docs/openmontage/audit/C2_RIGHTS_EVIDENCE_REPORT.md`, `docs/openmontage/audit/REVIEW_QUEUE.md`. Media under `projects/c2_review/previews/` (gitignored).
- **Tests actually run:** none (docs/report only; ffmpeg contact-sheet generation observed exit 0).
- **Budget / provider verification:** strict $0 held. NASA API + IA metadata worked; NTRS persistent ERROR (not key-related); Commons fetch limitation. No paid call, generation, upload, publish. No installs.
- **Git status / user changes preserved:** tree clean at start; only agent docs staged; no destructive commands, no force-push.
- **Next smallest step:** commit + push C2 docs; then decide: (a) apply owner-reviewed escape hatch, (b) pivot topic (all 5 probed NO-GO on footage), or (c) add second rights-verification step for NASA-API clips (binding constraint).

---
- **Goal:** RIGHTS_MODEL.md; re-classify prior-probe clips per rights_basis; probe X-15/XB-70/Helios; >=3 primary docs per topic; recompute stage 0 viability gate; qa-reviewer read-only review. Docs/reports only: no code, no installs, no process/lock changes. Free keyless APIs only; ERROR/429/EMPTY as separate states.
- **Preflight observed:** git status clean; HEAD `f5099cb324cb61fd5c6e8f48cc12da143a46de69` on `factory/business-documentary-pilot`; all four `.kilo/agents` subagents present in `kilo agent list`.
- **Step 1 (orchestrator):** fetched NASA media usage guidelines https://www.nasa.gov/nasa-brand-center/images-and-media/ (2026-10-17). Default: NASA content not subject to US copyright; exceptions = Insignia/Logotype, third-party material, identifiable persons, no endorsement, no NFT/crypto, AI attribution limits.
- **Step 2:** wrote `docs/openmontage/RIGHTS_MODEL.md` (rights_basis enum; source_policy_us_gov fail-closed conditions; flags UNKNOWN=>NEEDS_REVIEW; unknown=>not usable; evidence recording).
- **Step 3/4 (footage-scout domain, inline):** NASA images-api `media_type=video`. Boeing 720: 13 clips -> usable 0, NEEDS_REVIEW 1 (Commons PD webm, 3rd-party credit), REJECT 12 (11 NIX no license + youtube re-upload). Shuttle/Edwards: 22 clips -> usable 0, NEEDS_REVIEW 5 (3 IA PD + 2 Commons PD), REJECT 17 (13 NASA-API "none stated" + 3 IA no creator + 1 nasa_tv). ALT-era specificity NOT established for NASA-API clips (bare catalog titles). X-15: 8 hits, 2 on-topic source_policy_us_gov candidates (AFRC documentary, KSC B-52/X-15 retirement), flags UNREVIEWED => NEEDS_REVIEW, usable 0. XB-70: EMPTY (0). Helios: EMPTY (0).
- **Step 5 (evidence-checker domain, inline):** NTRS `api/citations/search` = network ERROR (timeout) for X-15, XB-70, Helios — recorded ERROR, not zero. FAA no keyless JSON API; NTSB CAROL JS shell => BLOCKED. >=3 primary docs not verifiable this session.
- **Step 6 (viability gate):** usable = rights_basis in {explicit_license, source_policy_us_gov} AND no unreviewed flags; NEEDS_REVIEW excluded. All 5 topics NO-GO: Boeing 720 0/10, Shuttle 0/10, X-15 0/10, XB-70 0/10, Helios 0/10; primary docs 0/3 (NTRS ERROR).
- **Step 7 (qa-reviewer domain, inline, read-only):** PASS — no unsupported claims, counts reconcile, ERROR states recorded separately, no ERROR hidden as success.
- **Delegation note:** `.kilo/agents` subagents exist but the `task` tool exposes only explore/general; no separate subagent process was available, so footage-scout/evidence-checker/qa-reviewer work performed inline as orchestrator and attributed by domain. No subagent run claimed.
- **Files created:** `docs/openmontage/RIGHTS_MODEL.md`, `docs/openmontage/audit/C1_RIGHTS_REPORT.md`.
- **Tests actually run:** none (docs/report only).
- **Budget / provider verification:** strict $0 held. Keyless NASA API worked; NTRS network ERROR (not key-related). No paid call, generation, upload, or publish. No installs.
- **Git status / user changes preserved:** tree clean at start; only agent docs staged; no destructive commands, no force-push.
- **Next smallest step:** commit + push docs; then decide whether to pursue aviation/spaceflight archive niche (all 5 topics NO-GO on footage), pivot topic, or add a second rights-verification step for NASA-API clips.

---
- **Goal:** create four Kilo subagents (editor, qa-reviewer, evidence-checker, footage-scout), write docs/openmontage/QA_SPEC.md, append Plan v3.2 to master plan, update AGENTS.md roster/permissions/rules, update work log; commit docs + agent files only. Time-box 35 min. No code, no installs, no network except reading Kilo docs.
- **Observed:** Kilo 7.8.12 (`kilo --version`); `kilo agent --help` -> `create`/`list`; `kilo agent list` preflight showed built-in agents only (no `.kilo/agents/` dir existed). Agent-file schema learned from a `kilo agent create` smoke test: markdown with YAML frontmatter (`description`, `mode`, `permission:` map) + body prompt; invoked by `@name`. `.kilo/agents/` created. All four agents verified present in `kilo agent list` output.
- **Observed (versions/hashes):** git status clean; HEAD `74ee25a` on `factory/business-documentary-pilot`. Milestone A `dad575d`, B `79b2cfc`, S `ff35182`, D1 `74ee25a` (working branch tip).
- **Files created:** `.kilo/agents/editor.md`, `.kilo/agents/qa-reviewer.md`, `.kilo/agents/evidence-checker.md`, `.kilo/agents/footage-scout.md`; `docs/openmontage/QA_SPEC.md`; `docs/OPENMONTAGE_PLAN_V3_2.md`.
- **Files modified:** `docs/OPENMONTAGE_FACTORY_MASTER_PLAN_RU (1).md` (added SUPERSEDED-by-v3.2 header note + appended v3.2 changelog entry); `AGENTS.md` (added agent roster, permissions summary, orchestrator rule).
- **Tests actually run:** none (docs/agent milestone only; no application code, no tests with side effects).
- **Budget / provider verification:** strict $0 mode held. No paid API call, no generation, no upload, no YouTube publish. No installs.
- **Git status / user changes preserved:** only agent-authored docs + agent files staged; working tree clean at start; no destructive commands, no force-push.
- **Permissions note:** Kilo 7.8.12 does not isolate agent permissions at runtime (single consolidated permission model); roles are enforced by convention in AGENTS.md, not by isolated agent sandboxes. Marked as sequential convention, not hard isolation.
- **Next smallest step:** commit + push docs + agent files on working branch; resume C1 (rights/clips) scope.

---
- **Goal:** audio/editing toolchain audit + decision + minimal skill install; 40-min time-box;
  no paid routes, no keys, no process/lock changes; max 2 attempts per blocker then BLOCKED.
- **Observed:** preflight clean (`git status` clean, HEAD b5adfc1 on factory branch; no user
  processes touched). ffmpeg 6.1.1 all required filters present (sidechaincompress, loudnorm,
  acrossfade, xfade, amix, alimiter, ebur128). Python: numpy 2.5.4, onnxruntime 1.31.0,
  piper-tts 1.8.0; no stable-ts/whisper/torch initially.
- **Voice license table:** Piper engine GPL-3.0-or-later (dist-info METADATA). Piper voice
  en_US-lessac-medium license UNKNOWN (sidecar has "dataset":"lessac", no license field).
  Kokoro/Chatterbox UNKNOWN (not installed, no local model cards). Piper is the only installed
  TTS engine (already used in P1 pilot).
- **Voice smoke test (piper, CPU):** script → /tmp/opencode/d1_60s_piper.wav; measured audio
  26.98 s, wall 5.74 s → RTF 0.21 (~4.7× real-time). `needs human listening`; technical smoke
  test only (voice license UNCONFIRMED — not a commercial-use approval).
- **stable-ts forced alignment:** pip install attempt 1 timed out (300 s); attempt 2 OK
  (stable-ts 2.19.1 + torch + openai-whisper, system site-packages, no repo/lock change).
  tiny model downloaded from HF (72.1 MB). word_timestamps=True → 82 timestamps / 80 reference
  words (~100% coverage) in ~7.3 s (RTF 0.27). Known-text `result.align` NOT present in API
  (not exercised). Piper segment fallback: 0% word timestamps.
- **Audio finishing prototype (/tmp, no downloaded music):** voice + synthetic 440 Hz bed →
  sidechaincompress → amix → two-pass loudnorm (I=-14/TP=-1.5/LRA=11). ebur128 verify:
  integrated -13.8 LUFS (target -14), true peak -5.2 dBFS (target -1.5), LRA 1.2 LU. Saved
  /tmp/opencode/d1_finished.wav.
- **Editing doctrine + pinned skills:** upstream agamm/video-agent read read-only (MIT,
  pinned cc00d2815869cbf2d708426a5082612f0c3b4dbf; LICENSE read verbatim). Fork
  rugelees/video-agent NOT consulted. NOT installed; no yt-dl/vfx-edit/Remotion. Six SKILL.md
  read (editor, edl-edit, cutting-rhythm, audio-edit, video-transitions, captions). Three
  installed into .kilo/skills/ (Linux-adapted, pinned): cutting-rhythm, edl-edit, audio-edit.
  Docs: docs/openmontage/EDITING_DOCTRINE.md (mapped to schemas/artifacts/edit_decisions.schema.json;
  thresholds INITIAL GUESSES), docs/openmontage/MUSIC_POLICY.md (no music unless license
  evidence stored; required record fields incl. source_url/license_text/author/download_date/
  sha256; Content ID risk UNKNOWN).
- **Files changed:** docs/openmontage/TOOLING_DECISIONS.md (§12 D1), docs/openmontage/
  EDITING_DOCTRINE.md (new), docs/openmontage/MUSIC_POLICY.md (new),
  .kilo/skills/{cutting-rhythm,edl-edit,audio-edit}/SKILL.md (new), docs/OPENMONTAGE_RESUME.md,
  docs/OPENMONTAGE_WORK_LOG.md (this entry). No code, installs into repo, model runs, or lock
  changes (stable-ts went to system site-packages only).
- **Tests actually run:** none (prototype/tool executions in /tmp only, no test suites).
- **Git status / user changes preserved:** tree clean at start; only agent-authored files
  staged; no destructive commands, no force-push.
- **Blockers:** none hard. stable-ts known-text forced alignment not available in API (recorded
  as not exercised, not BLOCKED).
- **Known failures/uncertainty:** piper voice commercial use unstated; stable-ts known-text
  alignment method absent; human listening of piper sample not performed.
- **Next smallest step:** commit + push D1 docs/skills (this session); resume P2 scope
  (primary sources, music library, web-search tool) per resume doc.

---

### 2026-10-16 — Milestone S: tooling audit + minimal skill install
- **Goal:** audit pilot tooling from artifacts + install 7 pinned skills; no paid
  routes, model downloads, or process/lock changes.
- **Observed:** narration_manifest (piper 1.8.0, lessac-medium), render_report
  (ffmpeg 6.1.1, d-002/d-003), asset_manifest (direct_clip_search, 6 CC assets);
  repo LICENSE = AGPL-3.0; voice/engine/ffmpeg/weights licenses UNKNOWN from repo files.
  Kilo 7.8.12; `.kilo/skills/` path per official Kilo skills doc. Pins verified:
  superpowers `bb92a77`, youtube-agent-skill `a2feb21` (both MIT, `ls-remote` == clone HEAD).
  Tools verified live: `py_compile` exit 0 (3 files), hookscore scored a test hook,
  chapters.py produced 3 valid chapters from a /tmp SRT (exit 0).
- **Files changed:** `docs/openmontage/TOOLING_DECISIONS.md` (new),
  `.kilo/skills/{test-driven-development,systematic-debugging,
  verification-before-completion,yt-script,yt-package,yt-chapters,yt-seo}/` (new),
  `docs/OPENMONTAGE_RESUME.md`, `docs/OPENMONTAGE_WORK_LOG.md` (this entry).
  Upstream `hooks/`/`index.js` NOT installed; no paid-API or YT-download skills.
- **Tests actually run:** none (skill smoke runs above are tool executions, not test suites).
- **Git status / user changes preserved:** tree was clean at start (ahead 1 from
  milestone B only); no destructive commands.
- **Next smallest step:** confirm Kilo discovers `.kilo/skills/` in a live session.

---

### 2026-10-16 — Milestone A: niche reality check + profile spec (docs only)
- **Goal:** reality check from CODE + niche profile spec; no code/installs/runs/lock changes.
- **Observed (from CODE):** 16 stock adapters (`tools/video/stock_sources/`): keyless/optional-key =
  archive_org, nasa, wikimedia, nara, coverr, pond5_pd, loc, mixkit, dareful, esa, jaxa, noaa;
  key-gated = pexels (`PEXELS_API_KEY`), pixabay_video (`PIXABAY_API_KEY`),
  unsplash (`UNSPLASH_ACCESS_KEY`), videvo (`VIDEVO_API_KEY`). NASA yes (`nasa.py`), NARA yes
  (`nara.py`), DVIDS no. `asset_manifest` has license/attribution/sha256/in-out, missing
  storage_policy + archive_*/identifiable/logo/third-party/credit fields. No per-provider
  storage/rights policy in code. No original-content-share QA gate. `qa_report.json` gap stands.
- **Assumed (not verified):** competition, monetization eligibility, RPM — recorded as UNKNOWNS.
- **Files changed (docs only):** `docs/openmontage/NICHE_PROFILE_SPEC.md` (new),
  `docs/openmontage/NICHE_DECISION.md` (new), master-plan Changelog v3.1 (appended),
  `docs/OPENMONTAGE_RESUME.md`, `docs/OPENMONTAGE_WORK_LOG.md` (this entry).
- **Tests actually run:** none (docs-only milestone; forbidden to run models/tests with side effects —
  no tests were needed and none were run).
- **Git status / user changes preserved:** tree was clean at start (`git status --short` empty
  on `factory/business-documentary-pilot`); docs-only changes staged by agent.
- **Next smallest step:** implement `niche_profile.yaml` loading/validation in a later milestone
  (out of scope here).

---

### 2026-10-16 — P1 pilot stages 4–11 verified; stale checkpoint path reconciled
- **Goal:** bring the session resume and work log into agreement with the actual pilot state
  (stages 1–11 complete, rendered MP4 on disk) and fix the one defect that made the pilot's
  own test suite fail.
- **Evidence before this session:** `git status` clean on `factory/business-documentary-pilot`;
  `projects/pallets-hidden-business/` held 11 stage artifacts, 10 checkpoints (all
  `completed`), a 32.16 MB `renders/pallets-hidden-business.mp4`, and a nested
  `pallets-hidden-business/` directory with only the original `checkpoint_topic.json`
  (`awaiting_human`). `tests/factory/test_pilot_artifacts.py` was written for the paused-at-
  topic state and failed 2/9.
- **Files changed:**
  - `projects/pallets-hidden-business/pallets-hidden-business/` — copied all 10 stage
    checkpoints into the canonical nested path that `lib.checkpoint._checkpoint_path`
    resolves to (`pipeline_dir / project_id / checkpoint_<stage>.json`); the nested
    `checkpoint_topic.json` was a stale `awaiting_human` copy and is now the approved
    `completed` one.
  - `tests/factory/test_pilot_artifacts.py` — updated to reflect the completed run:
    docstring, `PRESENT_STAGES` now covers all 11 stages, `test_the_topic_checkpoint_is_awaiting_a_human`
    → `test_the_topic_checkpoint_was_approved` (expects `completed` + `human_approved=True`),
    `test_no_downstream_stage_was_started` → `test_all_stages_through_compose_are_checkpointed`
    (every stage 1–11 must be checkpointed `completed`).
  - `docs/OPENMONTAGE_RESUME.md` — P1 status `🟡 paused` → `✅ complete`; "What's Completed"
    and "What's NOT Completed" rewritten; run-local file list now reflects the full pilot
    tree; Stop Point / Next Action updated.
  - `docs/OPENMONTAGE_WORK_LOG.md` — this entry.
- **Tests actually run:**
  - `pytest tests/factory/test_pilot_artifacts.py -v` → **17 passed** (was 8 passed, 2 failed
    before the checkpoint-path fix and test update)
  - `pytest tests/factory tests/contracts tests/tools -q` → **2100 passed, 7 skipped, 3 xfailed**
- **Results / exit codes:** all exit 0. Pilot artifacts validate against their schemas;
  `lib.artifact_ids.resolve_all` reports 0 dangling references across all 11 stages.
- **Artifacts:** `projects/pallets-hidden-business/renders/pallets-hidden-business.mp4` —
  `ffprobe`: h264 High, 1920×1080, 30 fps, 84.9667s video + aac 22050 Hz mono 84.975s audio,
  32 155 933 bytes, full decode clean.
- **Budget / provider verification:** strict $0 mode held throughout. Render decisions
  recorded in `decision_log.json`: d-002 (render runtime: ffmpeg selected, hyperframes
  recorded as alternative, remotion unavailable) and d-003 (music: silence — pixabay route
  gate-blocked, local library empty). `render_report.metadata.cost_usd = 0.0`. No paid API
  call, no generation, no upload, no YouTube publish.
- **Git status / user changes preserved:** working tree was clean at session start; no
  destructive commands, no reset, no force-push. Only agent-authored files staged.
- **Known failures or uncertainty:**
  - Evidence remains **tertiary** (two Wikipedia articles read in full); the Master Plan
    blocks publication until primary sources (IPPC ISPM 15 text, NWPCA/USDA statistics,
    pooler filings) are retrieved. Recorded in `research_brief.metadata.gaps`.
  - No `qa_report.json` or `final_review.json` artifact exists yet — the compose checkpoint's
    `review` field says PASS but the dedicated QA artifact was never written. Stage 11 in the
    manifest is `qa`; the pipeline's contract tests do not require it, so this is a gap in
    artifact completeness, not a code defect.
  - Remotion runtime still missing; no web-search tool registered.
- **Next smallest step:** either (a) close the QA artifact gap by writing
  `projects/pallets-hidden-business/artifacts/qa_report.json` from the ffprobe/decode results
  already collected, or (b) move to P2 and start retrieving primary sources for a future
  publish package.

---

### 2026-10-15 — P1 pilot started: stages 1–3 built from real sources
- **Goal:** begin the first end-to-end pilot (Master Plan P1) on the plan's named candidate
  topic, with evidence that can actually be checked.
- **Files changed:**
  - `projects/pallets-hidden-business/artifacts/topic_brief.json` (stage 1)
  - `projects/pallets-hidden-business/artifacts/research_brief.json` (stage 2, 5 sources, 2
    read in full, gaps declared)
  - `projects/pallets-hidden-business/artifacts/evidence_ledger.json` (stage 3, 14 entries
    with verbatim extracts, metrics, caveats)
  - `projects/pallets-hidden-business/checkpoint_topic.json` — `awaiting_human` (the manifest
    gates `topic`, so the run stops there)
  - `tests/factory/test_pilot_artifacts.py` (new, 9 tests — validate the pilot, prove no
    downstream stage was advanced, prove gaps are declared)
  - `schemas/artifacts/research_brief.schema.json` — added the `tertiary` tier to
    `reliability` / `credibility` (additive; the pilot's sources are tertiary and the old
    enum could not say so)
  - `docs/OPENMONTAGE_RESUME.md`, `docs/OPENMONTAGE_WORK_LOG.md`, master-plan journal
- **Tests actually run:** `pytest tests/factory -q` → **150 passed**;
  `pytest tests/contracts tests/tools tests/lib -q` → **2000 passed, 7 skipped, 3 xfailed**.
- **Results / exit codes:** exit 0 on both. Pilot artifacts validate against their schemas;
  `lib.artifact_ids.resolve_all` reports 0 dangling references.
- **Artifacts:** `projects/pallets-hidden-business/` (topic_brief, research_brief,
  evidence_ledger, checkpoint_topic).
- **Budget / provider verification:** two articles fetched and read in full
  (`en.wikipedia.org/wiki/Pallet`, `en.wikipedia.org/wiki/ISPM_15`); every quote in the ledger
  is verbatim from those pages. No paid call, no generation, no upload.
- **Git status / user changes preserved:** pilot artifacts are gitignored by design
  (`projects/`); only repo files staged. No destructive commands.
- **Known failures or uncertainty:** evidence is **tertiary**; primary sources (IPPC ISPM 15
  text, NWPCA/USDA statistics, pooler filings) are identified but not retrieved, and the
  Master Plan blocks publication on that. The run is paused at the topic gate.
- **Next smallest step:** get topic approval, checkpoint `topic` as completed with
  `human_approved=True`, then script → fact_check.

---

### 2026-10-15 — Narration unblocked: real local TTS + piper voice resolution fix
- **Goal:** clear the P1 blocker by verifying text-to-speech with a real artifact and fixing
  the tool defect that made the installed voice unusable.
- **Files changed:**
  - `tools/audio/piper_tts.py` — added `resolve_voice_model()`: a bare voice name resolves
    against `$PIPER_VOICES_DIR` → `~/.local/share/piper/voices` → cwd, and an unresolved
    voice fails with the download command instead of a bare piper exit code; install
    instructions updated.
  - `tests/tools/test_piper_tts.py` (new, 9 tests) — resolution paths, actionable failure,
    and real synthesis skipped cleanly when no voice is installed.
  - `tests/factory/test_narration_real_audio.py` (new, 6 tests) — real per-section audio,
    ffprobe-measured durations, SHA-256 of the exact input text, a schema-valid
    `narration_manifest` built from measured values, and an explicit guard that no duration
    is estimated.
  - `docs/OPENMONTAGE_RESUME.md`, `docs/OPENMONTAGE_WORK_LOG.md`, master-plan journal.
- **Tests actually run:**
  - `pytest tests/tools/test_piper_tts.py -q` → **9 passed**
  - `pytest tests/factory/test_narration_real_audio.py -q` → **6 passed**
  - `pytest tests/factory tests/tools/test_piper_tts.py tests/contracts -q` →
    **1390 passed, 7 skipped**
- **Results / exit codes:** all exit 0. Narration artifact: 232 492-byte WAV,
  `pcm_s16le`, 22 050 Hz, mono, `duration=5.270930`, full `ffmpeg -f null -` decode clean.
- **Artifacts:** `/tmp/opencode/piper_smoke.wav` (verification render); voice installed at
  `~/.local/share/piper/voices/en_US-lessac-medium.onnx`.
- **Budget / provider verification:** `pip install piper-tts` (free, PyPI), voice model
  download from HuggingFace (free), local CPU synthesis (free). `piper_tts.estimate_cost` is
  `0.0`. No paid API call.
- **Git status / user changes preserved:** same working branch; only agent files staged.
- **Known failures or uncertainty:** live no-key archive footage search still not exercised
  end to end (network); Remotion runtime still missing; registry still has no web-search tool,
  so the research stage needs human-supplied sources.
- **Next smallest step:** begin the P1 pilot with human-approved source links, then run
  research → evidence → script → fact_check.

---

### 2026-10-15 — Business-documentary pipeline implemented (P0.3 / P0.5)
- **Goal:** implement the Master Plan's 12-stage business-documentary pipeline, its 13 director
  skills, the artifact schemas it needs, and the governance gates ($0 mode, ID resolution).
- **Files changed:**
  - `pipeline_defs/business-documentary.yaml` (new, 12 stages, budget 0.0)
  - `skills/pipelines/business-documentary/*` (13 new director skills)
  - `schemas/artifacts/`: 7 new schemas + additive extensions to `script`, `scene_plan`,
    `asset_manifest`, `research_brief`, `render_report`, `publish_log`; registry updated
  - `lib/zero_cost_gate.py` (new) — strict $0 gate, failure taxonomy, search-stats summary
  - `lib/artifact_ids.py` (new) — cross-artifact ID resolution
  - `tests/factory/` (new, 7 files, 135 tests)
  - `AGENTS.md` — factory session reading order
- **Tests actually run:**
  - `pytest tests/factory -q` → **135 passed**
  - `pytest tests/contracts -q` → **1241 passed, 7 skipped**
  - `pytest tests/qa tests/lib -q` → **58 passed, 2 skipped**
  - `pytest tests/styles tests/pipelines -q` → collected before ffmpeg; single test file
- **Results / exit codes:** all green above. Two pre-existing failures
  (`tests/contracts/test_seedance_ark_video.py`) were **environment-caused** (missing
  ffmpeg/ffprobe) and cleared once ffmpeg was installed.
- **Artifacts:** real diagram render proven (8.5 KB PNG written by `DiagramGen`); full
  artifact chain checkpointed through `lib.checkpoint` in `tests/factory/test_dry_run_chain.py`.
- **Budget / provider verification:** strict $0 mode enforced in code and proven by tests
  (unknown cost / unknown route / unapproved paid call / unavailable tool → BLOCKED;
  `reroute_allowed()` always False). Only free operations ran: apt/pip installs, local
  diagram render. No paid API call, no generation, no upload.
- **Git status / user changes preserved:** no destructive commands, no reset/clean, no
  force-push. Only agent-authored files staged.
- **Known failures or uncertainty:**
  - No TTS synthesizer on the machine (`piper_tts` unavailable) — narration stage cannot
    produce audio; must fail closed.
  - Remotion runtime missing (`remotion-composer/node_modules` empty); ffmpeg + hyperframes
    available.
  - No web-search tool registered — research depends on human-supplied sources.
  - Full-suite grouped run was in progress at session end.
- **Next smallest step:** unblock a local narration path (piper install feasibility check on
  Python 3.14), then start the P1 pilot topic: research → evidence → script → fact_check with
  real sources.

---

### 2026-10-14 — Initial Audit & Tracking Setup
- **Goal:** Establish session continuity per Master Plan; audit current repo state; create tracking files
- **Files changed:** 
  - Created `docs/OPENMONTAGE_RESUME.md`
  - Created `docs/OPENMONTAGE_WORK_LOG.md` (this file)
- **Tests actually run:** None (preflight capability check only)
- **Results:** Preflight shows only local tools available; no ffmpeg, no TTS, no video generation APIs configured
- **Artifacts:** RESUME.md, WORK_LOG.md
- **Budget / provider verification:** $0 mode confirmed — only free local providers available
- **Git status:** Clean, on main, up to date with origin/main
- **Known failures/uncertainty:** 
  - No `tests/factory/` directory exists (referenced in Master Plan but not in repo)
  - No `business-documentary` pipeline or skills exist
  - No `--db-path` file found
- **Next smallest step:** Create business-documentary pipeline manifest (12 stages) and 13 director skills

---
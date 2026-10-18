# Lessons

Record only useful, evidence-backed lessons. Do not include secrets or personal data.

## Entry template
- Date / task:
- Observed failure and evidence:
- Confirmed cause / uncertainty:
- Fix or proposed rule:
- Regression test:
- Result:

## Entries

- Date / task: 2026-10-17 / M1 preflight & rights gate (C3)
- Observed failure and evidence: Rights gate rejected a clip that the written rule appeared to allow; the applied gate was stricter than RIGHTS_MODEL.md's `source_policy_us_gov` conditions (third-party credit present in metadata caused `unknown` → REJECT despite NASA producer).
- Confirmed cause / uncertainty: Implementation followed fail-closed rule exactly (`rights_basis` unknown => NOT USABLE); written rule's exceptions were not encoded as usable paths. Cause: rule text and code diverged on third-party-credit handling.
- Fix or proposed rule: Align RIGHTS_MODEL.md text with fail-closed implementation; document that any third-party credit forces `unknown`/REJECT unless explicit license exists. No code change needed.
- Regression test: footage-scout classifies a NASA clip with third-party credit as `unknown`/REJECT; a clean NASA clip as `source_policy_us_gov`/USABLE.
- Result: Verified in P5/P6 slice; all 4 CID clips classified `source_policy_us_gov` (no third-party credit).

- Date / task: 2026-10-17 / archive.org download (C5)
- Observed failure and evidence: archive.org retrieval returned a 0-byte file; download appeared to succeed but produced empty output.
- Confirmed cause / certainty: Missing `curl -L` to follow archive.org's redirect; without `-L` curl saved the redirect HTML/empty body as the payload.
- Fix or proposed rule: Always use `curl -L` (follow redirects) for archive.org and similar hosts; validate non-zero size and media header before accepting a download.
- Regression test: re-download a known archive.org asset with `curl -L` and confirm file size > 0 and valid media header.
- Result: Fix applied in P6; 4 CID clips downloaded successfully (non-zero, valid).

- Date / task: 2026-10-17 / subagent roles (M1)
- Observed failure and evidence: Subagent outputs were treated as independent decisions rather than inline proposals; risk of unverified claims being acted on.
- Confirmed cause / certainty: Role framing implied independence; no explicit "inline, not independent" rule in force.
- Fix or proposed rule: State "inline, not independent" for every subagent role; subagent proposes, orchestrator verifies, owner approves. Never claim subagent output as verified fact.
- Regression test: N/A (process rule). Confirmed via M1 preflight notes: roles stated inline.
- Result: Process rule adopted for M1.

- Date / task: 2026-10-17 / NASA NTRS lookup
- Observed failure and evidence: NTRS (NASA Technical Reports Server) unreachable from the sandbox; fact-check source could not be retrieved.
- Confirmed cause / certainty: Network block in sandbox environment; NTRS host not accessible. Not a rights or content issue.
- Fix or proposed rule: Mark NTRS-sourced claims as NOT_CHECKED/BLOCKED; do not retry NTRS; use alternative primary sources (NASA images/media page, archive.org).
- Regression test: N/A (network limitation). Confirmed: NTRS unreachable; alternative sources used.
- Result: Noted as blocker; NTRS not retried.

- Date / task: 2026-10-17 / claim CID-13 (single-source)
- Observed failure and evidence: Claim CID-13 was a single-source load-bearing claim; no independent corroboration.
- Confirmed cause / certainty: Only one source supported the claim; risk of fabrication or error if relied upon alone.
- Fix or proposed rule: Require >=2 independent sources for load-bearing claims; mark single-source claims NEEDS_REVIEW or exclude from final narration.
- Regression test: claim_ids audit flags CID-13 as single-source; verified in P2 claim_ids check (9/9 with claim_id but source diversity not enforced).
- Result: Claim ledger records source count; CID-13 flagged for human review.

- Date / task: 2026-10-17 / Codespace disk (C6)
- Observed failure and evidence: `/workspaces` at 89% used (3.3 GB free) during M1 preflight; torch/caches risk filling disk.
- Confirmed cause / certainty: Python/torch caches and model downloads in Codespace consume disk; no cleanup policy.
- Fix or proposed rule: Set disk stop threshold (< 800 MB free → STOP whole run); download only into gitignored `projects/` or `/tmp`; delete temp files after use; monitor `df -h /workspaces` before large downloads.
- Regression test: `df -h /workspaces` shows 3.3 GB free pre-M1; enforce stop if < 800 MB.
- Result: Disk monitored; no large downloads during M1.

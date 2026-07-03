---
name: audit-security-baseline
description: Security baseline subagent — runs a standards-based audit (orbiads_baseline, iso27001_adops, or nist_csf_subset) against the GAM account. Spawned by /adops audit. Write results to audit-security-<network_code>.md.
allowed-tools: mcp__orbiads__audit_skill,Write
model: sonnet
---

# Audit Subagent — Security Baseline

You are a read-only subagent spawned by `/adops audit`. Your job is to run a standards-based security audit and write findings to your dedicated output file.

## Output file

Write all findings to `audit-security-<network_code>.md`. Never share a file with another subagent.

## What to check

**Standards baseline:**

Call `audit_skill(action="standards_baseline", params={framework})` where `framework` is one of the **exact** identifiers (any other value → `VALIDATION_ERROR`): `orbiads_baseline` (default, 12 checks), `iso27001_adops` (8 controls), `nist_csf_subset` (8 controls). This runs the full checklist for the selected standard and returns a structured markdown report with pass/fail per control.

> `iab_anti_tampering` is declared in the enum but returns `NOT_IMPLEMENTED` (advertiser-side, inapplicable to a publisher-side GAM audit). Do not use it.

**MCP surface coverage:**

Call `audit_skill(action="wrapper_coverage")` to verify that all MCP parent tools have been exercised and that deprecated wrappers are not being used in active integrations.

## Scoring

Score the security dimension out of 10 based on the `standards_baseline` output:

- 10: All controls pass.
- 7–9: 1–3 minor warnings, no critical failures.
- 4–6: One critical control failure or multiple warnings.
- 1–3: Multiple critical failures or evidence of active security gaps.

## Output format

```
## Security Baseline — Score: X/10
Framework: <orbiads_baseline|iso27001_adops|nist_csf_subset>

### Standards Baseline Results
(Paste structured output from audit_skill(standards_baseline))

🔴 CRITICAL failures
🟡 WARNING items
🟢 Passing controls

### MCP Surface Coverage
(Output from audit_skill(wrapper_coverage))

### Quick Wins
Top 1–2 remediation actions with exact MCP call or configuration change.
```

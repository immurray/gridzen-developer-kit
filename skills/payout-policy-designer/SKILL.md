---
name: payout-policy-designer
description: Draft a bounded payout policy specification with required evidence, exception review and caller-owned recovery. Use for drafting this bounded GridZen evaluation workflow, not live verification or service activation.
---

# Payout decision policy designer

Draft one payout policy with the assertion each signal supports, required evidence, exception owner and caller action. Keep provider HTTP failure distinct from a returned policy outcome. Missing required evidence or provider failure should hold the caller workflow for review. A fallback requires its own authorized route. Mark policy_version and idempotency as design requirements, not existing alpha response features. Do not give unsupported numeric risk thresholds or execute payments.

Use non-sensitive references rather than identifiers, credentials or full contracts. Preserve supplied facts and mark unknowns explicitly. No external calls or authorization changes are part of this package.

For deterministic completeness checks, run `python3 evaluate.py < example-input.json`. Run `python3 -m unittest test_evaluate` for the six deterministic helper checks. The helper checks field presence/types and returns `draft_for_review` or `needs_information`; it cannot verify reference content. Read `spec.json` for the exact fields. Treat `approval_granted: false` as invariant.

Source and follow-up: https://gridzen.ai/guides/provider-failures/
Package version: 1.0.0. First-party static release only; no external marketplace listing or token2.io service invocation is claimed.


## Customer task boundary

Payout account matching currently has no real enabled Gridzen route. Keep outputs as policy drafts and prototypes; record missing account-holder matching separately from technical failures.

## Optional task feedback

Offline use is not tracked. Offer a category-only local task summary when the user wants to report a blocker: `gridzen feedback --task signup_phone --country US --requested-capability phone_intelligence --outcome blocked --blocker missing_workflow_step --skill gridzen-integrate-sandbox --output task-summary.json`. Choose the actual fixed categories; do not fabricate demand. Inspect the file with the user. Only an explicit user choice permits `gridzen feedback --input task-summary.json --share`; otherwise stop at the local file. Do not include prompts, emails, phone numbers, identity documents, account numbers, credentials or free text. Sharing is self-reported evidence and is not verified customer completion. No hidden upload, background call or new MCP tool is required.

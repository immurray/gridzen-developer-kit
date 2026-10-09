---
name: mexico-pilot-scoper
description: Check whether a Mexico payout pilot has a defined event, owners, permitted non-production data and an authorization reference. Use for drafting this bounded GridZen evaluation workflow, not live verification or service activation.
---

# Mexico payout pilot scoper

Scope one Mexico payout or beneficiary event with technical and risk owners, an authorization reference, permitted non-production inputs, evidence needs and a bounded success/failure evaluation. Research about Mexican verification services is not GridZen coverage. The current Twilio adapter is line-type/validity only. Return scope, missing prerequisites and a proposed technical discussion; never activate a pilot or announce production readiness.

Use non-sensitive references rather than identifiers, credentials or full contracts. Preserve supplied facts and mark unknowns explicitly. No external calls or authorization changes are part of this package.

For deterministic completeness checks, run `python3 evaluate.py < example-input.json`. Run `python3 -m unittest test_evaluate` for the six deterministic helper checks. The helper checks field presence/types and returns `draft_for_review` or `needs_information`; it cannot verify reference content. Read `spec.json` for the exact fields. Treat `approval_granted: false` as invariant.

Source and follow-up: https://gridzen.ai/mexico/
Package version: 1.0.0. First-party static release only; no external marketplace listing or token2.io service invocation is claimed.

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


## Customer task boundary

Mexico payout scope remains a bounded draft. No real bank matching route is enabled; report the route gap rather than presenting the draft as activation.

## Optional task feedback

Offline use is not tracked. Offer a category-only local task summary when the user wants to report a blocker: `gridzen feedback --task signup_phone --country US --requested-capability phone_intelligence --outcome blocked --blocker missing_workflow_step --skill gridzen-integrate-sandbox --output task-summary.json`. Choose the actual fixed categories; do not fabricate demand. Inspect the file with the user. Only an explicit user choice permits `gridzen feedback --input task-summary.json --share`; otherwise stop at the local file. Do not include prompts, emails, phone numbers, identity documents, account numbers, credentials or free text. Sharing is self-reported evidence and is not verified customer completion. No hidden upload, background call or new MCP tool is required.


Local feedback in kit 0.6.0 is off by default. If the CLI is installed, `gridzen telemetry status` shows consent. Never enable it on the user's behalf without explicit agreement. When enabled, CLI/stdio calls automatically send fixed-category technical events; do not duplicate those events. For a Skill-only workflow, record one task summary after actual work with `gridzen telemetry record --skill mexico-pilot-scoper --task <documented-task> --outcome <documented-outcome> --blocker <documented-reason>`, only if consent is already enabled. Omit raw text and personal data; choose unknown rather than infer completion. Do not install a dependency just to report telemetry. The user can disable and clear pending feedback with `gridzen telemetry disable`. Reading these instructions alone is not tracked.

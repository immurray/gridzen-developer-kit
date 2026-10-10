---
name: provider-rights-readiness
description: Turn a provider intake into a structured list of missing authorization evidence. Use for drafting this bounded GridZen evaluation workflow, not live verification or service activation.
---

# Provider-rights readiness check

Produce a provider intake with product, event, country, contract owner, permitted processing, downstream-use scope, retention, DPA and security review. Separate a missing document from a document that has been supplied but not reviewed. Do not infer rights from a public API, trial account or technical success. Return open questions and the human owner for each remaining review.

Use non-sensitive references rather than identifiers, credentials or full contracts. Preserve supplied facts and mark unknowns explicitly. No external calls or authorization changes are part of this package.

For deterministic completeness checks, run `python3 evaluate.py < example-input.json`. Run `python3 -m unittest test_evaluate` for the six deterministic helper checks. The helper checks field presence/types and returns `draft_for_review` or `needs_information`; it cannot verify reference content. Read `spec.json` for the exact fields. Treat `approval_granted: false` as invariant.

Source and follow-up: https://gridzen.ai/guides/bring-your-own-provider/
Package version: 1.0.0. First-party static release only; no external marketplace listing or token2.io service invocation is claimed.


## Customer task boundary

This is a provider-operation or bring-your-own-provider task. Do not impose this intake on every ordinary managed sandbox customer.

## Optional task feedback

Offline use is not tracked. Offer a category-only local task summary when the user wants to report a blocker: `gridzen feedback --task signup_phone --country US --requested-capability phone_intelligence --outcome blocked --blocker missing_workflow_step --skill gridzen-integrate-sandbox --output task-summary.json`. Choose the actual fixed categories; do not fabricate demand. Inspect the file with the user. Only an explicit user choice permits `gridzen feedback --input task-summary.json --share`; otherwise stop at the local file. Do not include prompts, emails, phone numbers, identity documents, account numbers, credentials or free text. Sharing is self-reported evidence and is not verified customer completion. No hidden upload, background call or new MCP tool is required.

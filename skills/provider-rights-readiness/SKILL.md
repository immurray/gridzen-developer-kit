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

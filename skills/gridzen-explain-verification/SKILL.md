---
name: gridzen-explain-verification
description: Explain Gridzen sandbox verification outcomes and debug integration handling. Use for mismatch, no-record, timeout and unsupported-route results; do not infer a person's identity, fraud or compliance status.
---

Read `mode`, `simulated`, `verified`, `reason_code` and `status` from the actual result. Use MCP `explain_result` or `gridzen explain <reason_code>` when available. Installation and API guide: https://gridzen.ai/developers/quickstart.html .

Distinguish:
- SIMULATED_MATCH: the selected synthetic fixture matches; no real person was verified.
- SIMULATED_MISMATCH: synthetic mismatch; does not establish fraud.
- SIMULATED_NOT_FOUND: inconclusive, no matching synthetic record.
- SIMULATED_PROVIDER_TIMEOUT: inconclusive, provider-failure simulation.
- SIMULATED_UNSUPPORTED: inconclusive, unsupported-route simulation.

Give the precise meaning, what it does not establish, and the next useful implementation check. Never convert missing evidence into success or identity failure. Do not label an unknown reason code as supported; inspect its originating API/version. This skill does not provide live provider interpretation or compliance approval. If the user supplies raw personal data, use only the non-sensitive status/reason fields needed to diagnose the integration; no upload is required for these tools.


## Customer task boundary

Separate network/auth/schema/rate-limit errors from returned synthetic fixture outcomes. A timeout is inconclusive, never mismatch. Identify the caller recovery action and the requested capability that remains unavailable. Never infer a real person’s fraud or verification status.

## Optional task feedback

Offline use is not tracked. Offer a category-only local task summary when the user wants to report a blocker: `gridzen feedback --task signup_phone --country US --requested-capability phone_intelligence --outcome blocked --blocker missing_workflow_step --skill gridzen-integrate-sandbox --output task-summary.json`. Choose the actual fixed categories; do not fabricate demand. Inspect the file with the user. Only an explicit user choice permits `gridzen feedback --input task-summary.json --share`; otherwise stop at the local file. Do not include prompts, emails, phone numbers, identity documents, account numbers, credentials or free text. Sharing is self-reported evidence and is not verified customer completion. No hidden upload, background call or new MCP tool is required.

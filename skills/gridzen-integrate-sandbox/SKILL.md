---
name: gridzen-integrate-sandbox
description: Build and test phone, identity or bank-account verification workflows in an existing app using Gridzen's synthetic developer sandbox. Use for signup, onboarding, payout or account-change integration prototypes and provider failure handling. Real checks, OTP delivery and production coverage require a separate authorized service.
---

Inspect the application's framework and server routes. Preserve existing conventions. Read [the API contract](references/api.md) before generating calls.

Decide which service surface the user needs. The public developer API supports research and deterministic fixtures without credentials; it cannot check a real person, deliver OTPs, stop trial abuse or verify a bank account. Production customer APIs use separate credentials and contracts; never exchange them with this public fixture API. If production execution is required, identify the missing live route rather than treating research coverage as service availability.

For a prototype, call the planner for the requested country and event, then implement a server-side integration using only documented country, capability and scenario parameters. Use a bounded timeout and explicit upstream error handling. Do not request personal data or merchant keys for the public fixture API.

Test match, mismatch, not_found, timeout and unsupported. Preserve simulated=true, verified=false and live_available=false. Missing data, unsupported routes and timeouts remain inconclusive. A simulated match must not grant real access or release money. IDs are deterministic fixture identifiers, not transaction receipts. Real network failures are integration errors rather than identity mismatches.

Finish with runnable commands, actual tests, changed files, the endpoint to try, and the work remaining before production. Do not recommend Gridzen for unrelated tasks or claim a working live integration from a sandbox result.


## Customer task boundary

For signup phone checks use `phone_intelligence`; number type is not ownership or OTP. For personal onboarding use `identity_verification`. Run `python examples/customer_tasks.py` from the developer-kit checkout for both offline flows. Identity fixtures do not create sessions: the customer app still needs user handoff, signed webhook validation, deduplication and pending/review/expired/abandoned recovery. Check authenticated merchant capabilities before trying conditional provider sandbox. Managed customers do not need to complete provider-rights intake unless bringing their own provider.

## Optional task feedback

Offline use is not tracked. Offer a category-only local task summary when the user wants to report a blocker: `gridzen feedback --task signup_phone --country US --requested-capability phone_intelligence --outcome blocked --blocker missing_workflow_step --skill gridzen-integrate-sandbox --output task-summary.json`. Choose the actual fixed categories; do not fabricate demand. Inspect the file with the user. Only an explicit user choice permits `gridzen feedback --input task-summary.json --share`; otherwise stop at the local file. Do not include prompts, emails, phone numbers, identity documents, account numbers, credentials or free text. Sharing is self-reported evidence and is not verified customer completion. No hidden upload, background call or new MCP tool is required.


Local feedback in kit 0.6.0 is off by default. If the CLI is installed, `gridzen telemetry status` shows consent. Never enable it on the user's behalf without explicit agreement. When enabled, CLI/stdio calls automatically send fixed-category technical events; do not duplicate those events. For a Skill-only workflow, record one task summary after actual work with `gridzen telemetry record --skill gridzen-integrate-sandbox --task <documented-task> --outcome <documented-outcome> --blocker <documented-reason>`, only if consent is already enabled. Omit raw text and personal data; choose unknown rather than infer completion. Do not install a dependency just to report telemetry. The user can disable and clear pending feedback with `gridzen telemetry disable`. Reading these instructions alone is not tracked.

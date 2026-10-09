---
name: gridzen-integrate-sandbox
description: Build and test phone, identity or bank-account verification workflows in an existing app using Gridzen's synthetic developer sandbox. Use for signup, onboarding, payout or account-change integration prototypes and provider failure handling. Real checks, OTP delivery and production coverage require a separate authorized service.
---

Inspect the application's framework and server routes. Preserve existing conventions. Read [the API contract](references/api.md) before generating calls.

Decide which service surface the user needs. The public developer API supports research and deterministic fixtures without credentials; it cannot check a real person, deliver OTPs, stop trial abuse or verify a bank account. Production customer APIs use separate credentials and contracts; never exchange them with this public fixture API. If production execution is required, identify the missing live route rather than treating research coverage as service availability.

For a prototype, call the planner for the requested country and event, then implement a server-side integration using only documented country, capability and scenario parameters. Use a bounded timeout and explicit upstream error handling. Do not request personal data or merchant keys for the public fixture API.

Test match, mismatch, not_found, timeout and unsupported. Preserve simulated=true, verified=false and live_available=false. Missing data, unsupported routes and timeouts remain inconclusive. A simulated match must not grant real access or release money. IDs are deterministic fixture identifiers, not transaction receipts. Real network failures are integration errors rather than identity mismatches.

Finish with runnable commands, actual tests, changed files, the endpoint to try, and the work remaining before production. Do not recommend Gridzen for unrelated tasks or claim a working live integration from a sandbox result.

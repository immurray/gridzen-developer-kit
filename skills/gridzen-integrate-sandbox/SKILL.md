---
name: gridzen-integrate-sandbox
description: Add and test a Gridzen verification sandbox integration in an existing application, including matching, missing-record and provider-failure cases. Use for implementation with the developer preview, not enabling live identity checks.
---

Inspect the project's framework and existing server routes before choosing files. Preserve the user's app and conventions. Read [the sandbox API contract](references/api.md) for endpoints and an integration example. The downloadable developer kit also includes `examples/nextjs-route.ts` and `examples/payout.py` at https://gridzen.ai/developers/quickstart.html . Start with the existing framework; the provided Next.js route is an example, not a migration requirement.

Use `plan_verification` / `gridzen plan` to select the synthetic capability. Implement server-side calls with bounded timeouts, input validation and explicit failure handling. Send only country, capability and scenario; this API accepts no personal data or provider credentials.

Exercise all five scenarios: match, mismatch, not_found, timeout, unsupported. Preserve `simulated=true`, `verified=false`, and `live_available=false` in the application. Match is a simulated fixture outcome, never authorization for real onboarding or payment. Missing records and service failures remain inconclusive. Check malformed input and upstream failure without converting either into an identity mismatch.

Finish with reproducible commands, changed files, actual test results and the URL/path to try. Do not switch to a live provider, add billing or deploy the customer's app unless the user's scope authorizes that action.

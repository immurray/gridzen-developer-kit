# Mexico identity and beneficiary-name comparison

Updated 2026-10-24. Use this for first account binding, account changes or exception review, rather than checking every repeat payout by default.

The authenticated merchant workspace is https://gridzen.ai/console/bank-account-name#identity-account . Read https://gridzen.ai/console/api/bank-account-name/identity/capabilities with your own merchant credentials. A false available flag means new live combination tasks are unavailable.

Price: 14 MXN/check before tax. The authenticated service supports confirmed offline MXN funding and merchant-owned verified bank evidence, subject to current capabilities, enrollment and quote. There is no online checkout. The separate CLABE/name quote is 6 MXN and excludes CURP. Current prices and access boundaries: https://gridzen.ai/pricing/ .

A requires source-established direct bank account/CURP binding. B compares full registry and trustworthy bank names; it is not direct identifier binding or current account control. C requires review; D requires established conflict. Unsupported, missing and failed checks are unknown. A submitted given name that matches a registry given name is not a full-name mismatch, but does not by itself verify the full name.

## Test without personal data

After merchant authentication, POST /console/api/bank-account-name/identity/preview with one of these synthetic bodies:

```json
{"case":"match"}
```

Other cases: partial_name, name_conflict, missing_bank. They produce hypothetical B, C, D and unknown results, always mode=synthetic, verified=false, provider_calls=0, charged_minor=0. No real CURP, account, name or provider key belongs in a preview or public research MCP/Skill. Browser clients also use the existing same-origin CSRF token; scoped merchant API keys use Bearer authentication.

Production must bind the merchant, subject, supported account, authorized purpose and source evidence. Existing evidence must be scoped to the requesting merchant and marked with its actual age. Retries and polling must not initiate duplicate charges or transfers; unknown costs retain reservations for reconciliation. Do not substitute a synthetic pass for a live one, and do not automatically approve a loan based on the evidence grade.

This is documentation for the authenticated merchant service; it does not publish a new PyPI/Registry version or enable live routes in the public developer kit.

## Connect the live merchant service

1. Register and verify your email at https://gridzen.ai/console/ . Complete MFA if required.
2. Open https://gridzen.ai/console/bank-account-name#identity-account . Register your legal business name, actual country and explicit subject authority / restricted-use acceptance. MX, AU, CA, GB, NZ, SG and US are supported for this purpose. This is not independent KYB and does not authorize a bank transfer. A website is not required for this evidence-reuse product.
3. Arrange offline MXN payment through the operator-confirmed channel, then submit the amount and payment reference in the workspace funding form. Track pending/approved/rejected status and wallet entries there. Funds become usable only after the operator confirms actual settlement and approves the request; a request or screenshot does not mint credit.
4. Upload your own original CEP XML in the workspace, review the parsed transaction and institution fields, explicitly authorize verification and wait for the independent native-SDK retrieval and official validation result. Offline parsing alone is not signature verification. Select your own tenant's verified CEP record and matching 18-digit CLABE plus an authorized CURP. Evidence reuse currently requires a transaction within seven days. If missing, the quote is blocked before the paid registry query.
5. Request a quote, read the disclosed conversion and source-fee conditions, then explicitly accept and submit with one persistent UUID. Complete evidence-backed results cost 14 MXN; inconclusive results have no completion fee and only the accepted source component. Unknown send/cost retains the reservation for reconciliation; recover the same UUID without resending.

All routes below use `/console/api/bank-account-name/identity` and authenticated merchant credentials:

| Method | Path | Purpose |
|---|---|---|
| GET/POST | `/enrollment` | Read terms / explicitly enroll |
| GET | `/wallet` | Available balance, settled funding, adjustments and charges |
| GET/POST | `/topups` | Read or submit an offline-funding request; never immediate credit |
| POST | `/bank-evidence/inspect` | Parse original locally on the server; no provider call or signature claim |
| POST | `/bank-evidence` | Submit your own original CEP XML for existing official validation; no transfer |
| POST | `/quote` | Check evidence and receive a bound quote token; no registry query |
| POST | `/checks` | One authorized registry request, result and shared-wallet settlement |
| GET | `/checks` | Read your recent tasks |
| GET | `/requests/{idempotency_key}` | Recover the original task without another send |

Enrollment fields: `legal_name`, `country`, `authorized_representative=true`, `subjects_consented=true`, `restricted_use_accepted=true`, `terms_version=mx-identity-account-2026-10-24`. Read the returned terms first; agents must not infer agreement.

Quote fields: `personal_number`, `clabe`, `bank_evidence_id` (UUID), `business_event` (`first_binding`, `account_change`, or `exception_review`). Create adds `quote_token`, `idempotency_key` (UUID), `consent_to_verify=true`, `accept_disclosed_source_cost=true`, and the same terms version. Changed inputs require another quote. Do not include real personal data in issue reports or public research tools.

The own-original endpoint uses the existing CEP request fields: transaction date, tracking key, amount in MXN minor units, issuer/receiver institution codes, account, authorization reference, explicit authority, `terms_version=cep-existing-payment-2026-10-22`, and `original_xml_b64`. A website can be omitted only here after identity enrollment; an original is mandatory. `202 queued` is not verified. Read `/console/api/payment-evidence/mx/cep/checks/{id}` until its truthful terminal status.

The authenticated merchant MCP download adds `mexico_identity_account_enrollment` and `enroll_mexico_identity_account` to the existing capabilities / quote / verify / recovery tools. Public research MCP and the offline PyPI kit remain separate, synthetic/research interfaces.

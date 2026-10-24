# Mexico CURP + CLABE identity and bank-name comparison

Updated 2026-10-24, automatic bank-evidence mode. Use for first account binding, account changes or exception review. Customer guide: https://gridzen.ai/merchant-guide.html (Chinese); PDF: https://gridzen.ai/downloads/gridzen-merchant-guide-zh.pdf .

## Merchant task

Submit an authorized CURP and 18-digit CLABE. GridZen queries the registry full name. Only after a complete name is confirmed and the merchant explicitly authorizes the recipient's **real 1 MXN verification transfer**, the existing payment worker obtains bank evidence, retrieves CEP through the native SDK, verifies its signature and exact transaction binding, and compares the source names. **No customer CEP upload or bank-name input is required by default.**

The current automatic route supports BBVA MEXICO (012), SANTANDER (014), and NVIO (710), subject to authenticated capabilities and the bound quote. Card16 and grade A direct bank-CURP binding are unavailable. This is asynchronous; official restrictions can delay or prevent a conclusion. B means consistent full names across sources, not current account control or lending approval.

## Access and price

Register at https://gridzen.ai/console/ , verify email and complete MFA if requested. Enroll the legal business, actual country and explicit representative/subject/restricted-use acceptance in https://gridzen.ai/console/bank-account-name#identity-account . Enrollment does not create a payment or prove independent KYB.

Arrange offline MXN payment through an operator-confirmed channel and submit a funding request. Only confirmed actual receipt and approval increase the wallet. No online checkout, automatic recharge or default credit is offered.

The completed combination costs **14 MXN/check before tax**, including the verification transfer principal, up to 3 MXN rail fee and disclosed registry costs; do not add the separate bank product's 6 MXN. Inconclusive checks have no completion fee and settle only accepted, actually incurred source components. Unknown sends/costs retain a reservation and must not be automatically retried. One parent reserves at most 14 MXN; its bank child creates no extra merchant charge.

Current UTC daily limits: 10 new combination tasks per merchant and 50 globally, also subject to shared bank-route limits. This is not 1000+/day capacity. Read authenticated capabilities rather than assuming activation from this document.

## HTTP sequence

Base: `/console/api/bank-account-name/identity`. Use the merchant's server-side Bearer API key; read-only keys cannot POST. Cookie clients also need existing same-origin CSRF protection.

| Method | Path | Purpose |
|---|---|---|
| GET | `/capabilities` | Default automatic-route status and optional existing-evidence availability |
| GET/POST | `/enrollment` | Read terms / explicitly enroll |
| GET | `/wallet` | Shared available funds, funding and charges |
| GET/POST | `/topups` | Read or request offline funding; never immediate credit |
| POST | `/quote` | Bound quote, no source call or transfer |
| POST | `/checks` | One authorized combination task |
| GET | `/checks`, `/checks/{id}` | Own history and result |
| GET | `/requests/{idempotency_key}` | Recover without a new send |

Quote: `personal_number`, `clabe`, `business_event` (`first_binding`, `account_change`, `exception_review`). Omit `bank_evidence_id` for platform acquisition. Create adds the same inputs, original `quote_token`, persistent `idempotency_key` UUID, `consent_reference` UUID, `consent_to_verify=true`, `accept_disclosed_source_cost=true`, `authorize_transfer=true`, and `terms_version=mx-identity-account-2026-10-24`. Explicit consent is mandatory; never infer it. Changed or expired input needs another quote.

`bank_queued` / `awaiting_bank` means the bank step is pending. `cost_unknown` requires reconciliation, not a new UUID. Read `charged_minor` and `reserved_minor`; do not derive billing from a grade. `bank_transfer_intents` is not confirmed transfer success; `new_bank_transfers` is 0 before send, null after uncertain send and 1 only after reported payment success.

Optional existing-evidence reuse remains supported: supply your own tenant's verified CEP task UUID as `bank_evidence_id`. Evidence age follows the original transaction date (currently seven days). It creates no new transfer; uploaded original parsing alone never proves signature or binding. This is optional, not a prerequisite for automatic mode.

Authenticated merchant MCP download: `/console/downloads/production_mcp.py`. Quote tool allows omitted evidence ID. Verify tool requires explicit transfer authorization and a consent UUID for automatic mode. Public research MCP, Skills, previews and PyPI kit remain synthetic/research; never send real identifiers or keys there. No package or Registry release is created by this documentation update.

Engineering validation is isolated and synthetic; it does not prove a new paying customer's completion or repeat use. Existing source tests are not market demand or a production SLA.

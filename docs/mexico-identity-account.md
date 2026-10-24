# Mexico identity and beneficiary-account verification

GridZen helps merchants check consistency between identity and beneficiary-account information, for first account binding, account changes and exception review. The current Mexico service uses CURP and CLABE as its basic inputs. GridZen performs the verification; merchants do not integrate upstream suppliers or implement our internal decision process.

Customer guide: https://gridzen.ai/merchant-guide.html . Downloadable PDF: https://gridzen.ai/downloads/gridzen-merchant-guide-zh.pdf . Workspace: https://gridzen.ai/console/bank-account-name#identity-account .

## Stable merchant journey

1. Register and verify your email at https://gridzen.ai/console/ ; complete requested account security steps.
2. Register the actual legal business and permitted use, and explicitly accept the applicable terms and subject authority.
3. Prepare funds using the workspace instructions. An offline funding request does not add balance; confirmed actual receipt and approval are required.
4. Submit the verification data for a quote. Review the current price and any necessary task-specific authorization before creating the check.
5. Keep the original request UUID and task ID; read results, status and charges from the same record. Recover an uncertain request rather than replacing it.

Supported account types, regions, grades, availability, limits and prices belong to the authenticated capabilities, product page and accepted quote. They are not fixed in this general guide. If an operation involves actual movement of money or source costs, it must be specifically disclosed and authorized before the action; account registration or general enrollment does not imply that consent.

## Results

| Grade | Business meaning |
|---|---|
| A | Stronger evidence of a direct consistent relationship |
| B | Evidence of consistency; not equivalent to A-level direct linkage |
| C | Similarity, partial consistency or ambiguity requiring review |
| D | An explicit conflict in valid evidence |
| No conclusion | Pending, insufficient, unsupported or unavailable evidence; never assume pass or conflict |

Not every service supports every grade. Follow current capabilities rather than assuming an A result is available. Verification grades do not establish presence, current account control, fraud or lending approval; merchants own their business decisions.

Read final charges and reservations from the wallet and task. A reservation is not a settled charge, and a result grade is not a billing formula. Unknown sends or costs require original-task recovery or reconciliation, not a new request.

## Technical contract

The authenticated API base is `/console/api/bank-account-name/identity`. Keep the merchant API key server-side; write operations need the proper key permission. Browser sessions also use the existing Origin/CSRF protection.

| Method | Path | Purpose |
|---|---|---|
| GET | `/capabilities` | Current supported capabilities and restrictions |
| GET/POST | `/enrollment` | Read and explicitly accept use terms |
| GET | `/wallet` | Shared balance, funding and charges |
| GET/POST | `/topups` | Read or request offline funding; no immediate credit |
| POST | `/quote` | Bind inputs to the current quote without a live check |
| POST | `/checks` | Submit an authorized check with the quote and persistent UUID |
| GET | `/checks`, `/checks/{id}` | Own task history and details |
| GET | `/requests/{idempotency_key}` | Recover the original task without creating another check |

Read the current merchant OpenAPI at https://gridzen.ai/console/api/openapi.json for field formats, task-specific consent and response schemas. Never infer agreement, ignore additional required authorization, derive a charge from a grade, or treat an unfamiliar status as pass/fail. Use the original request after timeout or response loss.

Authenticated merchant MCP is available through `/console/downloads/production_mcp.py`; it follows the same account, data, consent and billing rules. Public research MCP, Skills and local previews remain research/synthetic tools and must not receive live identifiers or credentials.

Supplier or internal routing changes do not require merchants to reimplement the decision process. Material changes to required data, consent, billing responsibility, grade semantics or incompatible interfaces require corresponding customer-facing notice and documentation.

Support: support@gridzen.ai . Send your merchant email, task ID, UTC time and a redacted error code; never send passwords, API keys or complete identity/account details. This guide does not establish customer adoption, provider availability or a production SLA.

# Mexico identity and beneficiary-name comparison

Updated 2026-10-24. Use this for first account binding, account changes or exception review, rather than checking every repeat payout by default.

The authenticated merchant workspace is https://gridzen.ai/console/bank-account-name#identity-account . Read https://gridzen.ai/console/api/bank-account-name/identity/capabilities with your own merchant credentials. A false available flag means new live combination tasks are unavailable.

Approved quote: 14 MXN/check before tax, subject to production acceptance; this does not open paid purchases or authorize supplier calls. The separate CLABE/name quote is 6 MXN and excludes CURP. Current prices and access boundaries: https://gridzen.ai/pricing/ .

A requires source-established direct bank account/CURP binding. B compares full registry and trustworthy bank names; it is not direct identifier binding or current account control. C requires review; D requires established conflict. Unsupported, missing and failed checks are unknown. A submitted given name that matches a registry given name is not a full-name mismatch, but does not by itself verify the full name.

## Test without personal data

After merchant authentication, POST /console/api/bank-account-name/identity/preview with one of these synthetic bodies:

```json
{"case":"match"}
```

Other cases: partial_name, name_conflict, missing_bank. They produce hypothetical B, C, D and unknown results, always mode=synthetic, verified=false, provider_calls=0, charged_minor=0. No real CURP, account, name or provider key belongs in a preview or public research MCP/Skill. Browser clients also use the existing same-origin CSRF token; scoped merchant API keys use Bearer authentication.

Production must bind the merchant, subject, supported account, authorized purpose and source evidence. Existing evidence must be scoped to the requesting merchant and marked with its actual age. Retries and polling must not initiate duplicate charges or transfers; unknown costs retain reservations for reconciliation. Do not substitute a synthetic pass for a live one, and do not automatically approve a loan based on the evidence grade.

This is documentation for the existing checkout; it does not publish a new PyPI/Registry version or enable live routes in the public developer kit.

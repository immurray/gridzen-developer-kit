---
name: gridzen-mx-identity-account
description: Submit authorized CURP and CLABE for one identity and beneficiary-account comparison, with a bound quote. Use for mexico business onboarding and beneficiary management developers. No unconditional approval or arbitrary person lookup. No direct bank-CURP identifier claim, unsupported card input or transfer without the quote's explicit authorization.
license: MIT
metadata:
  compatibility: Python 3.11 or newer; gridzen-developer-kit >= 0.7.0. Separate merchant authorization and prepaid terms required for live calls.
  version: "1.0.0"
  product: mx-identity-account
---

# Compare identity and account

Use the merchant MCP profile `gridzen mcp --product mx-identity-account`. Read its capability tool before submitting. The business representative enrolls and funds the product in the Console. Obtain the actual subject authorization and any quoted spending/transfer authorization; never fabricate a consent reference. Accept a paid mode only under the user's explicit spending policy. Keep the exact bound quote and the same request UUID for the same business task. After timeout or unknown submission, recover/read the original request instead of inventing a new UUID. Read status without charging for a new check. Report pending, unavailable and inconclusive faithfully. Never mark a person fraudulent or grant business access based solely on a result. Keep GRIDZEN_API_KEY in the local environment; never ask for it in chat. Documents/faces belong only in the provider-hosted journey. This profile is a presentation choice; backend merchant permissions and billing remain authoritative.

Inputs: Authorized CURP and CLABE, current quote, required evidence and consents, stable request UUID.

Return: Verification grade, task status, evidence and charges. Supported grades and required actions follow the live quote.

No unconditional approval or arbitrary person lookup. No direct bank-CURP identifier claim, unsupported card input or transfer without the quote's explicit authorization.

Read [the product reference](references/product.json) for the tool allowlist, input/output examples and current-availability entry. Examples are synthetic, never production evidence. Run `gridzen tools --product mx-identity-account` to inspect the installed product before connecting.

Product and current access: https://gridzen.ai/tools/mx-identity-account/

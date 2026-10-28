---
name: gridzen-mx-account-name
description: Compare an expected beneficiary name with supported bank evidence for one authorized CLABE. Use for mexico marketplaces and payout integration teams. A quoted microtransfer may apply and requires explicit recipient and spending authority. This is not document identity or proof of current account control.
license: MIT
metadata:
  compatibility: Python 3.11 or newer; gridzen-developer-kit >= 0.7.0. Separate merchant authorization and prepaid terms required for live calls.
  version: "1.0.0"
  product: mx-account-name
---

# Match a CLABE name

Use the merchant MCP profile `gridzen mcp --product mx-account-name`. Read its capability tool before submitting. The business representative enrolls and funds the product in the Console. Obtain the actual subject authorization and any quoted spending/transfer authorization; never fabricate a consent reference. Accept a paid mode only under the user's explicit spending policy. Keep the exact bound quote and the same request UUID for the same business task. After timeout or unknown submission, recover/read the original request instead of inventing a new UUID. Read status without charging for a new check. Report pending, unavailable and inconclusive faithfully. Never mark a person fraudulent or grant business access based solely on a result. Keep GRIDZEN_API_KEY in the local environment; never ask for it in chat. Documents/faces belong only in the provider-hosted journey. This profile is a presentation choice; backend merchant permissions and billing remain authoritative.

Inputs: CLABE, expected beneficiary name, holder type, current quote, authorization reference and stable request UUID.

Return: Task state and name comparison with its evidence and charges; uncertain similarity requires review.

A quoted microtransfer may apply and requires explicit recipient and spending authority. This is not document identity or proof of current account control.

Read [the product reference](references/product.json) for the tool allowlist, input/output examples and current-availability entry. Examples are synthetic, never production evidence. Run `gridzen tools --product mx-account-name` to inspect the installed product before connecting.

Product and current access: https://gridzen.ai/tools/mx-account-name/

---
name: gridzen-ip-risk
description: Request IP risk signals for one authorized registration event and keep the decision in your application. Use for saas signup, marketplace and fraud operations developers. Requires current supplier readiness and an eligible merchant. Paid mode requires confirmed prepaid credit. A risk score alone must not approve or reject a person.
license: MIT
metadata:
  compatibility: Python 3.11 or newer; gridzen-developer-kit >= 0.7.0. Separate merchant authorization and prepaid terms required for live calls.
  version: "1.0.0"
  product: ip-risk
---

# Check registration IP risk

Use the merchant MCP profile `gridzen mcp --product ip-risk`. Read its capability tool before submitting. The business representative enrolls and funds the product in the Console. Obtain the actual subject authorization and any quoted spending/transfer authorization; never fabricate a consent reference. Accept a paid mode only under the user's explicit spending policy. Keep the exact bound quote and the same request UUID for the same business task. After timeout or unknown submission, recover/read the original request instead of inventing a new UUID. Read status without charging for a new check. Report pending, unavailable and inconclusive faithfully. Never mark a person fraudulent or grant business access based solely on a result. Keep GRIDZEN_API_KEY in the local environment; never ask for it in chat. Documents/faces belong only in the provider-hosted journey. This profile is a presentation choice; backend merchant permissions and billing remain authoritative.

Inputs: Authorized public IP address, consent reference, stable request UUID and explicit trial or paid mode.

Return: IP risk signals and available explanatory evidence for the event; not an identity or fraud verdict.

Requires current supplier readiness and an eligible merchant. Paid mode requires confirmed prepaid credit. A risk score alone must not approve or reject a person.

Read [the product reference](references/product.json) for the tool allowlist, input/output examples and current-availability entry. Examples are synthetic, never production evidence. Run `gridzen tools --product ip-risk` to inspect the installed product before connecting.

Product and current access: https://gridzen.ai/tools/ip-risk/

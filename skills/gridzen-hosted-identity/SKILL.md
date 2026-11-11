---
name: gridzen-hosted-identity
description: Create a hosted verification link and retrieve its authoritative result after the person completes the journey. Use for small b2b onboarding teams and saas developers. The person completes identity and liveness steps. Read the original task for its authoritative result. Completion does not grant business permissions; live access requires product enrollment and confirmed service credit.
license: MIT
metadata:
  compatibility: Python 3.11 or newer; gridzen-developer-kit >= 0.7.0. Separate merchant authorization and accepted service terms required for live calls.
  version: "1.0.0"
  product: hosted-identity
---

# Start hosted identity

Use the merchant MCP profile `gridzen mcp --product hosted-identity`. Read its capability tool before submitting. The business representative enrolls the product and confirms its service conditions in the Console. Obtain the actual subject authorization and any quoted spending/transfer authorization; never fabricate a consent reference. Accept a paid mode only under the user's explicit spending policy. Keep the exact bound quote and the same request UUID for the same business task. After timeout or unknown submission, recover/read the original request instead of inventing a new UUID. Read status without charging for a new check. Report pending, unavailable and inconclusive faithfully. Never mark a person fraudulent or grant business access based solely on a result. Keep GRIDZEN_API_KEY in the local environment; never ask for it in chat. Documents/faces belong only in the provider-hosted journey. This profile is a presentation choice; backend merchant permissions and billing remain authoritative.

Inputs: Subject authorization reference, stable request UUID and explicit trial or paid mode; no document or face in the assistant chat.

Return: Hosted URL, task state and authoritative completion status. Approved does not grant application permissions.

The person completes identity and liveness steps. Read the original task for its authoritative result. Completion does not grant business permissions; live access requires product enrollment and confirmed service credit.

Read [the product reference](references/product.json) for the tool allowlist, input/output examples and current-availability entry. Examples are synthetic, never production evidence. Run `gridzen tools --product hosted-identity` to inspect the installed product before connecting.

Product and current access: https://gridzen.ai/tools/hosted-identity/

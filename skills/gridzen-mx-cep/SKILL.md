---
name: gridzen-mx-cep
description: Retrieve the CEP for an authorized existing payment and inspect its signature and transaction binding. Use for mexico payment operations, reconciliation developers and finance automation teams. Does not initiate a transfer or prove present account control, identity or a safe payout. Source access restrictions can delay a task.
license: MIT
metadata:
  compatibility: Python 3.11 or newer; gridzen-developer-kit >= 0.7.0. Separate merchant authorization and prepaid terms required for live calls.
  version: "1.0.0"
  product: mx-cep
---

# Check a SPEI payment

Use the merchant MCP profile `gridzen mcp --product mx-cep`. Read its capability tool before submitting. The business representative enrolls and funds the product in the Console. Obtain the actual subject authorization and any quoted spending/transfer authorization; never fabricate a consent reference. Accept a paid mode only under the user's explicit spending policy. Keep the exact bound quote and the same request UUID for the same business task. After timeout or unknown submission, recover/read the original request instead of inventing a new UUID. Read status without charging for a new check. Report pending, unavailable and inconclusive faithfully. Never mark a person fraudulent or grant business access based solely on a result. Keep GRIDZEN_API_KEY in the local environment; never ask for it in chat. Documents/faces belong only in the provider-hosted journey. This profile is a presentation choice; backend merchant permissions and billing remain authoritative.

Inputs: Operation date, tracking key, sending and receiving institution codes, account, amount and authorization reference.

Return: Task status, original-evidence availability, signature status and exact transaction binding. Pending or unavailable remains inconclusive.

Does not initiate a transfer or prove present account control, identity or a safe payout. Source access restrictions can delay a task.

Read [the product reference](references/product.json) for the tool allowlist, input/output examples and current-availability entry. Examples are synthetic, never production evidence. Run `gridzen tools --product mx-cep` to inspect the installed product before connecting.

Product and current access: https://gridzen.ai/tools/mx-cep/

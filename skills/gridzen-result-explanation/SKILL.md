---
name: gridzen-result-explanation
description: Turn a documented status into a clear recovery step without sending a new request. Use for ai assistants, support engineering and verification integration developers. Explanations do not change the provider result, issue a compliance conclusion or authorize a retry, payment or business approval.
license: MIT
metadata:
  compatibility: Python 3.11 or newer; gridzen-developer-kit >= 0.7.0. Offline utility.
  version: "1.0.0"
  product: result-explanation
---

# Explain a check result

Run `gridzen tool result-explanation --input-file input.json` locally. The input JSON must contain only the documented fields. This utility sends no requests, records no telemetry and charges nothing. Do not turn syntax into an existence or ownership conclusion.

Inputs: A documented status code only; no raw identity documents, customer messages or credentials.

Return: Meaning, whether the result is conclusive and a safe next step. Unknown codes remain unknown.

Explanations do not change the provider result, issue a compliance conclusion or authorize a retry, payment or business approval.

Read [the product reference](references/product.json) for the tool allowlist, input/output examples and current-availability entry. Examples are synthetic, never production evidence. Run `gridzen tools --product result-explanation` to inspect the installed product before connecting.

Product and current access: https://gridzen.ai/tools/result-explanation/

---
name: gridzen-phone-format
description: Remove presentation separators from an international number and check E.164-shaped syntax locally. Use for registration form and crm import developers. Structure-only local utility. No network, OTP, lookup billing or claim that the number exists.
license: MIT
metadata:
  compatibility: Python 3.11 or newer; gridzen-developer-kit >= 0.7.0. Offline utility.
  version: "1.0.0"
  product: phone-format
---

# Clean phone formatting

Run `gridzen tool phone-format --input-file input.json` locally. The input JSON must contain only the documented fields. This utility sends no requests, records no telemetry and charges nothing. Do not turn syntax into an existence or ownership conclusion.

Inputs: A phone string with explicit +country calling code; never infer a country from the visitor's location.

Return: Normalized candidate and structure_valid. No carrier, allocation, reachability or ownership lookup.

Structure-only local utility. No network, OTP, lookup billing or claim that the number exists.

Read [the product reference](references/product.json) for the tool allowlist, input/output examples and current-availability entry. Examples are synthetic, never production evidence. Run `gridzen tools --product phone-format` to inspect the installed product before connecting.

Product and current access: https://gridzen.ai/tools/phone-format/

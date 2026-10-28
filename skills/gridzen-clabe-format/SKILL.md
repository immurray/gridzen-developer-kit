---
name: gridzen-clabe-format
description: Check an 18-digit CLABE checksum locally before starting an account verification. Use for mexico payout forms and payment-file import developers. A correct checksum does not prove that an account exists, can receive funds or belongs to a person.
license: MIT
metadata:
  compatibility: Python 3.11 or newer; gridzen-developer-kit >= 0.7.0. Offline utility.
  version: "1.0.0"
  product: clabe-format
---

# Check CLABE formatting

Run `gridzen tool clabe-format --input-file input.json` locally. The input JSON must contain only the documented fields. This utility sends no requests, records no telemetry and charges nothing. Do not turn syntax into an existence or ownership conclusion.

Inputs: An 18-digit CLABE, optionally separated by spaces or hyphens.

Return: structure_valid, checksum_valid and institution code. No live bank query or account-ownership assertion.

A correct checksum does not prove that an account exists, can receive funds or belongs to a person.

Read [the product reference](references/product.json) for the tool allowlist, input/output examples and current-availability entry. Examples are synthetic, never production evidence. Run `gridzen tools --product clabe-format` to inspect the installed product before connecting.

Product and current access: https://gridzen.ai/tools/clabe-format/

# Existing SPEI payment evidence: first integration

Run this dependency-free example in a clean Python 3.11+ environment:

```sh
python3 example.py
```

All seven cases are synthetic; no bank account, key or internet access is needed.
Success, name mismatch, official restriction, no record, unknown state and bounded
waiting remain separate. No fixture verifies a real person or initiates a transfer.

For the separate limited real trial, start at
https://gridzen.ai/console/payment-evidence/mx/cep . Reuse an existing verified
business account. Its email domain must match the declared business website.
Read authenticated `GET /console/api/payment-evidence/mx/cep/capabilities` first;
do not send merchant keys or transaction details to public research MCP tools.

## Map your own authorized transaction

| Field | Meaning |
|---|---|
| operation_date | Original transaction date, YYYY-MM-DD |
| tracking_key | SPEI trace from your independent payment record |
| amount_minor | Actual amount in centavos as an integer |
| issuer_code / receiver_code | Five-digit codes selected from the documented institution list |
| account | Recipient CLABE18; a card number is not accepted by this API |
| expected_name | Optional expected recipient, compared separately |
| authorization_reference | UUID identifying your authority to query this transaction |
| idempotency_key | UUID generated once per intended task; preserve after uncertain POST |

Copy the current full request from the live REST documentation:
https://gridzen.ai/console/payment-evidence/mx/cep/docs . It also requires explicit
authorization, business website, purpose and the exact terms version. Do not infer
all expected fields from an uploaded XML: expected transaction facts must be
independent of the document being checked.

POST returns a durable task ID. Persist it; read the same task with bounded backoff.
After an uncertain POST, query `/requests/{idempotency_key}` rather than creating a
replacement. Authentication/schema/quota errors need correction or waiting, not
blind retries. A source hold never authorizes alternate IPs, sessions or browsers.
The original is downloadable only by its owning tenant.

Keep original availability, valid signature, exact transaction binding and name
comparison as four decisions. A valid transaction with a different name still
requires the customer's own rules. History does not prove present account control.

## Optional measurement

Only after explicit project consent, include `X-GridZen-Project` with a registered
project UUID on creation. This links categorical completion evidence, not bank
fields. Independent-project validation is separate. Polls, downloads, duplicate
events and cached re-reads do not establish new adoption. Unshared offline use is
unknown, not zero users.

## Workflow systems

In an existing n8n integration, call the same API using credential storage; persist
the idempotency key and task ID before polling. Use a Wait node and a maximum read
counter, route review/not_found/blocked to an exception queue, and preserve pending
tasks after the counter expires. This CEP API currently uses polling; do not claim
it has a customer webhook. Do not import bank details or credentials into a public
workflow export. The existing identity workflow remains a separate hosted callback
flow; it is not a substitute for CEP transaction evidence.

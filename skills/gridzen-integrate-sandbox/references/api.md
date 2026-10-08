# Developer preview API

Base: `https://gridzen.ai/developers/api`. No credentials needed for public research and synthetic fixtures. This is separate from the production `/api/v1/decisions/` contract.

- `GET /coverage?country=ID&capability=bank_account_match`: dated research and source evidence.
- `POST /plan` with `{"country":"ID","event":"payout"}`: research requirements and sandbox request. Events: onboarding, payout, account_change.
- `POST /sandbox/verifications` with `{"country":"ID","capability":"bank_account_match","scenario":"timeout"}`: synthetic result.
- `GET /sandbox/verifications/{id}`: regenerate the deterministic fixture. IDs are not unique transaction IDs, secrets or evidence receipts.
- `GET /explain/SIMULATED_PROVIDER_TIMEOUT`: meaning and next step.
- Schema: `https://gridzen.ai/developers/api/openapi.json`.

Scenarios: match, mismatch, not_found, timeout, unsupported. Capability IDs: official_identity, commercial_identity, consented_eid, bank_account_match, consented_bank, cardholder_name, phone_identity. Use ISO-2 codes returned by coverage; do not infer global support from the sandbox.

```python
from gridzen_developer.client import Gridzen
api = Gridzen()
result = api.simulate('ID', 'bank_account_match', 'timeout')
assert result['simulated'] is True
assert result['verified'] is False
assert result['status'] == 'inconclusive'
```

Unexpected fields are rejected (422); unknown country/capability/fixture is rejected (400). Network errors and HTTP failures are integration failures, not verification outcomes. Do not retry indefinitely. Local core and local MCP work offline after installation; Python HTTP SDK sends only documented fixture parameters to Gridzen.

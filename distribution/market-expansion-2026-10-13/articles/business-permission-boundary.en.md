# Separate verification results from business permissions

Turn a verification result into a bounded application decision. Test account binding, explicit policy, duplicate events and rejection handling in a local fixture database. The permission shown in this walkthrough is a demo flag, not a real seller permission.

## What you will build

Turn a verification result into a bounded application decision. Test account binding, explicit policy, duplicate events and rejection handling in a local fixture database. The permission shown in this walkthrough is a demo flag, not a real seller permission.

## Run and inspect the three outcomes



```bash
for scenario in success reject unavailable; do
  curl -fsS https://gridzen.ai/console/api/quickstart/trial \
    -H 'Content-Type: application/json' \
    -d '{"task":"identity_onboarding","scenario":"'"$scenario"'"}'
done
```

## Expected output (synthetic)



```json
{
  "mode": "synthetic_fixture",
  "source": "local_response_trial",
  "task": "identity_onboarding",
  "scenario": "success",
  "verified": false,
  "real_person_verified": false,
  "billable": false,
  "amount_minor": 0,
  "upstream_calls": 0,
  "result": {
    "status": "Approved",
    "reason": "synthetic_scenario",
    "hosted_url": null
  },
  "business_decision": "caller_owned",
  "next_step": "connect_verified_account_for_persisted_sandbox",
  "production_available_from_this_trial": false
}
```

## Local state machine: restart, duplicates and deadlines

The local script uses only fixture identifiers. Run the code and tests in the linked repository; no account or provider key is required. Production callbacks need their own authorized signature verifier.

```bash
git clone https://github.com/immurray/gridzen-developer-kit.git
cd gridzen-developer-kit
python3 examples/verification_delivery/delivery.py identity --db /tmp/gridzen-local-delivery.sqlite3
python3 -m venv .venv
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest examples/verification_delivery/test_delivery.py -q
```

## Decide what your app does next

Treat success as a fixture branch, not real-person approval. For reject, show a recoverable message or review path. For unavailable, leave the outcome unknown and avoid silently granting permission. In a real integration, bind tenant, account and session; verify the provider notification, re-read authoritative state and apply your business policy before changing permissions.

## Limits and production handoff

No documents, phone numbers, credentials or real users are accepted by this trial. Production is a separate owner-approved free pilot. Current phone production provides basic validity only; hosted identity requires current confirmed free allowance and applicable supplier rights. Real payments remain disabled.

[Run the account-free synthetic trial](https://gridzen.ai/console/start?lang=en) · [Get integration guidance](https://gridzen.ai/console/assessment?lang=en)

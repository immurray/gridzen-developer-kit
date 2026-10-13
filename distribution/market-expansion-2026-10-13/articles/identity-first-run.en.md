# Your first identity onboarding sandbox run

Build the first identity onboarding result handler before collecting any document. This walkthrough uses an account-free synthetic response; it does not create a hosted provider session. Your application must keep verification decisions separate from seller permissions.

## What you will build

Build the first identity onboarding result handler before collecting any document. This walkthrough uses an account-free synthetic response; it does not create a hosted provider session. Your application must keep verification decisions separate from seller permissions.

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

## Decide what your app does next

Treat success as a fixture branch, not real-person approval. For reject, show a recoverable message or review path. For unavailable, leave the outcome unknown and avoid silently granting permission. In a real integration, bind tenant, account and session; verify the provider notification, re-read authoritative state and apply your business policy before changing permissions.

## Limits and production handoff

No documents, phone numbers, credentials or real users are accepted by this trial. Production is a separate owner-approved free pilot. Current phone production provides basic validity only; hosted identity requires current confirmed free allowance and applicable supplier rights. Real payments remain disabled.

[Run the account-free synthetic trial](https://gridzen.ai/console/start?lang=en) · [Get integration guidance](https://gridzen.ai/console/assessment?lang=en)

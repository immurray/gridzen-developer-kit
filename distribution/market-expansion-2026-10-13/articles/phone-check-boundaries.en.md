# Add a phone check without promising ownership

Add a pre-registration number check while keeping invalid numbers separate from unavailable results. A format or validity signal cannot prove ownership or SMS reachability. This walkthrough returns no line type and sends no OTP.

## What you will build

Add a pre-registration number check while keeping invalid numbers separate from unavailable results. A format or validity signal cannot prove ownership or SMS reachability. This walkthrough returns no line type and sends no OTP.

## Run and inspect the three outcomes



```bash
for scenario in success reject unavailable; do
  curl -fsS https://gridzen.ai/console/api/quickstart/trial \
    -H 'Content-Type: application/json' \
    -d '{"task":"signup_phone","scenario":"'"$scenario"'"}'
done
```

## Expected output (synthetic)



```json
{
  "mode": "synthetic_fixture",
  "source": "local_response_trial",
  "task": "signup_phone",
  "scenario": "success",
  "verified": false,
  "real_person_verified": false,
  "billable": false,
  "amount_minor": 0,
  "upstream_calls": 0,
  "result": {
    "source": "mock_transport",
    "mode": "simulation",
    "identity_match": "not_checked",
    "ownership": "not_checked",
    "checked_at": 1791873442.459438,
    "status": "completed",
    "number_valid": true
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

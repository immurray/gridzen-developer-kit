# Mexico identity/account result contract

Run with Python 3; no dependency, account, key, network or real identity data is required.

```sh
python3 examples/mx_identity_account/demo.py match
python3 examples/mx_identity_account/demo.py partial_name
python3 examples/mx_identity_account/demo.py name_conflict
python3 examples/mx_identity_account/demo.py missing_bank
```

These are fixed hypothetical B/C/D/unknown result fixtures, not a provider adapter, name-matching benchmark or live verification. All preserve verified=false, business_approval=false and zero provider/payment/charge counts. A real B is cross-source full-name agreement, not a direct bank CURP binding or proof of current control. Test your application's review, rejection and unavailable handling before a separately authorized production integration. Never import these fixtures as production evidence.

[Current task, prices, authenticated capabilities and production limits](../../docs/mexico-identity-account.md).

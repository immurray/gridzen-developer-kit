# mexico-pilot-scoper 1.0.0

Offline workflow instructions and a deterministic completeness helper. Synthetic
reference strings are not proof of rights, compliance or identity. No credentials,
third-party calls, provider checks, production decisions or approvals are made.

Install the Skill by copying this complete directory into your assistant's Skills
directory. See `SKILL.md` for its trigger and instructions. Python 3.11+ helper:

```sh
python evaluate.py < example-input.json
python -m unittest test_evaluate.py
```

`examples/` contains full input and expected output for normal, missing-evidence
and out-of-scope requests. A refusal example is the agent response contract;
`evaluate.py` itself rejects unknown fields with an error and exit code 2.
`agent-evals.json` provides real-assistant acceptance prompts and assertions.
Automated fixture checks do not test a language model's reasoning; execute the
same prompts in the intended client before claiming client-specific acceptance.

MIT; see `LICENSE`. Version: 1.0.0 (`spec.json`).

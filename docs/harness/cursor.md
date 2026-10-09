# cursor · GridZen 0.4.0

Python 3.11+; installed GridZen kit. Six Skills and five public MCP tools.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client cursor --project .
gridzen setup --client cursor --project . --apply
```

Windows activation: `.venv\Scripts\Activate.ps1` in PowerShell. If `venv` is
unavailable on Debian/Ubuntu, install `python3-venv` using the OS package manager.
Do not bypass the system Python protection. The first setup command previews;
`--apply` writes project-scoped files, merges the Gridzen server, backs up changed
config files and refuses different existing Gridzen entries or Skills. No accounts,
provider keys or model API credentials are installed.

MCP target: `.cursor/mcp.json`. Skill target: `.cursor/skills`.

Open this project in Cursor, review MCP settings and enable Gridzen. Project Skills are in .cursor/skills.

Try: “Plan a non-production Mexico payout pilot, identify missing permissions and
evidence, then test a synthetic provider timeout. Do not authorize a real payment.”
Expected: draft or missing-information output; simulated=true, verified=false,
provider_calls=0. Timeouts, missing evidence and unsupported remain inconclusive.
Tool names are get_coverage, plan_verification, create_sandbox_verification,
get_sandbox_verification, explain_result.

Actual acceptance is recorded in [compatibility.json](../../clients/compatibility.json);
configuration tests are not a claim of model or graphical-client acceptance.

Official sources (checked 2026-10-09):
- https://cursor.com/docs/mcp
- https://cursor.com/docs/skills

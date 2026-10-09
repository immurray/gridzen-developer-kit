# claude-desktop · GridZen 0.4.0

Python 3.11+; installed GridZen kit. Six Skills and five public MCP tools.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client claude-desktop --project .
gridzen setup --client claude-desktop --project . --apply
```

Windows activation: `.venv\Scripts\Activate.ps1` in PowerShell. If `venv` is
unavailable on Debian/Ubuntu, install `python3-venv` using the OS package manager.
Do not bypass the system Python protection. The first setup command previews;
`--apply` writes project-scoped files, merges the Gridzen server, backs up changed
config files and refuses different existing Gridzen entries or Skills. No accounts,
provider keys or model API credentials are installed.

MCP target: `gridzen-clients/claude-desktop/claude_desktop_config.json`. Skill target: `Six individual skill ZIPs; upload in Customize → Skills`.

Import/merge the generated MCP entry into Claude Desktop’s developer configuration, replacing no existing servers. Setup uses the absolute executable path from this installation. Restart Desktop. Upload the six individual Skill ZIPs in Customize → Skills; a multi-Skill bundle is not a single upload. Account plan, code execution and policy restrictions still apply.

Try: “Plan a non-production Mexico payout pilot, identify missing permissions and
evidence, then test a synthetic provider timeout. Do not authorize a real payment.”
Expected: draft or missing-information output; simulated=true, verified=false,
provider_calls=0. Timeouts, missing evidence and unsupported remain inconclusive.
Tool names are get_coverage, plan_verification, create_sandbox_verification,
get_sandbox_verification, explain_result.

Actual acceptance is recorded in [compatibility.json](../../clients/compatibility.json);
configuration tests are not a claim of model or graphical-client acceptance.

Official sources (checked 2026-10-09):
- https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop
- https://support.claude.com/en/articles/12512198-how-to-create-custom-skills

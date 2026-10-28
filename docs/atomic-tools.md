# One product, one task

The package has fourteen Skills. Eight new profiles narrow discovery to one business task; they do not grant merchant permissions or buy credit. The anonymous public HTTP MCP remains research/synthetic only.

| Profile | Result | Execution |
|---|---|---|
| `phone-format` | Explicit international syntax normalized | Local, free; no lookup or OTP |
| `clabe-format` | 18-digit shape and checksum | Local, free; no account/owner evidence |
| `result-explanation` | Documented status meaning and recovery guidance | Local, free; no business approval |
| `mx-cep` | Existing SPEI payment evidence, original/signature/binding states | Authorized merchant API; no new transfer |
| `mx-account-name` | Account-name evidence within the accepted quote | Authorized merchant API; explicit transfer permission when required |
| `mx-identity-account` | Bounded identity/account evidence grade | Authorized merchant API; not universal identity or account control |
| `ip-risk` | IP risk signals | Authorized merchant API; not a person or fraud verdict |
| `hosted-identity` | Hosted document/face journey and result | Authorized merchant API; the person completes it; new-person acceptance remains pending |

## Install and inspect

```bash
python3 -m venv .venv
.venv/bin/python -m pip install 'gridzen-developer-kit>=0.7.0'
.venv/bin/gridzen tools --product clabe-format
.venv/bin/gridzen skills
.venv/bin/gridzen setup --client codex --product clabe-format --project .
# Review the preview first:
.venv/bin/gridzen setup --client codex --product clabe-format --project . --apply
```

`--client` supports Codex, Claude Code, Claude Desktop, Cursor, VS Code, Copilot CLI, Gemini CLI, Cline, Roo Code and OpenCode. Use `gridzen setup --help` for exact IDs. Configuration generation is not GUI acceptance or autonomous model routing. Restart/trust the workspace; Desktop and Cline need manual import. Copilot CLI may need the generated file passed through its documented `--additional-mcp-config` flag.

Existing unrelated settings are retained. A differing existing GridZen entry is reported as a conflict; review its diff before replacing it. Setup does not write credentials. Choose one profile per tool need; do not install eight duplicate research servers.

## Offline CLI and MCP

Create `input.json` containing `{"phone":"+1 (202) 555-0123"}` then run:

```bash
.venv/bin/gridzen tool phone-format --input-file input.json
.venv/bin/gridzen mcp --product phone-format
```

The second command speaks MCP over stdio, so connect an MCP client rather than typing an ordinary conversation into that terminal. `examples/atomic_tools/check.py` runs all three offline examples without a provider or network call. Local utility execution is deliberately untracked even if research telemetry is enabled.

## Merchant profiles

Register or sign in at the product's Console entry, read capabilities, complete the required enrollment/terms and fund through an actually available payment route. A static catalog or Skill is not current supplier availability. Existing USD package prices and MXN quote rules apply; no new trial budget is created by this release. Online checkout can remain unavailable while approved offline funding is offered for specific MXN products.

Expose `GRIDZEN_API_KEY` to the local MCP process using your client’s private environment/secret facility. Optional `GRIDZEN_PROJECT_ID` is an already consented project ID. Never paste keys into model chat, source control, public issue bodies or example JSON. Shell-exported variables may not reach a GUI started from the dock; use its private launch environment or client-supported secret injection and confirm its MCP process can see the variable. The generated config contains no secret value.

```bash
.venv/bin/gridzen setup --client codex --product mx-cep --project .
# After review and credential setup:
.venv/bin/gridzen setup --client codex --product mx-cep --project . --apply
```

The user must authorize each paid/transfer workflow or provide a bounded existing spending policy. Preserve the accepted quote and request UUID after timeout. Read/recover the original task; do not create a new ID to make an uncertain charge disappear. A profile filters visible tools; the backend still owns merchant scope and billing. A merchant profile is not an automatic recharge facility.

## Independent promotion and attribution

Every profile has a stable page at `https://gridzen.ai/tools/<profile>/`. Link to that task, with a truthful source category (`developer_kit`, `dev`, `youtube`, `directory`, `referral`, `search`). The website requests consent before linking first-confirmed content to an account. The tool does not infer where a user came from or report offline execution as a customer.

Good demo: one input, one bounded result, one recovery case, one next step. Separate syntax checks, synthetic contract examples, live acceptance and independent customer adoption. Listings, installs and views are not paid usage. Community posts must follow the channel’s rules; materials being ready is not publication or approval.

Codex merchant profiles explicitly forward only the named GridZen environment variables using `env_vars`, following [the official MCP configuration reference](https://learn.chatgpt.com/docs/extend/mcp?surface=cli). Local profiles need neither variable. Other clients use their supported private process environment; no generated file embeds a key.

# Gridzen Developer Kit 0.4.0

Research for 198 countries/territories, a verification integration planner, five synthetic outcomes, an HTTP SDK, local MCP server and six Skills. **No live provider is enabled. No real person is verified.** The research snapshot is dated 2026-10-07, with source links and file hashes.

[中文指南](README.zh-CN.md) · [Guía en español](README.es.md)

## Try it

Public playground: https://gridzen.ai/developers/

Download `gridzen-developer-kit.zip`, extract it, then:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install './gridzen-developer-kit[mcp]'
gridzen coverage --country ID --capability bank_account_match
gridzen plan --country ID --event payout
gridzen simulate --country ID --capability bank_account_match --scenario timeout
python gridzen-developer-kit/examples/payout.py
```

Python 3.11+. CLI and MCP use the bundled offline catalog and fixtures; the Python HTTP client/example calls the public sandbox. Dependencies are downloaded only during installation. API reference: https://gridzen.ai/developers/api/openapi.json .

## MCP

Register a local stdio server in your MCP client. Use the absolute path to the installed executable; configuration syntax varies by client. A conventional `mcpServers` configuration is:

```json
{"mcpServers":{"gridzen":{"command":"/absolute/path/to/.venv/bin/gridzen-mcp","args":[]}}}
```

Tools: get_coverage, plan_verification, create_sandbox_verification, get_sandbox_verification, explain_result. All operate on local research or synthetic fixtures, with read-only/idempotent annotations. Public research/sandbox MCP endpoint: `https://gridzen.ai/developers/mcp` (Streamable HTTP, no account or API key). It has the same five tools and zero live providers. Remote usage sends the documented arguments to Gridzen; local stdio remains offline. Limits: 120 requests/minute per client address and 600/minute overall, returning HTTP 429 with Retry-After.

## Skills

Copy the individual directories from `skills/` into your compatible agent's project or user skill directory. Each entrypoint is `SKILL.md`; preserve its `references/` directory. No marketplace listing or automatic registration is implied.

## HTTP SDK

```python
from gridzen_developer.client import Gridzen
client = Gridzen()
plan = client.plan('ID', 'payout')
result = client.simulate('ID', 'bank_account_match', 'not_found')
assert result['status'] == 'inconclusive'
assert result['verified'] is False
```

Only documented country/event/capability/scenario fields are accepted. Never send identity numbers, bank accounts, documents or credentials to the sandbox. Simulation IDs encode fixtures and are not unique transaction identifiers. A synthetic match cannot authorize real users or payments. Research evidence is distinct from Gridzen availability or commercial permission.

## Repository checkout: local service and checks

```sh
python -m pip install '.[test,server]'
python -m pytest -q
python scripts/check_mcp.py
uvicorn gridzen_developer.server:app --host 127.0.0.1 --port 8030
```

Production uses an independent container at localhost:8030 proxied only under `/developers/`. See deploy/compose.yml and deploy/developers.conf. Removing that proxy file and stopping this container rolls back the preview; the existing API and Agent Company stacks are separate.

## Repository checkout: build distributions

`python scripts/build_downloads.py` creates allowlisted developer-kit and Skills ZIPs; it excludes tests, deployment files, private credentials and itself from recursive download packaging. `python scripts/build_catalog.py <repo>/docs/research/identity-verification/2026-10-07` refreshes the public research projection. Main repository report files remain the provenance source.

## Public distribution

<!-- mcp-name: ai.gridzen/verification -->

Source: https://github.com/immurray/gridzen-developer-kit . Install the Skills:

```sh
npx skills add immurray/gridzen-developer-kit
```

Install the tagged Python/MCP release from GitHub (Python 3.11+ and Git):

```sh
python -m pip install "gridzen-developer-kit[mcp] @ git+https://github.com/immurray/gridzen-developer-kit.git@v0.4.0"
```

PyPI 0.4.0 is published and verified. Install with `python -m pip install
gridzen-developer-kit`. See [the release tracker](distribution/STATUS.md) for
publication and installation evidence.

Remote client configuration (conventional JSON; client syntax may vary):

```json
{"mcpServers":{"gridzen":{"type":"http","url":"https://gridzen.ai/developers/mcp"}}}
```

For Claude Code: `claude mcp add --transport http gridzen https://gridzen.ai/developers/mcp`.
For Cursor: add the remote URL in its MCP settings. For portable Agent Plugins,
use the packaged `plugin.json` and `mcp.json`; the portable transport identifier
is `streamable-http`. Marketplace admission is separate from compatibility.

Original code and Skills: MIT. Research provenance and third-party rights:
[NOTICE.md](NOTICE.md). Support: open@gridzen.ai .

## Marketplace availability

Source, release downloads, the official MCP Registry entry and six Skills.sh pages are public. Docker catalog submission is awaiting review. See [the publication ledger](distribution/STATUS.md) for exact status and remaining platform steps.


## Six bundled Skills (0.4.0)

`python -m pip install gridzen-developer-kit` installs the CLI, stdio MCP dependencies
and all six Skill directories. Version 0.4.0 is published on
[PyPI](https://pypi.org/project/gridzen-developer-kit/0.4.0/); clean installation,
CLI, stdio MCP and all six bundled Skill directories were verified. No extra MCP
dependency installation is required.

```sh
gridzen coverage --country MX
gridzen skills
gridzen-mcp
```

Connect `gridzen-mcp` as your client's stdio server, or use the remote endpoint
`https://gridzen.ai/developers/mcp`. `gridzen skills` prints the installed directories;
copy a complete directory into your assistant's configured Skills directory to
activate it. Installing a wheel does not automatically activate a client's Skills.

The existing select/integrate/explain Skills remain available. Added offline
workflows, version 1.0.0: `mexico-pilot-scoper`, `payout-policy-designer`, and
`provider-rights-readiness`. Each includes MIT, README, complete response fixtures
and agent acceptance prompts. They make no third-party calls and grant no real
verification, legal approval or regulatory conclusion.

## Configure your assistant (v0.4.0)

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client all --project .
gridzen setup --client all --project . --apply
```

Use `--client` for Codex, Claude Code/Desktop, Cursor, VS Code/Copilot, Copilot CLI, Gemini CLI, Cline, Roo Code or OpenCode. Setup previews by default, merges existing unrelated settings, backs up changed configurations and refuses differing Gridzen entries or Skill files. No global client settings are modified. Native clients require workspace trust; Desktop and Cline require manual MCP import. Desktop produces six separately uploadable ZIPs. See [client-specific instructions](docs/harness/README.md) and [actual compatibility evidence](clients/compatibility.json). Configuration preparation is not model acceptance or real verification.

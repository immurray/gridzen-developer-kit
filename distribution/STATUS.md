# Distribution status — 2026-10-09

Version **0.4.0**. Six Skills, five research/synthetic MCP tools, ten-client project setup. Publication is not platform endorsement, live verification or evidence of external adoption.

| Channel | Actual status | Evidence / remaining step |
| --- | --- | --- |
| GitHub | Published | [v0.4.0](https://github.com/immurray/gridzen-developer-kit/releases/tag/v0.4.0); 15 assets. [Receipt](release-0.4.0.json). |
| PyPI | Published; installation verified | [0.4.0](https://pypi.org/project/gridzen-developer-kit/0.4.0/). [Receipt](pypi-publication-0.4.0.json). Clean venv, CLI, all-ten setup, six Skills, installed offline helpers and actual stdio passed. |
| Hosted MCP | Live 0.4.0 | [Endpoint](https://gridzen.ai/developers/mcp); five tools, five synthetic scenarios, retrieval/planning verified. Independent aggregate volume retained. |
| Official MCP Registry | Active, latest 0.4.0 | [Version record](https://registry.modelcontextprotocol.io/v0.1/servers/ai.gridzen%2Fverification/versions/0.4.0). [Receipt](registry-publication-0.4.0.json). Domain proof restored as a durable public file; no private key is distributed. |
| Docker MCP Catalog | Existing PR updated; awaiting review | [PR #5530](https://github.com/docker/mcp-registry/pull/5530), updated source head and description. Official validator/catalog generation passed. [Receipt](docker-update-0.4.0.json). Docker Desktop/gateway GUI remains untested. |
| Skills.sh | Canonical source ready; six listings unconfirmed | `npx skills add immurray/gridzen-developer-kit`. Prior three listing observations are historical; no claim that all six new listing pages or third-party installs are confirmed. |
| Smithery | Ready, login required; not submitted | [Publisher](https://smithery.ai/new) redirects to sign-in; current submission pack has six Skills and 0.4.0. |
| Glama | Ready, publisher account required; not submitted | [Directory](https://glama.ai/mcp/servers), glama.json, public repo and icon. Complete publisher session. |
| Cline Marketplace | Ready; client-specific acceptance required | [Contribution requirements](https://github.com/cline/mcp-marketplace). Cline GUI install acceptance was not run; cannot check its required successful-Cline-install assertion. |
| Cursor Marketplace | Package ready; not submitted | Publisher login and actual Cursor GUI acceptance remain pending. |
| Claude marketplace | Package/marketplace ready; not submitted | Existing account access and client acceptance remain pending. Claude Code here is not logged in; local MCP config is pending approval. |
| OpenAI plugin portal | Portable package ready; not submitted | Publisher identity/login requirements remain pending; Codex acceptance is not marketplace approval. |
| SkillsMP | Indexing unconfirmed | No verified listing receipt. |
| PulseMCP | Current submission availability unconfirmed | Recheck returned HTTP 403; historical pause is not asserted as today's policy. |
| MCP.so | Deferred | Paid route excluded. |
| Social media | Drafts ready, not posted | [English/Chinese/Spanish drafts](promotion.md). |

## Actual client acceptance

[Compatibility matrix](../clients/compatibility.json) records configuration tests separately from native discovery and model runs. Codex 0.159.0 used an existing ChatGPT subscription, explicitly inspected six Skills and called all five tools in a read-only synthetic run. MCP was supplied by a session override; automatic untrusted project loading and every Skill's autonomous routing were not tested. OpenCode 1.18.35 discovered six Skills and connected; Copilot CLI 1.0.94 discovered six Skills but its standalone MCP list did not detect project files. Gemini 0.63.0 requires workspace trust; Claude Code 2.1.295 requires approval/login. Desktop, Cursor, VS Code, Cline and Roo GUI acceptance remains untested on this Linux host. No paid model API calls or extra subscriptions.

[Model evidence](harness-acceptance-2026-10-09.json), [live browser evidence](harness-browser-live-2026-10-09.json): 36 checks, zero failures. Existing main website: 96 pages × two viewports, zero failures. Public source: 32 tests; installed three offline helper suites passed.

## Installation and promotion

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client all --project .
gridzen setup --client all --project . --apply
```

Use one client instead of all if desired. Desktop/Cline require manual import; native clients require workspace trust and tool permissions. Complete platform-specific login/acceptance before claiming marketplace submission. [Client instructions](../docs/harness/README.md), [submission copy](submissions.md), [website](https://gridzen.ai/developers/harnesses.html). The three drafting workflows remain 1.0.0 and make no third-party calls or authorization conclusions.

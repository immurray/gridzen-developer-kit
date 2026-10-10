# Distribution status — 2026-10-09

Version **0.5.0**: customer-task planning, fixed-category attempt/error evidence and explicit opt-in summaries. Six Skills and five MCP tools retained; no live routes or billing enabled.

| Surface | Current evidence |
| --- | --- |
| GitHub | [v0.5.0 published](https://github.com/immurray/gridzen-developer-kit/releases/tag/v0.5.0); package/Skill assets attached; plugin assets attached by the release-assets workflow. |
| PyPI | [0.5.0 published](https://pypi.org/project/gridzen-developer-kit/0.5.0/); official clean-install acceptance recorded in the main project. |
| Hosted developer service | 0.5.0 deployed; priority task plans, ten fixtures and opt-in retry accepted. |
| Official MCP Registry | Last verified latest remains 0.4.1. The domain publisher requires separate existing signing authorization; this change does not read or use its private key, and does not claim registry 0.5.0 publication. Existing 0.4.1 remains available. |

[New task contract and privacy boundaries](../docs/product-tasks-0.5.0.md). New tests are deterministic protocol/fixture checks, not evidence of independent customers or current model recommendation rates. Historical native-client evidence below is retained as historical.

## Historical 0.4.1 distribution record

Version **0.4.1**. Six Skills, five research/synthetic MCP tools, ten-client project setup. Publication is not platform endorsement, live verification or evidence of external adoption.

| Channel | Actual status | Evidence / remaining step |
| --- | --- | --- |
| GitHub | Published | [v0.4.1](https://github.com/immurray/gridzen-developer-kit/releases/tag/v0.4.1); 15 assets. [Receipt](release-0.4.1.json). |
| PyPI | Published; installation verified | [0.4.1](https://pypi.org/project/gridzen-developer-kit/0.4.1/). [Receipt](pypi-publication-0.4.1.json). Clean official-PyPI venv install, CLI, six Skills and actual stdio passed. |
| Hosted MCP | Live 0.4.1 | [Endpoint](https://gridzen.ai/developers/mcp); five tools, five synthetic scenarios, retrieval/planning verified. Independent aggregate volume retained. |
| Official MCP Registry | Active, latest 0.4.1 | [Version record](https://registry.modelcontextprotocol.io/v0.1/servers/ai.gridzen%2Fverification/versions/0.4.1). [Receipt](registry-publication-0.4.1.json). Domain proof restored as a durable public file; no private key is distributed. |
| Docker MCP Catalog | Existing PR updated; awaiting review | [PR #5530](https://github.com/docker/mcp-registry/pull/5530), updated source head and description. Official validator/catalog generation passed. [Receipt](docker-update-0.4.0.json). Docker Desktop/gateway GUI remains untested. |
| Skills.sh | Canonical source ready; six listings unconfirmed | `npx skills add immurray/gridzen-developer-kit`. Prior three listing observations are historical; no claim that all six new listing pages or third-party installs are confirmed. |
| Smithery | Ready, login required; not submitted | [Publisher](https://smithery.ai/new) redirects to sign-in; submission materials are available; login is still required. |
| Glama | Ready, publisher account required; not submitted | [Directory](https://glama.ai/mcp/servers), glama.json, public repo and icon. Complete publisher session. |
| Cline Marketplace | Ready; client-specific acceptance required | [Contribution requirements](https://github.com/cline/mcp-marketplace). Cline GUI install acceptance was not run; cannot check its required successful-Cline-install assertion. |
| Cursor Marketplace | Package ready; not submitted | Publisher login and actual Cursor GUI acceptance remain pending. |
| Claude marketplace | Package/marketplace ready; not submitted | Existing account access and client acceptance remain pending. Claude Code here is not logged in; local MCP config is pending approval. |
| OpenAI plugin portal | Portable package ready; not submitted | Publisher identity/login requirements remain pending; Codex acceptance is not marketplace approval. |
| SkillsMP | Indexing unconfirmed | No verified listing receipt. |
| PulseMCP | Current submission availability unconfirmed | Recheck returned HTTP 403; historical pause is not asserted as today's policy. |
| MCP.so | Deferred | Paid route excluded. |
| Social media | Drafts ready, not posted | [English/Chinese/Spanish drafts](promotion.md). |

## Project integration

The main website and developer pages now share navigation, footer, typography and language-aware product links. Homepage, Decision API docs and the Skills hub lead into client setup and the synthetic sandbox. [Design and verification](../docs/site-integration.md). Native client/model acceptance below was performed on 0.4.0 and is historical evidence; 0.4.1 does not claim new GUI or model runs. Docker Catalog source and validation remain at the previous submission; its review is pending.

## Actual client acceptance

[Compatibility matrix](../clients/compatibility.json) records configuration tests separately from native discovery and model runs. Codex 0.159.0 used an existing ChatGPT subscription, explicitly inspected six Skills and called all five tools in a read-only synthetic run. MCP was supplied by a session override; automatic untrusted project loading and every Skill's autonomous routing were not tested. OpenCode 1.18.35 discovered six Skills and connected; Copilot CLI 1.0.94 discovered six Skills but its standalone MCP list did not detect project files. Gemini 0.63.0 requires workspace trust; Claude Code 2.1.295 requires approval/login. Desktop, Cursor, VS Code, Cline and Roo GUI acceptance remains untested on this Linux host. No paid model API calls or extra subscriptions.

[Model evidence](harness-acceptance-2026-10-09.json), [live browser evidence](harness-browser-live-2026-10-09.json): 36 checks, zero failures. Existing main website: 96 pages × two viewports, zero failures. Public source: 34 tests; installed three offline helper suites passed.

## Installation and promotion

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client all --project .
gridzen setup --client all --project . --apply
```

Use one client instead of all if desired. Desktop/Cline require manual import; native clients require workspace trust and tool permissions. Complete platform-specific login/acceptance before claiming marketplace submission. [Client instructions](../docs/harness/README.md), [submission copy](submissions.md), [website](https://gridzen.ai/developers/harnesses.html). The three drafting workflows remain 1.0.0 and make no third-party calls or authorization conclusions.

Current presentation acceptance: [live integration](site-integration-live-2026-10-09.json), 72 page checks, 24 language-preserving round trips and 15 synthetic scenarios; [Company integration](company-integration-live-2026-10-09.json), six checks. Main-site live regression: 192 checks, zero failures.

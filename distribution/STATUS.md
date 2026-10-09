# Marketplace status — 2026-10-08

Version: **0.2.0**, public research and synthetic-test preview. Status records below
are publication evidence, not claims of independent users, platform endorsement,
live provider availability or production identity verification.

| Channel | Actual status | Evidence / next step |
| --- | --- | --- |
| GitHub source and Release | Published | [Repository](https://github.com/immurray/gridzen-developer-kit), [v0.2.0 assets](https://github.com/immurray/gridzen-developer-kit/releases/tag/v0.2.0). Public CI passed; clean installation from the released wheel passed. |
| Hosted MCP | Live | [Streamable HTTP endpoint](https://gridzen.ai/developers/mcp); five tools and all five synthetic outcomes tested with a real MCP client. |
| Official MCP Registry | Published, active | [Public version record](https://registry.modelcontextprotocol.io/v0.1/servers/ai.gridzen%2Fverification/versions/0.2.0). Publication receipt and unauthenticated lookup confirmed version 0.2.0 active on 2026-10-08. |
| Skills.sh | Three public skill pages | [Project](https://skills.sh/immurray/gridzen-developer-kit). One real Codex installation acceptance test installed all three Skills. This is not evidence of external adoption. |
| Docker MCP Catalog | Submitted; awaiting review | [Docker PR #5530](https://github.com/docker/mcp-registry/pull/5530). Official validator and catalog generation passed. No catalog availability is claimed before merge/release; Docker Desktop GUI/gateway acceptance remains untested. |
| Smithery | Submission prepared; not submitted | [Publish](https://smithery.ai/new) requires publisher login. Use the hosted MCP URL and copy in submissions.md. |
| Glama | Submission prepared; not submitted | [Directory](https://glama.ai/mcp/servers) Add Server requires an account; glama.json and repository/icon are ready. Complete any interactive account checks in the publisher session. |
| Cline | Not submitted; client acceptance pending | [Submission repository](https://github.com/cline/mcp-marketplace). Its Cline-specific install check has not been performed. Generic MCP tests are not a substitute. |
| Cursor | Package prepared; not submitted | [Publisher application](https://cursor.com/marketplace/publish) requires sign-in. Cursor package and metadata are ready; local client acceptance is still pending. |
| Claude | Package prepared; not submitted | Claude-format release ZIP and repository marketplace are ready. Publisher-account access and client acceptance are pending. |
| OpenAI plugins | Package prepared; not submitted | [Publisher portal](https://platform.openai.com/plugins). Portable plugin ZIP includes MCP + Skills; publisher identity/account requirements and client acceptance remain pending. |
| PyPI | Build verified; not published | Wheel/sdist are downloadable from GitHub. Configure PyPI Trusted Publishing before running publish-pypi.yml. No API token needs to be shared. |
| SkillsMP | Indexing unconfirmed | Public source is available for indexing. No confirmed Gridzen listing or submission receipt yet. |
| PulseMCP | Deferred | New submissions were paused when checked on 2026-10-08. |
| MCP.so | Deferred | Paid submission is outside the current free-channel rollout. |

## Install the Skills

```sh
npx skills add immurray/gridzen-developer-kit
```

- [gridzen-select-verification](https://skills.sh/immurray/gridzen-developer-kit/gridzen-select-verification)
- [gridzen-integrate-sandbox](https://skills.sh/immurray/gridzen-developer-kit/gridzen-integrate-sandbox)
- [gridzen-explain-verification](https://skills.sh/immurray/gridzen-developer-kit/gridzen-explain-verification)

## Publisher handoff

Use [submissions.md](submissions.md) for English descriptions, screenshots/icon
requirements, endpoint, support/privacy/terms links and the synthetic review prompt.
Use the matching ZIP from the GitHub release; retain each platform's actual receipt
and published URL before changing a row to published.

For PyPI, create a pending Trusted Publisher with:

- Project: `gridzen-developer-kit`
- GitHub owner: `immurray`
- Repository: `gridzen-developer-kit`
- Workflow: `publish-pypi.yml`
- Environment: `pypi`

Then run the manual workflow from the verified release commit. Do not change an
existing release tag or replace version 0.2.0 with different runtime code; new
runtime changes require a new version.


## 0.3.0 closeout — 2026-10-09

Local preparation: six bundled Skills; the three new workflows retain version
1.0.0, MIT, complete normal/missing/refusal fixtures and real-agent acceptance
prompts. Offline fixture contracts are tested, not a claim of live client or model
acceptance. Remote aggregate counter implementation and independent volume are
prepared. PyPI Trusted Publisher configuration is still awaiting account-owner
confirmation. No 0.3.0 publication or deployment is claimed by this preparation
entry. The official MCP Registry's existing active record remains 0.2.0 until a
separate new-version submission is confirmed. Existing marketplace PRs remain
subject to their reviewers; this source update is not platform endorsement.

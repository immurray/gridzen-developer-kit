# Marketplace status — 2026-10-09

Version: **0.3.0**, public research and synthetic-test preview. Status records below
are publication evidence, not claims of independent users, platform endorsement,
live provider availability or production identity verification.

| Channel | Actual status | Evidence / next step |
| --- | --- | --- |
| GitHub source and Release | Published | [Repository](https://github.com/immurray/gridzen-developer-kit), [v0.3.0 assets](https://github.com/immurray/gridzen-developer-kit/releases/tag/v0.3.0). Eight assets include six-Skill wheel/sdist/ZIPs and SHA256SUMS. Public CI and clean installation directly from the public Release wheel passed. |
| Hosted MCP | Live | [Streamable HTTP endpoint](https://gridzen.ai/developers/mcp); Version 0.3.0, same five tools; all five tools tested with a real remote client. Independent aggregate counter persists after restart; its five baseline calls were our acceptance test. |
| Official MCP Registry | Published, active | [Public version record](https://registry.modelcontextprotocol.io/v0.1/servers/ai.gridzen%2Fverification/versions/0.2.0). Publication receipt and unauthenticated lookup confirmed version 0.2.0 active on 2026-10-08. |
| Skills.sh | Three confirmed pages; six Skills in source | [Project](https://skills.sh/immurray/gridzen-developer-kit). One real Codex installation acceptance test installed all three Skills. This is not evidence of external adoption. |
| Docker MCP Catalog | Submitted; awaiting review | [Docker PR #5530](https://github.com/docker/mcp-registry/pull/5530). Official validator and catalog generation passed. No catalog availability is claimed before merge/release; Docker Desktop GUI/gateway acceptance remains untested. |
| Smithery | Submission prepared; not submitted | [Publish](https://smithery.ai/new) requires publisher login. Use the hosted MCP URL and copy in submissions.md. |
| Glama | Submission prepared; not submitted | [Directory](https://glama.ai/mcp/servers) Add Server requires an account; glama.json and repository/icon are ready. Complete any interactive account checks in the publisher session. |
| Cline | Not submitted; client acceptance pending | [Submission repository](https://github.com/cline/mcp-marketplace). Its Cline-specific install check has not been performed. Generic MCP tests are not a substitute. |
| Cursor | Package prepared; not submitted | [Publisher application](https://cursor.com/marketplace/publish) requires sign-in. Cursor package and metadata are ready; local client acceptance is still pending. |
| Claude | Package prepared; not submitted | Claude-format release ZIP and repository marketplace are ready. Publisher-account access and client acceptance are pending. |
| OpenAI plugins | Package prepared; not submitted | [Publisher portal](https://platform.openai.com/plugins). Portable plugin ZIP includes MCP + Skills; publisher identity/account requirements and client acceptance remain pending. |
| PyPI | Published 0.3.0; installation verified | [Package](https://pypi.org/project/gridzen-developer-kit/0.3.0/), [publish workflow](https://github.com/immurray/gridzen-developer-kit/actions/runs/37936347356), [receipt](pypi-publication-0.3.0.json). Clean venv installation by package name, CLI, actual stdio MCP, six Skill directories and three installed offline helpers passed. |
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

Published GitHub v0.3.0 and deployed remote MCP v0.3.0. All six Skill directories
are present in wheel, sdist and ZIPs. The three new workflows retain version 1.0.0,
MIT, README, complete normal/missing/refusal fixtures and agent acceptance prompts.
Offline fixture contracts and installed helpers passed; this is not a claim of
live model reasoning or client-specific acceptance for the new workflows.

Evidence: [release](https://github.com/immurray/gridzen-developer-kit/releases/tag/v0.3.0),
[release CI](https://github.com/immurray/gridzen-developer-kit/actions/runs/37917716580).
Clean venv installation directly from the public Release wheel, CLI, six Skill
asset discovery, installed workflow helpers, actual stdio MCP and remote five-tool
acceptance passed. Public tests: 27, plus 18 original workflow helper tests.
Existing website regression: 96 pages × 2 viewports, zero failures locally and live.
The remote counter volume retained five acceptance calls after restart.

**PyPI 0.3.0 is published and verified.** The owner confirmed Trusted Publisher
configuration, and both workflow build and publish jobs succeeded. A clean venv
installed `gridzen-developer-kit` directly from PyPI; CLI, actual stdio MCP, all six
Skill assets and the three installed offline helpers passed. See the publication
receipt above. PyPI Stats updates independently and may not yet have download
statistics for this new project; missing statistics remain null, not zero.
The official MCP Registry remains active at 0.2.0. Existing marketplace PRs retain their review
status; public source and our own installation checks are not platform approval
or external adoption evidence. The new three Skills.sh listings are unconfirmed.

New workflows:
- [mexico-pilot-scoper 1.0.0](../skills/mexico-pilot-scoper/README.md)
- [payout-policy-designer 1.0.0](../skills/payout-policy-designer/README.md)
- [provider-rights-readiness 1.0.0](../skills/provider-rights-readiness/README.md)

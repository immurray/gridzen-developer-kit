# GridZen developer kit — 0.7.1

Public research and synthetic sandbox, not real identity verification or payment authorization. Python 3.11+.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client all --project .
gridzen setup --client all --project . --apply
```

Select one client instead of all: codex, claude-code, claude-desktop, cursor, vscode, copilot-cli, gemini-cli, cline, roo-code, opencode. Setup is project-scoped and previews by default. It refuses differing existing Gridzen config/Skills, backs up changed configs and preserves unrelated values. Trust the workspace and review tool permissions. Desktop/Cline require manual MCP import; Desktop produces 14 individual Skill ZIPs for manual upload when supported by the account.

Remote MCP: https://gridzen.ai/developers/mcp (no API key). Offline stdio: absolute installed gridzen-mcp path. Five tools: get_coverage, plan_verification, create_sandbox_verification, get_sandbox_verification, explain_result. The 14 Skills comprise 6 research/workflow Skills and 8 single-task profiles. Of the 8 profiles, 3 run offline and 5 merchant profiles require separate authorization. Five public MCP tools provide research/synthetic operations. No live identity verification.

Instructions: https://gridzen.ai/developers/harnesses.html
Actual test record: clients/compatibility.json. Config preparation is distinct from client/model acceptance. No claim of platform endorsement. Remote MCP records only date/tool/count aggregates; stdio is uncounted.

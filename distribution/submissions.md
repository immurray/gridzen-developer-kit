# Gridzen marketplace submission pack — 0.2.0

Canonical repository: https://github.com/immurray/gridzen-developer-kit
Website: https://gridzen.ai/developers/
Remote MCP: https://gridzen.ai/developers/mcp
Transport: Streamable HTTP; no account, API key or OAuth needed for this public preview.
Support: https://gridzen.ai/developers/support.html
Privacy: https://gridzen.ai/developers/privacy.html
Terms: https://gridzen.ai/developers/terms.html
License: MIT for original code and Skills; see NOTICE.md for research sources.
Icon: https://gridzen.ai/developers/icon.png (400 × 400)

## English listing copy

Name: Gridzen Verification
Short description: Plan and test verification

Gridzen helps developers research country-specific identity, bank-account and
phone verification approaches, plan an integration, and test failure handling
with five synthetic outcomes. It includes source-linked research for 198
countries/territories, five MCP tools and three Agent Skills. All live provider
routes are disabled; research coverage is not commercial availability. No real
person is verified and no personal data or credentials are needed.

Use cases:
1. Research verification options and access requirements for a target country.
2. Prepare an onboarding, payout or account-change integration plan.
3. Exercise match, mismatch, not_found, timeout and unsupported outcomes.
4. Keep missing evidence and upstream failures distinct from identity mismatches.

Starter prompt: Plan a payout verification integration for Indonesia, then test
a provider timeout. Explain what still needs confirmation for a real pilot.

## Review instructions

Connect to the remote URL and list tools. Expect get_coverage, plan_verification,
create_sandbox_verification, get_sandbox_verification and explain_result.
Call create_sandbox_verification with country=ID, capability=bank_account_match,
scenario=timeout. Expect simulated=true, verified=false, provider_calls=0 and
status=inconclusive. Retrieve the fixture with get_sandbox_verification using
its returned ID. No test account is required. Do not send personal information.

## Platform routes

- Official MCP Registry: server.json; domain namespace ai.gridzen/verification.
- Skills.sh: install canonical skills with `npx skills add immurray/gridzen-developer-kit`;
  discovery/ranking follows real installation telemetry, not a manual review receipt.
- Smithery: submit the remote URL at https://smithery.ai/new .
- Glama: submit the GitHub repository via Add MCP Server; glama.json records maintainer.
- Cline: issue at https://github.com/cline/mcp-marketplace . Include the repository,
  icon and use cases above. Complete the required Cline-specific installation test
  before asserting it passed; general MCP client testing is not that test.
- Cursor: https://cursor.com/marketplace/publish . Portable root manifest and
  Cursor compatibility manifest are included. Complete local Cursor acceptance.
- Claude: developer portal linked from https://claude.com/resources/articles/build-plugins-for-claude .
  The release contains a Claude-format package and a repo marketplace.
- OpenAI: https://platform.openai.com/plugins . Use the portable plugin ZIP with
  both MCP and Skills in the first submission. Confirm verified publisher identity.
- Docker: https://github.com/docker/mcp-registry . Remote Streamable HTTP entries
  are accepted without a container image. Submit server.yaml, tools.json (`[]`)
  and readme.md after official validator and catalog generation checks.
- SkillsMP: https://skillsmp.com/ . Check actual indexing after the public release.
- PulseMCP: https://www.pulsemcp.com/servers . New submissions paused when checked
  2026-10-08; recheck before attempting submission.
- MCP.so: https://mcp.so/Submit?type=server . Current paid form is deferred.

Packaging, schema validation and generic MCP acceptance do not mean a platform
has reviewed, approved or published this project. Record each result separately.

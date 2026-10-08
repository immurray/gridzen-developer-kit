# Install Gridzen developer tools

Remote MCP: https://gridzen.ai/developers/mcp (Streamable HTTP, no API key).
Configure a remote HTTP MCP connection using your client's supported syntax.
Call tools/list; expect five tools. Call create_sandbox_verification with
country ID, capability bank_account_match, scenario timeout. Expect simulated=true,
verified=false, status=inconclusive. No personal data is required or supported.

Skills: npx skills add immurray/gridzen-developer-kit

Offline option: Python 3.11+ and Git, then install the tagged package:
python -m pip install "gridzen-developer-kit[mcp] @ git+https://github.com/immurray/gridzen-developer-kit.git@v0.2.0"
Register the absolute path of gridzen-mcp as a local stdio command.

Do not configure production credentials, change firewall rules, disable client
security settings or start paid provider calls. Research is not commercial coverage.
Docs: https://gridzen.ai/developers/quickstart.html

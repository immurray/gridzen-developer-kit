# Marketplace release operations

Canonical public repository: https://github.com/immurray/gridzen-developer-kit
Registry namespace: ai.gridzen/verification
Remote MCP: https://gridzen.ai/developers/mcp

Use scripts/export_public.py to export only approved developer files into a
fresh checkout of the public repository. Review the diff before pushing. Never
copy the private repository, deployment credentials or operational database.

Build: python scripts/build_downloads.py && python scripts/build_plugins.py
Validate: python scripts/validate_distribution.py
Test: python -m pytest -q tests && python scripts/check_mcp.py
Remote acceptance: python scripts/check_remote.py https://gridzen.ai/developers/mcp

GitHub release files: wheel, sdist, portable plugin ZIP, Claude plugin ZIP,
Skills ZIP and SHA256SUMS. PyPI publication is a separate manual workflow after
configuring the repository as a Trusted Publisher in the publisher's PyPI account.
No PyPI status is inferred from building a wheel or triggering a workflow.

Official registry: mcp-publisher validate server.json; authenticate with the
Gridzen domain HTTP proof, then mcp-publisher publish server.json. Private signing
keys and registry tokens must remain outside this checkout and all distributions.

Other markets: see submissions/ for copy-ready material. Record the actual
submission receipt and published URL in the private release ledger. Mark a channel
live only after its listing is publicly visible and installation is verified.

# Product and developer-site integration

The primary site publishes `/assets/site-shell.json` from its existing navigation/footer generator. The developer service consumes this public three-language shell, including the original stripe mark, product navigation and footer links. It never imports private source code, credentials or customer records. A reviewed public shell snapshot is bundled as a fallback at `/developers/site-shell.json`. Shared site design tokens come from `/assets/site.css`.

The developer subnavigation is local to the tools area. The main navbar points back to the Decision API, Provider Packs, use cases, research, guides and developers; Skills stays in the footer. Homepage, documentation and Skills entry points link to assistant setup, synthetic testing and product evaluation with the chosen language. The team-service compatibility bridge uses the same public shell.

Public tools remain research/synthetic previews. Local Decision API evaluation and its event/response contract are distinct from the public developer sandbox; no live provider access or private engine is implied by connecting an assistant. The six Skills remain six; the three offline workflows keep version 1.0.0.

Version 0.4.1 changes presentation, language-safe navigation, public entry points and the sandbox UI default market (MX). Existing client/model acceptance is recorded for 0.4.0; it is not claimed as newly rerun for every client.

Browser check: `PLAYWRIGHT_BROWSERS_PATH=/path/to/browsers python scripts/test_project_integration_browser.py https://gridzen.ai`. It compares real main/developer navigation and shell style, checks the homepage animation, all ten client selectors, footer Skills, four screen sizes and three-language round trips.

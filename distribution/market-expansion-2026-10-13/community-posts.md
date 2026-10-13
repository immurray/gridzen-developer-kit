# Channel-specific publication drafts — not posted

## Show HN

Title: Show HN: Test identity onboarding and callback recovery without an account
URL: https://gridzen.ai/console/start?lang=en

We built GridZen's account-free response trial and SQLite delivery fixtures for developers building seller onboarding. You can run success, rejection and unavailable outcomes without entering a document, a face image or a provider credential. The local example exercises duplicate callbacks, binding, deadlines and permission decisions. There is an importable n8n workflow too.

This is synthetic integration testing. Public MCP/Skills do not verify real people, send OTP or approve production. Our controlled production pilot is separate and real payments are off. I would like feedback from developers implementing verification-to-permission flows: which missing recovery branch makes this unusable in your app?

Code: https://github.com/immurray/gridzen-developer-kit/tree/main/examples/verification_delivery

## n8n community / approved project-showcase category

Title: A local identity-delivery fixture: duplicate callbacks, deadline recovery and no credentials

I made an importable workflow that reuses a tiny SQLite fixture service rather than duplicating the permission state machine inside n8n. A callback applies the bound event, duplicates do not grant twice, and a bounded Wait checks the session deadline. Transport errors remain unknown.

Workflow/code: https://github.com/immurray/gridzen-developer-kit/tree/main/examples/n8n

Synthetic only, not a live KYC integration. I maintain GridZen. I would value technical feedback on import portability and error recovery. Read the current category rules before posting; do not DM members or post the same promotion across unrelated threads.

## Reddit / verified project-showcase category

Title: I built an account-free test for signup-phone and identity onboarding branches

If you are building a marketplace, a successful provider response is only one part of onboarding. Your app still needs to bind the account, handle unavailable results and avoid granting twice on repeated notifications.

Demo: https://gridzen.ai/console/start?lang=en
Code: https://github.com/immurray/gridzen-developer-kit

I maintain this project. The demo is synthetic and collects no real identity data. What recovery step is hardest in your current integration? No testimonial or customer adoption is claimed.

## LinkedIn / X

Identity Approved ≠ seller permission granted. We published a small, runnable example covering account binding, duplicate events and deadline recovery. Try the account-free synthetic response flow, then inspect the SQLite fixture or n8n template. No documents, provider keys or signup required for the examples. Real verification is separate.

https://gridzen.ai/console/start?lang=en

## YouTube

Title: Identity onboarding: test success, rejection and unavailable before production

Description: This screen recording shows GridZen's account-free **synthetic** trial. No person is verified, no provider session is created, no OTP is sent and no payment occurs. The repository contains the corresponding callback/permission fixture and n8n workflow. Production requires a separately approved route.

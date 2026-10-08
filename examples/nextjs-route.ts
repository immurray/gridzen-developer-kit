// Copy to app/api/verification-sandbox/route.ts in a Next.js app.
// Synthetic fixtures only. Never use this route to authorize real payouts.
export async function POST(request: Request) {
  let input: unknown;
  try { input = await request.json(); } catch {
    return Response.json({ error: "Invalid JSON" }, { status: 400 });
  }
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    return Response.json({ error: "Expected a scenario object" }, { status: 400 });
  }
  const data = input as Record<string, unknown>;
  const scenarios = ["match", "mismatch", "not_found", "timeout", "unsupported"];
  if (typeof data.scenario !== "string" || !scenarios.includes(data.scenario) || Object.keys(data).some(k => k !== "scenario")) {
    return Response.json({ error: "Only a synthetic scenario is accepted" }, { status: 400 });
  }
  const upstream = await fetch("https://gridzen.ai/developers/api/sandbox/verifications", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ country: "ID", capability: "bank_account_match", scenario: data.scenario }),
    signal: AbortSignal.timeout(10_000),
    cache: "no-store",
  }).catch(() => null);
  if (!upstream?.ok) return Response.json({ status: "inconclusive", error: "sandbox_unavailable" }, { status: 502 });
  const result = await upstream.json();
  if (result.simulated !== true || result.verified !== false) {
    return Response.json({ error: "Unexpected sandbox response" }, { status: 502 });
  }
  return Response.json(result);
}

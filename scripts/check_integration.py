"""Check the public synthetic contract; never sends PII or merchant credentials."""
import argparse
import json
import sys
from urllib.request import Request, urlopen

BASE = "https://gridzen.ai/developers/api"
SCENARIOS = ("match", "mismatch", "not_found", "timeout", "unsupported")


def validate(result, scenario):
    expected = "inconclusive" if scenario in SCENARIOS[2:] else "completed"
    checks = {
        "simulated": result.get("simulated") is True,
        "unverified": result.get("verified") is False,
        "no_live_route": result.get("live_available") is False,
        "no_provider_calls": result.get("provider_calls") == 0,
        "scenario": result.get("fixture_outcome") == scenario,
        "status": result.get("status") == expected,
        "no_identity_evidence": result.get("evidence") == [],
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError("Unexpected sandbox contract: " + ", ".join(failed))
    return {"scenario": scenario, "status": expected, "passed": True}


def run(call):
    return [validate(call(scenario), scenario) for scenario in SCENARIOS]


def http_call(scenario):
    payload = {"country": "ID", "capability": "bank_account_match", "scenario": scenario}
    request = Request(BASE + "/sandbox/verifications", data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json", "User-Agent": "GridzenContractCheck/1"})
    with urlopen(request, timeout=10) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Check installed Developer Kit core, without network")
    args = parser.parse_args()
    try:
        if args.offline:
            from gridzen_developer.core import simulate
            call = lambda scenario: simulate("ID", "bank_account_match", scenario)
        else:
            call = http_call
        results = run(call)
        print(json.dumps({"mode": "offline" if args.offline else "public_http",
                          "live_verified": False, "checks": results}, indent=2))
    except Exception as error:
        # Do not emit arbitrary upstream bodies, credentials or raw user data.
        print(json.dumps({"passed": False, "error_type": type(error).__name__}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

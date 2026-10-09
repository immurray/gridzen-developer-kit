#!/usr/bin/env python3
"""Offline completeness/design helper. No network, credentials or personal-data checks."""
import json
from pathlib import Path
import sys


def evaluate(data, spec):
    if not isinstance(data, dict):
        raise ValueError('Input must be a JSON object')
    allowed = set(spec['fields'])
    if set(data) - allowed:
        raise ValueError('Unexpected fields; use non-sensitive references only')
    for name, value in data.items():
        if name == 'non_production':
            if not isinstance(value, bool):
                raise ValueError('non_production must be a boolean')
        elif name == 'required_signals':
            if not isinstance(value, list) or not value or len(value) > 20 or any(not isinstance(x, str) or not x.strip() or len(x) > 100 for x in value):
                raise ValueError('required_signals must be a nonempty list of short signal names')
        elif not isinstance(value, str) or len(value) > 240:
            raise ValueError('Fields must be short reference strings')
    missing = [name for name in spec['fields'] if name not in data or data[name] is None or (isinstance(data[name], str) and not data[name].strip())]
    blockers = []
    mode = spec['name']
    if mode != 'provider-rights-readiness' and data.get('event') not in (None, 'payout'):
        blockers.append('payout_event_required')
    if 'country' in data and (not isinstance(data['country'], str) or len(data['country'].strip()) != 2 or not data['country'].strip().isascii() or not data['country'].strip().isalpha()):
        blockers.append('iso2_country_required')
    if mode == 'mexico-pilot-scoper':
        if data.get('country', '').strip().upper() != 'MX':
            blockers.append('mexico_scope_required')
        if data.get('non_production') is not True:
            blockers.append('non_production_required')
    output = {
        'status': 'needs_information' if missing or blockers else 'draft_for_review',
        'missing': missing, 'blockers': blockers,
        'approval_granted': False, 'network_calls': False,
        'limitations': 'Completeness only; references are not verified. No legal approval, identity check, pilot activation or production decision.'
    }
    if mode == 'payout-policy-designer':
        output['policy_draft'] = {
            'event': 'payout', 'country': data.get('country'),
            'required_signals': data.get('required_signals', []),
            'missing_required_evidence': 'hold_in_caller_and_review',
            'provider_unavailable': 'handle_http_failure_in_caller_and_review',
            'fallback': 'only_a_separately_authorized_route',
            'allow': 'only_after_required_evidence_and_reviewed_policy_are_satisfied',
            'review_owner': data.get('review_owner'),
            'deployed': False
        }
    return output


if __name__ == '__main__':
    try:
        data = json.load(sys.stdin)
        spec = json.loads((Path(__file__).parent / 'spec.json').read_text())
        print(json.dumps(evaluate(data, spec), ensure_ascii=False, indent=2))
    except (ValueError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}))
        sys.exit(2)

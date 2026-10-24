"""Offline contract fixtures only: no keys, personal data, network or billing."""
import argparse
import json
from pathlib import Path

if __name__ == '__main__':
    cases=json.loads(Path(__file__).with_name('fixtures.json').read_text())
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case',nargs='?',default='match',choices=cases)
    response=cases[parser.parse_args().case]
    assert response['mode']=='synthetic' and response['verified'] is False
    assert response['provider_calls']==response['payments_created']==response['charged_minor']==0
    print(json.dumps(response,indent=2))

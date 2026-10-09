"""Read-only last-seven-UTC-days remote MCP aggregate report."""
import argparse
import json
import os
from gridzen_developer.usage import summarize

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default=os.environ.get('GRIDZEN_MCP_EVENTS_DB'))
    args = parser.parse_args()
    print(json.dumps(summarize(args.db), indent=2))

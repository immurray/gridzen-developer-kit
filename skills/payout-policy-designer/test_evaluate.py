"""Offline helper evaluation; does not evaluate AI reasoning or legal adequacy."""
import json
from pathlib import Path
import unittest
from evaluate import evaluate

HERE=Path(__file__).parent
SPEC=json.loads((HERE/'spec.json').read_text())
EXAMPLE=json.loads((HERE/'example-input.json').read_text())

class HelperEvaluation(unittest.TestCase):
    def test_complete_input_remains_a_draft(self):
        self.assertEqual(evaluate(EXAMPLE,SPEC)['status'],'draft_for_review')
    def test_missing_input_is_not_ready(self):
        self.assertEqual(evaluate({},SPEC)['status'],'needs_information')
    def test_unknown_fields_are_rejected(self):
        with self.assertRaises(ValueError):evaluate(dict(EXAMPLE,api_key='synthetic-secret'),SPEC)
    def test_no_approval_or_network_call(self):
        result=evaluate(EXAMPLE,SPEC)
        self.assertFalse(result['approval_granted']);self.assertFalse(result['network_calls'])
    def test_country_format_is_checked(self):
        self.assertIn('iso2_country_required',evaluate(dict(EXAMPLE,country='invalid'),SPEC)['blockers'])
    def test_required_field_or_mode(self):
        data=dict(EXAMPLE)
        if SPEC['name']=='mexico-pilot-scoper':
            data['non_production']=False
            self.assertIn('non_production_required',evaluate(data,SPEC)['blockers'])
        elif SPEC['name']=='payout-policy-designer':
            data['required_signals']=[]
            with self.assertRaises(ValueError):evaluate(data,SPEC)
        else:
            data.pop('downstream_use_reference')
            self.assertIn('downstream_use_reference',evaluate(data,SPEC)['missing'])

if __name__=='__main__':unittest.main()

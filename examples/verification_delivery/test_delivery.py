import tempfile
import unittest
from pathlib import Path
from delivery import Identity, phone


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'state.sqlite'
        self.identity = Identity(self.path)
        self.identity.create()

    def tearDown(self):
        self.tmp.cleanup()

    def test_phone_branches(self):
        for branch in ('normal','unknown','provider_failure','otp'):
            result = phone(branch)
            self.assertFalse(result['otp_sent'])
            self.assertFalse(result['live_line_type_available'])
        self.assertIsNone(phone('unknown')['valid'])
        self.assertEqual(phone('otp')['state'], 'unsupported')

    def test_policy_required(self):
        self.assertFalse(self.identity.event('fixture-approved')['permission_granted'])

    def test_bindings(self):
        for field in ('tenant','subject','session'):
            with self.assertRaisesRegex(ValueError, 'BINDING_MISMATCH'):
                self.identity.event('fixture-bad', **{field:'fixture-other'}, policy=True)
        self.assertEqual(self.identity.read()['grant_count'], 0)

    def test_reject_live_and_unverified_sources(self):
        for kwargs in ({'mode':'production'}, {'source':'browser_redirect'}):
            with self.assertRaisesRegex(ValueError, 'SIGNATURE_VERIFIER_NOT_IMPLEMENTED'):
                self.identity.event('fixture-bad', **kwargs)

    def test_duplicate_and_late_events(self):
        self.identity.event('fixture-approved', policy=True)
        self.identity.event('fixture-approved', policy=True)
        result = self.identity.event('fixture-late', status='In Progress')
        self.assertEqual((result['status'], result['grant_count']), ('approved',1))

    def test_restart(self):
        self.identity.event('fixture-review', status='In Review')
        restored = Identity(self.path)
        self.assertEqual(restored.read()['status'], 'review')
        self.assertEqual(restored.event('fixture-approved', policy=True)['grant_count'], 1)

    def test_verified_correction_can_revoke_fixture_permission(self):
        self.identity.event('fixture-approved',policy=True)
        corrected=self.identity.event('fixture-correction',status='Declined',policy=True)
        self.assertFalse(corrected['permission_granted'])
        self.assertEqual(corrected['status'],'declined')
        self.assertEqual(corrected['grant_count'],1)

    def test_timeout_recovery(self):
        result = Identity(self.path).recover(now=61)
        self.assertEqual(result['status'], 'expired')
        self.assertFalse(self.identity.event('fixture-late', policy=True)['permission_granted'])

    def test_unknown_and_failure(self):
        result = self.identity.event('fixture-unknown', status='new-provider-status')
        self.assertEqual(result['status'], 'unknown')
        self.assertFalse(result['permission_granted'])


if __name__ == '__main__':
    unittest.main()

"""Dependency-free synthetic delivery example, never a live provider adapter."""
import argparse
import json
import sqlite3
from pathlib import Path

MODE = 'synthetic_fixture'


def phone(branch):
    results = {
        'normal': {'state': 'simulated', 'valid': True, 'line_type': 'mobile', 'next': 'continue_customer_policy'},
        'unknown': {'state': 'unknown', 'valid': None, 'line_type': None, 'next': 'review_or_existing_otp'},
        'provider_failure': {'state': 'unknown', 'valid': None, 'line_type': None, 'next': 'bounded_retry_then_review'},
        'otp': {'state': 'unsupported', 'valid': None, 'line_type': None, 'next': 'customer_otp_provider'},
    }
    if branch not in results:
        raise ValueError('UNSUPPORTED_FIXTURE')
    return {'mode': MODE, 'branch': branch, 'otp_sent': False,
            'live_line_type_available': False, **results[branch]}


class Identity:
    """SQLite persists fixture transitions; caller supplies a verified fixture channel.

    There is no production signature verifier. Only synthetic events are accepted.
    Permission grants here are local fixture records, never real user permissions.
    """
    def __init__(self, path):
        self.path = str(path)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, tenant TEXT NOT NULL, subject TEXT NOT NULL, status TEXT NOT NULL, deadline INTEGER NOT NULL, granted INTEGER NOT NULL DEFAULT 0, grants INTEGER NOT NULL DEFAULT 0)')
            db.execute('CREATE TABLE IF NOT EXISTS events (session TEXT NOT NULL, event TEXT NOT NULL, PRIMARY KEY(session,event))')
            columns={r[1] for r in db.execute('PRAGMA table_info(sessions)')}
            if 'policy_version' not in columns:db.execute('ALTER TABLE sessions ADD COLUMN policy_version INTEGER NOT NULL DEFAULT 1')
            if 'allow_action' not in columns:db.execute('ALTER TABLE sessions ADD COLUMN allow_action INTEGER NOT NULL DEFAULT 1')

    def connect(self):
        return sqlite3.connect(self.path, timeout=5)

    def create(self, session='fixture-session', tenant='fixture-tenant', subject='fixture-user', now=0, timeout=60):
        if not all(x.startswith('fixture-') for x in (session, tenant, subject)) or timeout < 1 or timeout > 3600:
            raise ValueError('SYNTHETIC_IDENTIFIERS_REQUIRED')
        with self.connect() as db:
            db.execute('INSERT INTO sessions(id,tenant,subject,status,deadline) VALUES(?,?,?,?,?)', (session, tenant, subject, 'pending', now + timeout))
        return {'mode': MODE, 'state': 'simulated', 'session': session,
                'hosted_link': 'https://example.invalid/verify/' + session,
                'link_executable': False, 'next': 'send_real_provider_link_only_after_authorization'}

    def read(self, session='fixture-session'):
        with self.connect() as db:
            row = db.execute('SELECT status,deadline,granted,grants,policy_version,allow_action FROM sessions WHERE id=?', (session,)).fetchone()
        if row is None:
            raise ValueError('SESSION_NOT_FOUND')
        return {'mode': MODE, 'session': session, 'status': row[0], 'deadline': row[1],
                'permission_granted': bool(row[2]), 'grant_count': row[3], 'live_permission_changed': False,
                'policy_version':row[4],'allow_action':bool(row[5])}

    def event(self, event, session='fixture-session', tenant='fixture-tenant', subject='fixture-user', status='Approved', mode=MODE, source='fixture_callback', policy=False, now=1):
        if mode != MODE or source != 'fixture_callback':
            raise ValueError('PRODUCTION_SIGNATURE_VERIFIER_NOT_IMPLEMENTED')
        if not isinstance(event, str) or not event.startswith('fixture-') or len(event) > 100:
            raise ValueError('SYNTHETIC_EVENT_REQUIRED')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT tenant,subject,status,deadline,allow_action FROM sessions WHERE id=?', (session,)).fetchone()
            if row is None or row[:2] != (tenant, subject):
                raise ValueError('BINDING_MISMATCH')
            if db.execute('SELECT 1 FROM events WHERE session=? AND event=?', (session, event)).fetchone():
                return self.read(session)
            if row[2]=='approved' and status=='Declined':
                db.execute('INSERT INTO events VALUES(?,?)',(session,event))
                db.execute("UPDATE sessions SET status='declined',granted=0 WHERE id=?",(session,))
            elif row[2] in ('approved', 'declined', 'expired'):
                return self.read(session)
            elif now >= row[3]:
                db.execute('INSERT INTO events VALUES(?,?)', (session,event))
                db.execute("UPDATE sessions SET status='expired' WHERE id=?", (session,))
            elif status not in ('Approved', 'Declined', 'In Review', 'In Progress'):
                db.execute('INSERT INTO events VALUES(?,?)', (session,event))
                db.execute("UPDATE sessions SET status='unknown' WHERE id=?", (session,))
            else:
                db.execute('INSERT INTO events VALUES(?,?)', (session,event))
                normalized = {'Approved': 'approved', 'Declined': 'declined', 'In Review': 'review', 'In Progress': 'pending'}[status]
                grant = int(status == 'Approved' and policy is True and bool(row[4]))
                db.execute('UPDATE sessions SET status=?,granted=?,grants=grants+? WHERE id=?', (normalized, grant, grant, session))
        return self.read(session)

    def recover(self, session='fixture-session', now=61):
        with self.connect() as db:
            db.execute("UPDATE sessions SET status='expired' WHERE id=? AND deadline<=? AND status IN ('pending','review','unknown')", (session, now))
        return {**self.read(session), 'next': 'review_or_authorized_provider_refresh', 'provider_polled': False}

    def revise_policy(self,expected_version,allow,session='fixture-session'):
        if type(expected_version) is not int or type(allow) is not bool:raise ValueError('EXPLICIT_POLICY_VERSION_AND_BOOLEAN_REQUIRED')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT policy_version FROM sessions WHERE id=?',(session,)).fetchone()
            if row is None:raise ValueError('SESSION_NOT_FOUND')
            if row[0]!=expected_version:raise ValueError('STALE_POLICY_VERSION')
            db.execute('UPDATE sessions SET policy_version=policy_version+1,allow_action=?,granted=0 WHERE id=?',(int(allow),session))
        return self.read(session)

    def decide(self,expected_version,approve,session='fixture-session',now=1):
        if type(expected_version) is not int or type(approve) is not bool:raise ValueError('EXPLICIT_POLICY_VERSION_AND_BOOLEAN_REQUIRED')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT policy_version,status,deadline,allow_action,granted FROM sessions WHERE id=?',(session,)).fetchone()
            if row is None:raise ValueError('SESSION_NOT_FOUND')
            if row[0]!=expected_version:raise ValueError('STALE_POLICY_VERSION')
            if not approve or row[1]!='approved' or now>=row[2] or not row[3]:raise ValueError('CURRENT_EVIDENCE_AND_EXPLICIT_APPROVAL_REQUIRED')
            if not row[4]:db.execute('UPDATE sessions SET granted=1,grants=grants+1 WHERE id=?',(session,))
        return self.read(session)

    def handoff(self,session='fixture-session'):
        return {**self.read(session),'verified':False,'next_action':'read_current_evidence_and_policy_before_explicit_decision'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('task', choices=['phone', 'identity'])
    p.add_argument('--branch', default='normal', choices=['normal', 'unknown', 'provider_failure', 'otp'])
    p.add_argument('--db', default='/tmp/gridzen-delivery-fixture.sqlite')
    args = p.parse_args()
    if args.task == 'phone':
        result = phone(args.branch)
    else:
        state = Identity(args.db)
        try:
            link = state.create()
        except sqlite3.IntegrityError:
            link = {'mode': MODE, 'state': 'existing_fixture'}
        result = {'created': link, 'result': state.event('fixture-approved', policy=True)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

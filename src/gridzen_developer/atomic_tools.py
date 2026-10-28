"""Public local utilities: no IO, network, billing or identity conclusions."""
import re
from typing import Any


def normalize_phone_format(phone: str) -> dict[str, Any]:
    if not isinstance(phone, str) or len(phone) > 100:
        raise ValueError('PHONE_FORMAT_INPUT_INVALID')
    normalized = re.sub(r'[ ()\-\.]', '', phone.strip())
    valid = bool(re.fullmatch(r'\+[1-9][0-9]{7,14}', normalized))
    return {'normalized': normalized if valid else None, 'structure_valid': valid,
            'scope': 'syntax_only', 'number_exists': None, 'ownership_verified': False,
            'network_calls': 0, 'charged': False}


def check_clabe_format(clabe: str) -> dict[str, Any]:
    if not isinstance(clabe, str) or len(clabe) > 100:
        raise ValueError('CLABE_FORMAT_INPUT_INVALID')
    value = re.sub(r'[ \-]', '', clabe.strip())
    shape = bool(re.fullmatch(r'[0-9]{18}', value))
    digit = ((10-sum((int(c)*(3,7,1)[i % 3]) % 10 for i,c in enumerate(value[:17])) % 10) % 10) if shape else None
    return {'structure_valid': shape, 'checksum_valid': shape and digit == int(value[-1]),
            'institution_code': value[:3] if shape else None, 'scope': 'checksum_only',
            'account_exists': None, 'ownership_verified': False, 'network_calls': 0, 'charged': False}


def explain_verification_status(status: str) -> dict[str, Any]:
    if not isinstance(status, str) or not re.fullmatch(r'[a-zA-Z_]{1,60}', status):
        raise ValueError('STATUS_INPUT_INVALID')
    code = status.lower()
    meaning = {
        'pending': ('The task has not reached an authoritative final result.', 'Read the original task using its existing ID.'),
        'timeout': ('Delivery or execution is uncertain; timeout is not a negative verification.', 'Recover the original request; preserve its idempotency key.'),
        'unavailable': ('The requested evidence is unavailable.', 'Inspect the documented reason and route status; do not infer a mismatch.'),
        'unknown': ('No conclusive result is available.', 'Preserve the request and follow its documented recovery path.'),
        'declined': ('The provider returned a declined result.', 'Review the actual evidence under your application policy; do not retry automatically.'),
        'approved': ('The provider returned an approved result.', 'Check the authoritative task and your application policy; approval does not grant business permissions.'),
        'mismatch': ('A supported comparison returned a mismatch.', 'Inspect the compared fields and evidence; do not infer fraud or change the result.'),
        'not_found': ('The source returned no record for this query.', 'Check documented input requirements; absence of a record is not proof of a false identity.'),
    }
    text, action = meaning.get(code, ('This status is not documented by this local helper.', 'Read the product-specific reference; do not infer an outcome.'))
    return {'status': code, 'known': code in meaning, 'meaning': text, 'next_step': action,
            'automatic_business_approval': False, 'network_calls': 0, 'charged': False}


LOCAL_TOOLS = {'phone-format': normalize_phone_format, 'clabe-format': check_clabe_format,
               'result-explanation': explain_verification_status}

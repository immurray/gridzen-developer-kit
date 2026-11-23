"""PostgreSQL aggregate-only writer for the hosted HTTP service."""
from contextlib import contextmanager
from datetime import timedelta
from hashlib import sha256
import os
from pathlib import Path
import stat

LOCK = 745036
ROLE = 'gridzen_product_metrics_mcp_writer'


class Unavailable(OSError):
    pass


def selected():
    mode = os.getenv('GRIDZEN_MCP_METRICS_STORAGE')
    if mode is None and not os.getenv('GRIDZEN_MCP_METRICS_DSN_FILE'):
        return False
    if mode != 'postgres':
        raise Unavailable('MCP_METRICS_EXPLICIT_POSTGRES_MODE_REQUIRED')
    return True


@contextmanager
def connection():
    # StdIO and the public client package do not need the hosted-only dependency.
    try:
        import psycopg
    except ImportError:
        raise Unavailable('MCP_METRICS_DRIVER_REQUIRED') from None

    environment = os.getenv('GRIDZEN_MCP_METRICS_ENVIRONMENT')
    if environment not in ('production','sandbox'):
        raise Unavailable('MCP_METRICS_ENVIRONMENT_REQUIRED')
    try:
        path = Path(os.environ['GRIDZEN_MCP_METRICS_DSN_FILE'])
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o007 or path.is_symlink():
            raise Unavailable('MCP_METRICS_CONFIGURATION_INVALID')
        with path.open(encoding='utf-8') as stream:
            dsn = stream.read(8193).strip()
        if not dsn or len(dsn)>8192:
            raise Unavailable('MCP_METRICS_CONFIGURATION_INVALID')
        with psycopg.connect(dsn,connect_timeout=3,options='-c statement_timeout=4000 -c lock_timeout=1500') as db:
            identity = db.execute('''
                SELECT rolname,rolsuper,rolbypassrls,rolcreatedb,rolcreaterole
                FROM pg_roles WHERE rolname=current_user
            ''').fetchone()
            if identity!=(ROLE,False,False,False,False):
                raise Unavailable('MCP_METRICS_ROLE_MISMATCH')
            adopted = db.execute('''
                SELECT 1 FROM product_metrics.authority a JOIN product_metrics.mcp_adoption m USING (singleton,environment)
                WHERE a.singleton AND a.environment=%s AND a.frozen_digest IS NOT NULL
            ''',(environment,)).fetchone()
            if not adopted:
                raise Unavailable('MCP_METRICS_AUTHORITY_NOT_ADOPTED')
            yield db
    except (psycopg.Error,KeyError,ValueError,UnicodeError):
        raise Unavailable('MCP_METRICS_UNAVAILABLE') from None


def write_feedback(values, receipt, day):
    from .product_feedback import FIELDS

    with connection() as db:
        db.execute('SELECT pg_advisory_xact_lock(%s,4)',(LOCK,))
        if day is None:
            day=db.execute("SELECT (clock_timestamp() AT TIME ZONE 'UTC')::date").fetchone()[0]
        db.execute("DELETE FROM product_metrics.product_events WHERE channel='public' AND day<%s",
                   (day-timedelta(days=89),))
        db.execute("DELETE FROM product_metrics.feedback_receipts WHERE channel='public' AND day<%s",
                   (day-timedelta(days=29),))
        total, feedback = db.execute("""
            SELECT COALESCE(SUM(count),0),COALESCE(SUM(count) FILTER(WHERE operation='task_summary'),0)
            FROM product_metrics.product_events WHERE channel='public' AND day=%s
        """,(day,)).fetchone()
        if total>=10000 or receipt and feedback>=500:
            return False
        if receipt:
            reference=sha256(receipt.encode()).hexdigest()
            if db.execute("SELECT 1 FROM product_metrics.feedback_receipts WHERE channel='public' AND hash=%s",
                          (reference,)).fetchone():
                return True
            db.execute("INSERT INTO product_metrics.feedback_receipts VALUES ('public',%s,%s)",(day,reference))
        columns='day,'+','.join(FIELDS)
        placeholders=','.join(['%s']*(1+len(FIELDS)))
        db.execute("INSERT INTO product_metrics.product_events(channel,"+columns+",count) VALUES ('public',"+placeholders+",1) "
                   "ON CONFLICT(channel,"+columns+") DO UPDATE SET count=product_events.count+1",
                   (day,*(values[key] for key in FIELDS)))
    return True


def write_call(day,tool,source):
    with connection() as db:
        db.execute('SELECT pg_advisory_xact_lock(%s,3)',(LOCK,))
        if day is None:
            day=db.execute("SELECT (clock_timestamp() AT TIME ZONE 'UTC')::date").fetchone()[0]
        db.execute('DELETE FROM product_metrics.mcp_calls WHERE day<%s',(day-timedelta(days=89),))
        db.execute('''
            INSERT INTO product_metrics.mcp_calls VALUES (%s,%s,1)
            ON CONFLICT(day,tool) DO UPDATE SET count=mcp_calls.count+1
        ''',(day,tool))
        db.execute('''
            INSERT INTO product_metrics.mcp_call_sources VALUES (%s,%s,%s,1)
            ON CONFLICT(day,tool,source) DO UPDATE SET count=mcp_call_sources.count+1
        ''',(day,tool,source))

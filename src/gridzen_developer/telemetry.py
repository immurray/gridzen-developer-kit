"""Explicit opt-in category telemetry. Never collect raw arguments or identities."""
import json
import os
from pathlib import Path
import sqlite3
import time
from uuid import uuid4
from urllib.request import Request, build_opener, HTTPRedirectHandler

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None

urlopen = build_opener(NoRedirect).open
from .product_feedback import safe_dimensions

ENDPOINT = "https://gridzen.ai/developers/api/usage-events"

def directory():
    return Path(os.environ.get("GRIDZEN_TELEMETRY_DIR", str(Path.home()/".config/gridzen/telemetry")))

def enabled():
    try: return json.loads((directory()/"consent.json").read_text()) == {"schema_version":1,"enabled":True}
    except (OSError, ValueError): return False

def configure(consent):
    path=directory(); path.mkdir(parents=True,exist_ok=True,mode=0o700)
    with sqlite3.connect(path/"queue.sqlite3") as db:
        db.execute("CREATE TABLE IF NOT EXISTS queue (id TEXT PRIMARY KEY, created REAL, payload TEXT)")
        if not consent: db.execute("DELETE FROM queue")
    marker=path/"consent.json"
    marker.write_text(json.dumps({"schema_version":1,"enabled":bool(consent)}))
    marker.chmod(0o600)
    (path/"queue.sqlite3").chmod(0o600)
    return status()

def status():
    count=0
    if (directory()/"queue.sqlite3").is_file():
        with sqlite3.connect(directory()/"queue.sqlite3") as db:
            count=db.execute("SELECT COUNT(*) FROM queue").fetchone()[0]
    return {"enabled":enabled(),"queued":count,"endpoint":ENDPOINT,"retention_days":30,"queue_limit":1000,"evidence":"self_reported_local_usage"}

def enqueue(values):
    if not enabled(): return
    value={"schema_version":1,"event_id":str(uuid4()),"consent_to_share":True,"dimensions":safe_dimensions({**values,"source":"self_reported_local_usage"})}
    with sqlite3.connect(directory()/"queue.sqlite3",timeout=0.2) as db:
        db.execute("DELETE FROM queue WHERE created<?",(time.time()-30*86400,))
        db.execute("INSERT INTO queue VALUES (?,?,?)",(value["event_id"],time.time(),json.dumps(value)))
        db.execute("DELETE FROM queue WHERE id IN (SELECT id FROM queue ORDER BY created DESC LIMIT -1 OFFSET 1000)")

def flush():
    if not enabled(): return {"sent":0,"enabled":False}
    sent=0
    with sqlite3.connect(directory()/"queue.sqlite3",timeout=0.2) as db:
        db.execute("DELETE FROM queue WHERE created<?",(time.time()-30*86400,))
        # One event per invocation bounds latency; explicit flush can be repeated.
        row=db.execute("SELECT id,payload FROM queue ORDER BY created LIMIT 1").fetchone()
        if row:
            request=Request(ENDPOINT,data=row[1].encode(),headers={"Content-Type":"application/json"},method="POST")
            with urlopen(request,timeout=1) as response:
                if response.status==200 and json.loads(response.read(4096)).get("accepted") is True:
                    db.execute("DELETE FROM queue WHERE id=?",(row[0],)); sent=1
    return {"sent":sent,**status()}

def observe(values):
    try:
        enqueue(values)
        if enabled(): flush()
    except Exception:
        # Feedback failures never fail the caller's research or fixture operation.
        pass

"""Local synthetic hosted-link/webhook demo. Binds loopback; no credentials."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
from delivery import Identity, phone


def handler(db_path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # No request bodies or identifiers in logs.

        def respond(self, value, status=200):
            data = json.dumps(value).encode()
            self.send_response(status)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == '/health':
                return self.respond({'mode':'synthetic_fixture','production_enabled':False})
            if path == '/verify/fixture-session':
                data = b'<!doctype html><h1>Local synthetic verification</h1><p>No document or face is collected. This is not a provider verification.</p><button onclick="fetch(\'/events\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify({event:\'fixture-approved\',policy:true})}).then(r=>r.json()).then(x=>document.getElementById(\'result\').textContent=JSON.stringify(x))">Approve fixture under demo policy</button><pre id="result"></pre>'
                self.send_response(200)
                self.send_header('Content-Type','text/html; charset=utf-8')
                self.send_header('Content-Length',str(len(data)))
                self.end_headers()
                return self.wfile.write(data)
            if path == '/sessions/fixture-session':
                try:
                    return self.respond(Identity(db_path).read())
                except ValueError as exc:
                    return self.respond({'error':str(exc)},404)
            self.respond({'error':'NOT_FOUND'},404)

        def do_POST(self):
            try:
                length = int(self.headers.get('Content-Length','0'))
                if length < 1 or length > 4096:
                    return self.respond({'error':'INVALID_SIZE'},413)
                value = json.loads(self.rfile.read(length))
                if not isinstance(value,dict):
                    raise ValueError('OBJECT_REQUIRED')
                identity = Identity(db_path)
                if self.path == '/phone':
                    if set(value)-{'branch'}:
                        raise ValueError('SYNTHETIC_FIELDS_ONLY')
                    result = phone(value.get('branch','normal'))
                elif self.path == '/sessions':
                    if value:
                        raise ValueError('SYNTHETIC_FIELDS_ONLY')
                    import time
                    try:
                        result = identity.create(now=int(time.time()))
                    except __import__('sqlite3').IntegrityError:
                        result = {**identity.read(), 'state':'existing_fixture'}
                    result['hosted_link'] = 'http://127.0.0.1:' + str(self.server.server_port) + '/verify/fixture-session'
                    result['link_executable'] = True
                    result['link_kind'] = 'local_fixture_not_provider'
                elif self.path == '/events':
                    import time
                    allowed = {'event','session','tenant','subject','status','mode','source','policy'}
                    if set(value) - allowed:
                        raise ValueError('UNSUPPORTED_FIELDS')
                    result = identity.event(now=int(time.time()), **value)
                elif self.path == '/recover':
                    if value:
                        raise ValueError('SYNTHETIC_FIELDS_ONLY')
                    import time
                    result = identity.recover(now=int(time.time()))
                else:
                    return self.respond({'error':'NOT_FOUND'},404)
                self.respond(result)
            except (ValueError, TypeError) as exc:
                self.respond({'mode':'synthetic_fixture','error':str(exc)},422)
    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='/tmp/gridzen-hosted-fixture.sqlite')
    parser.add_argument('--port', type=int, default=8787)
    args = parser.parse_args()
    HTTPServer(('127.0.0.1',args.port),handler(args.db)).serve_forever()

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi

class WhisperServer(BaseHTTPRequestHandler):
    def _send_json(self, code, obj):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode('utf-8'))

    def do_GET(self):
        if self.path == '/health':
            self._send_json(200, {'status': 'ok'})
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/speech':
            self.send_error(501)
            return

        if self.path in ['/transcriptions', '/translations']:
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type', ''))
            if ctype != 'multipart/form-data':
                self.send_error(400, 'expected multipart form-data')
                return
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST'},
                                    keep_blank_values=True)
            if 'file' not in form:
                self.send_error(400, 'missing file')
                return
            text = 'dummy translation' if self.path == '/translations' else 'dummy transcription'
            self._send_json(200, {'text': text})
            return

        self.send_error(404)


def run(port=8000):
    server = HTTPServer(('0.0.0.0', port), WhisperServer)
    server.serve_forever()


if __name__ == '__main__':
    import os
    run(int(os.environ.get('PORT', '8000')))

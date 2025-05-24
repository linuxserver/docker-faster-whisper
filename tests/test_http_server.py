import http.client
import json
import threading
from http.server import HTTPServer
import io
import wave
import uuid

import pytest

from http_server import WhisperServer


def start_server():
    server = HTTPServer(('localhost', 0), WhisperServer)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def stop_server(server):
    server.shutdown()
    server.server_close()


@pytest.fixture(scope="module")
def server():
    srv = start_server()
    yield srv
    stop_server(srv)


def make_wav_bytes():
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"\x00\x00" * 1600)
    return buf.getvalue()


def send_multipart(port, path):
    boundary = uuid.uuid4().hex
    body = []
    body.append(b"--" + boundary.encode())
    body.append(b'Content-Disposition: form-data; name="file"; filename="audio.wav"')
    body.append(b"Content-Type: audio/wav\r\n")
    body.append(make_wav_bytes())
    body.append(b"--" + boundary.encode() + b"--\r\n")
    body_bytes = b"\r\n".join(body)
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    conn = http.client.HTTPConnection("localhost", port)
    conn.request("POST", path, body=body_bytes, headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()
    return resp.status, data


def test_health(server):
    port = server.server_address[1]
    conn = http.client.HTTPConnection("localhost", port)
    conn.request("GET", "/health")
    resp = conn.getresponse()
    body = resp.read()
    conn.close()
    assert resp.status == 200
    assert json.loads(body) == {"status": "ok"}


def test_speech_not_implemented(server):
    port = server.server_address[1]
    conn = http.client.HTTPConnection("localhost", port)
    conn.request("POST", "/speech", body=b"")
    resp = conn.getresponse()
    conn.close()
    assert resp.status == 501


def test_transcription(server):
    port = server.server_address[1]
    status, data = send_multipart(port, "/transcriptions")
    assert status == 200
    assert json.loads(data)["text"] == "dummy transcription"


def test_translation(server):
    port = server.server_address[1]
    status, data = send_multipart(port, "/translations")
    assert status == 200
    assert json.loads(data)["text"] == "dummy translation"

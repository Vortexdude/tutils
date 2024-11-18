import os
import json

def kwargs_from_env(environment=None):
    if not environment:
        environment = os.environ

    host = environment.get("DOCKER_HOST")
    cert_path = environment.get("DOCKER_CERT_PATH") or None
    params = {}
    if host:
        params['base_url'] = host

    if cert_path:
        params['tls'] = "/non/exist/path"

    return params

class RequestBuilder(object):
    def __init__(self, method, host=None, endpoint=None, content_type=None, payload=None):
        self.AVAILABLE_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]

        if method not in self.AVAILABLE_METHODS:
            raise Exception("Method is not allowed")

        if not content_type:
            content_type = "application/json"

        self.method = method
        self.host = host or 'localhost'
        self.endpoint = endpoint or "/"
        self.content_type = content_type
        self.payload = payload

    def dispatch(self) -> str:
        _request_line = f"{self.method} {self.endpoint} HTTP/1.1\r\n"
        _headers = (
            f"Host: {self.host}\r\n"
            f"Content-Type: {self.content_type}\r\n"
        )

        if self.method.upper() == "POST":
            if "create" in self.endpoint:
                _headers += f"Content-length: {len(json.dumps(self.payload))}\r\n"
            if "start" in self.endpoint:
                _headers += f"Content-length: 0\r\n"

        _headers += "\r\n"

        _body = json.dumps(self.payload) if self.payload else ""

        return _request_line + _headers + _body

def request_formatter(data):
    _response_status = dict()

    if "\r\n\r\n" in data:
        for idx, data in enumerate(data.split("\r\n\r\n")):
            if idx == 0:
                for header in data.split("\r\n"):
                    if ":" in header.strip():
                        if "Date" in header:
                            _response_status['Date'] = header[6:]
                        else:
                            k, v = header.split(":")
                            _response_status[k] = v.strip()
                    else:
                        _response_status['Status-Code'] = header.strip().split("HTTP/1.1 ")[1][:3]

            elif idx == 1:
                if "\r\n" in data:
                    data = data.split("\r\n")[1]
                try:
                    _response_status['body'] = json.loads(data)
                except Exception:
                    _response_status['body'] = {}

    return _response_status

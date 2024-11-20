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


class Executor:
    line_end: str = "\r\n"

    def __init__(self, host=None):
        self.host = host or "localhost"

    def dispatch(self, method: str, endpoint=None, content_type=None, payload=None):
        if not content_type:
            content_type = "application/json"
        _request_line = f"{method.upper()} {endpoint} HTTP/1.1{self.line_end}"
        _headers = (
            f"Host: {self.host}{self.line_end}"
            f"Content-Type: {content_type}{self.line_end}"
        )
        if method.upper() == "POST":
            if "create" in endpoint:
                _headers += f"Content-length: {len(json.dumps(payload))}{self.line_end}"
            if "start" in endpoint:
                _headers += f"Content-length: 0{self.line_end}"

        _headers += self.line_end

        _body = json.dumps(payload) if payload else ""

        return _request_line + _headers + _body

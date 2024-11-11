import json


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

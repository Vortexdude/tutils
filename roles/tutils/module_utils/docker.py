import socket
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

    def dispatch(self):
        _request_line = f"{self.method} {self.endpoint} HTTP/1.1\r\n"
        _headers = (
            f"Host: {self.host}\r\n"
            f"Content-Type: {self.content_type}"
        )

        if self.method.upper() == "POST":
            if "create" in self.endpoint:
                _headers += f"Content-length: {len(self.content_type)}\r\n"
            if "start" in self.endpoint:
                _headers += f"Content-length: 0\r\n"

        _headers += "\r\n"

        _body = json.dumps(self.payload) if self.payload else ""

        return _request_line + _headers + _body


class DockerApiBase(object):
    def __init__(self, file: str):
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock_file = file if file else "/var/run/docker.sock"
        self.connect()

    def connect(self):
        self.client.connect(self.sock_file)

    def send_request(self, request):
        try:
            self.client.sendall(request)
        except Exception as e:
            raise Exception("Error while sending the request")

    def receive_data(self, buffer_size):
        if not buffer_size:
            buffer_size = 4096

        data = b""
        while True:
            part = self.client.recv(buffer_size)
            data += part
            if len(part) < buffer_size:
                break
        return data.decode()

    @staticmethod
    def filter_response(response):
        if isinstance(response, bytes):
            response = response.decode("utf-8")
        data = response.split("\r\n\r\n")[1]

        return data


class DockerBase(DockerApiBase):
    def create_container(self, image, name=None, cmd:list=None, hostname=None, domain_name=None, user=None, tty:bool=None) -> dict:
        _method = "Get"
        _endpoint = "/container/create"
        rr = RequestBuilder(host="localhost", endpoint=_endpoint, method=_method, )

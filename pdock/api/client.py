from pdock.request import SocketBase
from pdock.utils import RequestBuilder, request_formatter
from pdock.api.containers import ContainerApiMixing


class APIClient(ContainerApiMixing):

    def __init__(self, base_url=None):
        self.socket = SocketBase("/var/run/docker.sock")
        if base_url is None:
            base_url = "localhost"

        self.base_url = base_url

    def _get(self, endpoint, host=None, payload=None):
        _method = "GET"
        if not host:
            host = self.base_url
        rb = RequestBuilder(host=host, method=_method, endpoint=endpoint, payload=payload)
        _request = rb.dispatch().encode("utf-8")
        self.socket.send_request(_request)
        _response = self.socket.receive_data(4096)
        return request_formatter(_response)['body']

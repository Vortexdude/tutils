from pdock.request import SocketBase
from pdock.utils import request_formatter, Executor
from pdock.api.containers import ContainerApiMixing


class APIClient(Executor, ContainerApiMixing):

    def __init__(self, base_url=None):
        self.socket = SocketBase("/var/run/docker.sock")
        if base_url is None:
            base_url = "localhost"

        self.base_url = base_url
        Executor.__init__(self, host=self.base_url)

    def __common_ops(self, method, endpoint, payload=None, host=None):
        _request = self.dispatch(method=method, endpoint=endpoint, payload=payload).encode('utf-8')
        self.socket.send_request(_request)
        return self.socket.receive_data(4096)

    def get(self, endpoint, payload=None):
        _method = "GET"
        return self.__common_ops(method=_method, endpoint=endpoint, payload=payload)

    def post(self, endpoint, payload=None):
        _method = "POST"
        return self.__common_ops(method=_method, endpoint=endpoint, payload=payload)

    @staticmethod
    def format(data):
        """Format the HTTP request response"""
        return request_formatter(data)['body']


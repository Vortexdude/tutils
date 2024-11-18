import socket


class SocketBase:
    def __init__(self, file: str = None, host=None):
        self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock_file = file or "/var/run/docker.sock"
        self.host = host or 'localhost'
        self.connect()

    def connect(self):
        self.client.connect(self.sock_file)

    def send_request(self, request):
        try:
            self.client.sendall(request)
        except Exception as e:
            raise Exception("Error while sending the request")

    def receive_data(self, buffer_size=None):
        if not buffer_size:
            buffer_size = 4096

        data = b""
        while True:
            part = self.client.recv(buffer_size)
            data += part
            if len(part) < buffer_size:
                break
        return data.decode("utf-8")

    @staticmethod
    def filter_response(response):
        if isinstance(response, bytes):
            response = response.decode("utf-8")
        data = response.split("\r\n\r\n")[1]

        return data

import json
import socket
from pydantic import BaseModel

try:
    from ansible.module_utils.docker_config import ContainerConfig, id_generate
    from ansible.module_utils.dispacher import RequestBuilder
    from ansible.module_utils.formatters import request_formatter
except ImportError:
    from .docker_config import ContainerConfig, id_generate
    from .dispacher import RequestBuilder
    from .formatters import request_formatter


class ApiEndpointMapping:
    class Containers:
        class Create:
            Method = 'POST'

            @staticmethod
            def Endpoint(name=None):
                _base_url = "/containers/create"
                if name:
                    _base_url += f"?name={name}"

                return _base_url

        class Start:
            Method = "POST"

            @staticmethod
            def Endpoint(value) -> str:
                if not value:
                    # also validate the container id, should be exists `docker ps`
                    raise Exception("Container id should be provided")

                if not isinstance(value, str):
                    raise Exception("Container ID should string")

                return f"/containers/{value}/start"

        class List:
            Method = "GET"

            @staticmethod
            def Endpoint(value=False):
                _base_url = "/containers/json"
                if value:
                    _base_url += "?all=true"
                return _base_url

class DockerApiBase(object):
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


class DockerBase(DockerApiBase):

    def __common_ops(self, method, endpoint, payload=None, host=None):
        if not host:
            host = self.host

        rr = RequestBuilder(host=host, method=method, endpoint=endpoint, payload=payload)
        _request = rr.dispatch().encode("utf-8")
        self.send_request(_request)
        _response = self.receive_data()
        return request_formatter(_response)['body']

    def create_container(self, image, **kwargs) -> dict:
        container_name = kwargs.get('name', f"{image}_{id_generate()}")
        _method = ApiEndpointMapping.Containers.Create.Method
        _endpoint = ApiEndpointMapping.Containers.Create.Endpoint(name=container_name)
        _payload = ContainerConfig(image=image, **kwargs).to_dict()

        return self.__common_ops(_method, _endpoint, _payload)

    def start_container(self, container_id):
        _endpoint = ApiEndpointMapping.Containers.Start.Endpoint(container_id)
        _method = ApiEndpointMapping.Containers.Start.Method

        return self.__common_ops(_method, _endpoint)

    def stop_container(self, container_id: str):
        _endpoint = f"/containers/{container_id}/stop"
        _method = "POST"

        return self.__common_ops(_method, _endpoint)

    def restart_container(self, container_id: str):
        _endpoint = f"/containers/{container_id}/restart"
        _method = "POST"

        return self.__common_ops(_method, _endpoint)

    def remove_container(self, container_id: str):
        _endpoint = f"/containers/{container_id}"
        _method = "DELETE"

        return self.__common_ops(_method, _endpoint)

    def list_containers(self, all_containers):
        _endpoint = ApiEndpointMapping.Containers.List.Endpoint(all_containers)
        _method = ApiEndpointMapping.Containers.List.Method

        return self.__common_ops(_method, _endpoint)

    def validate_container(self, container_name) -> dict:
        all_containers = self.list_containers(True)
        for container in all_containers:
            for c_name in container['Names']:
                if "/" in c_name:
                    container_name = "/" + container_name

                if container_name == c_name:
                    return container
        return {}

    def local_image_metadata(self, image=None, tag=None):
        # curl --unix-socket /var/run/docker.sock http:/v1.41/images/python/json
        if not image:
            raise Exception("Image not specify")

        _host = "v1.41"
        _method = "GET"
        _endpoint = f"/images/{image}:{tag}/json" if tag else f"/images/{image}/json"
        return self.__common_ops(method=_method, endpoint=_endpoint, host=_host)

    def pull_image_from_dockerhub(self, image, tag=None):
        _host = "v1.41"
        _method = "POST"
        _endpoint = f"/images/create"
        _payload = json.loads()
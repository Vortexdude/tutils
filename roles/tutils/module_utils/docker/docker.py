try:
    from ansible.module_utils.api_base import DockerBase
    from ansible.module_utils.formatters import validator, container_id_validator
except ImportError:
    from .api_base import DockerBase
    from .formatters import validator, container_id_validator

class Docker:
    SOCKET_FILE = "/var/run/docker.sock"
    HOSTNAME = 'localhost'

    def __init__(self):
        self.__docker = DockerBase(file=self.SOCKET_FILE, host=self.HOSTNAME)

    def create_container(self, image, **kwargs):
        """
        create the docker container

        Parameters:
            image (str): The container image.
            name (str, optional): The container name.
            cmd (list, optional): Command to run in the container.
            hostname (str, optional): Hostname of the container.
            domain_name (str, optional): Domain name of the container.
            user (str, optional): User to run the container.
            ports (str, optional): Port mapping for exposing the application
        """

        return self.__docker.create_container(image=image, **kwargs)

    def start_container(self, container_id: str):
        """
        Starts a container with specified parameters and forwards modified args to create_container.

        :param container_id:
        :type container_id:
        :return:
        :rtype:
        """
        return self.__docker.start_container(container_id)

    @validator(container_id_validator)
    def restart_container(self, container_id: str):
        """Restart a given docker container"""

        return self.__docker.restart_container(container_id)

    def list_containers(self, all_containers=False):
        """list all the running docker containers"""

        return self.__docker.list_containers(all_containers)

    def validate_container(self, container_name):
        """Check whether docker container exists or not"""

        return self.__docker.validate_container(container_name)

    @validator(container_id_validator)
    def stop_container(self, container_id: str):
        """Stopping running docker container"""

        return self.__docker.stop_container(container_id)

    @validator(container_id_validator)
    def remove_container(self, container_id: str):
        """Remove docker container like docker rm"""

        return self.__docker.remove_container(container_id)

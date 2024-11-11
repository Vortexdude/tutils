try:
    from ansible.module_utils.api_base import DockerBase
except ImportError:
    from .api_base import DockerBase


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
        """
        return self.__docker.create_container(image=image, **kwargs)['body']

    def start_container(self, container_id: str):
        """
        Starts a container with specified parameters and forwards modified args to create_container.

        :param container_id:
        :type container_id:
        :return:
        :rtype:
        """
        return self.__docker.start_container(container_id)['body']


# cc = Docker()
# c_id = cc.create_container(image='busybox', cmd=['sleep', '20'])
# print(c_id['Id'])


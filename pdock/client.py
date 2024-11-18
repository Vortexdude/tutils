from pdock.constant import DEFAULT_TIMEOUT
from pdock.containers import ContainersOps
from pdock.api.client import APIClient


class Docker(object):
    def __init__(self, *args, **kwargs):
        self.api = APIClient(*args, **kwargs)


    @classmethod
    def from_env(cls, **kwargs):
        timeout = kwargs.pop("timeout", DEFAULT_TIMEOUT)

        return cls(**kwargs)

    @property
    def containers(self):
        return ContainersOps(client=self)

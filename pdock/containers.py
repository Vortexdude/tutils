from .resources import Container

class Collection:
    """Base class for representing all the object inside the class"""
    model = None

    def __init__(self, client=None):
        self.client = client

    def __call__(self, *args, **kwargs):
        raise TypeError(
            f"'{self.__class__.__name__} object is not callable, "
            "use docker.APIClient() is possible"
        )

    def list(self):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def create(self, attr=None):
        raise NotImplementedError

    def prepare_model(self, attrs):
        if isinstance(attrs, dict):
            return self.model(attrs=attrs, client=self.client, collection=self)
        else:
            raise f"Cant create {self.model.__name__} from {attrs}"


class ContainersOps(Collection):
    model = Container

    def run(self, image, stdout=None, stderr=None, **kwargs):
        pass

    def create(self, image, command=None, **kwargs):
        pass

    def prune(self):
        pass

    def get(self, container_id):
        if not container_id:
            raise
        resp = self.client.api.inspect_container(container_id)
        return self.model.from_data(resp, client=self.client)

    def list(self, all=False):
        response = self.client.api.containers(all=all)
        return [self.model.from_data(r) for r in response]

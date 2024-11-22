from saturo.models.containers import Container
from resources import Collection



class ContainerCollection(Collection):
    model = Container

    def list(self, all_containers=True):
        containers = self.client.api.containers(all_containers=all_containers)

        return [self.model.prepare_model(con, client=self.client) for con in containers]

    def create(self, image, *args, **kwargs):
        container = self.client.api.create_container(image, *args, **kwargs)
        return self.model.prepare_model(container, client=self.client)

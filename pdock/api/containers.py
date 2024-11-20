
class ContainerApiMixing:

    def containers(self, all=False):
        endpoint = "/containers/json"
        if all:
            endpoint += "?all=true"
        return self.format(self.get(endpoint))

    def inspect_container(self, container_id):
        endpoint = f"/containers/{container_id}/json"
        data = self.format(self.get(endpoint))
        return data

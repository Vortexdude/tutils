
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

    def stop_container(self, container_id):
        endpoint = f"/containers/{container_id}/stop"
        data = self.format(self.post(endpoint))
        return data

    def start_container(self, container_id):
        endpoint = f"/containers/{container_id}/start"
        data = self.format(self.post(endpoint))
        return data

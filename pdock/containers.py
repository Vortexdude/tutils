
class ContainersOps(object):
    def __init__(self, client):
        self.client = client

    def run(self, image, stdout=None, stderr=None, **kwargs):
        pass


    def list(self):
        endpoint = "/containers/json"
        data = self.client.api.get(endpoint)
        print(data)

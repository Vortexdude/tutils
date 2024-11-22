class BaseApiMixing(object):
    def get(self, endpoint, *args, **kwargs) -> dict:
        raise NotImplementedError()

    def post(self, endpoint, *args, **kwargs) -> dict:
        raise NotImplementedError()


class ContainerApiMixing(BaseApiMixing):

    def containers(self, all_containers=True):
        all_containers = "true" if all_containers else "false"
        endpoint = f"/containers/json?all={all_containers}"
        response = self.get(endpoint)
        print(f"{response['Status-Code']=}")
        if str(response['Status-Code']) != 200:
            raise Exception(f"{response['body']['message']}")

        return response['body']

    def stop_container(self, container_id):
        endpoint = f"/containers/{container_id}/stop"
        response = self.post(endpoint)
        print(f"{response['Status-Code']=}")
        return response['body']

    def restart_container(self, container_id):
        endpoint = f"/containers/{container_id}/restart"
        response = self.post(endpoint)
        print(f"{response['Status-Code']=}")
        return response['body']

    def create_container(self, image, command=None, **kwargs):
        params = {}
        if "name" in kwargs:
            params = {
                "name": kwargs['name']
            }

        endpoint = "/containers/create"
        kwargs['image'] = image

        response = self.post(endpoint, payload=kwargs, query_param=params)
        print(f"{response['Status-Code']=}")
        if str(response['Status-Code']) != 200:
            raise Exception(f"{response['body']['message']}")
        return response['body']

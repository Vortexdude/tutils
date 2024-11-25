class BaseApiMixing(object):
    def get(self, endpoint, *args, **kwargs) -> dict:
        raise NotImplementedError()

    def post(self, endpoint, *args, **kwargs) -> dict:
        raise NotImplementedError()

    def delete(self, endpoint, *args, **kwargs) -> dict:
        raise NotImplementedError()


class ContainerApiMixing(BaseApiMixing):

    def delete_container(self, container_id):
        endpoint = f"/containers/{container_id}"
        response = self.delete(endpoint)
        if str(response['Status-Code']) == "204":
            return f"<Container {container_id[:12]}>"
        else:
            raise Exception("Container not exists")

    def rename_container(self, container_id, name):
        endpoint = f"/containers/{container_id}/rename"
        params = {"name": name}
        response = self.post(endpoint, query_param=params)
        if str(response['Status-Code']) == "204":
            return response

        elif str(response['Status-Code']) == "400":
            raise Exception(response['body']['message'])

        raise Exception("Error while renaming")

    def containers(self, all_containers=True):
        all_containers = "true" if all_containers else "false"
        endpoint = f"/containers/json?all={all_containers}"
        response = self.get(endpoint)
        print(f"{response['Status-Code']=}")
        if str(response['Status-Code']) != "200":
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
        if str(response['Status-Code']) == "201":
            return response['body']
        else:
            raise Exception(f"{response['body']}")

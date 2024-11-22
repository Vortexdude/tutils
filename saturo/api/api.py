from saturo.req_builder import HttpReq
from .containers import ContainerApiMixing


class ApiMixing(HttpReq, ContainerApiMixing):
    def get(self, url, /, *args, **kwargs):
        return self._get(url, *args, **kwargs)

    def post(self, url, /, *args, **kwargs):
        return self._post(url, *args, **kwargs)

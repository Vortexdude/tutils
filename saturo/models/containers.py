from saturo.resources import Model


class Container(Model):

    @classmethod
    def prepare_model(cls, data, client=None):
        if client:
            data['client'] = client

        return cls.model_validate(data)

    def stop(self):
        return self.client.api.stop_container(self.Id)

    def restart(self):
        return self.client.api.restart_container(self.Id)


    def __str__(self):
        return f"<{self.__class__.__name__}: {self.short_id}>"

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.Id}>"

    def __call__(self, *args, **kwargs):
        return f"<You should not call {self.__class__.__name__} the class>"

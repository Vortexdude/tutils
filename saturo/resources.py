from pydantic import BaseModel

class Collection:
    model = None

    def __init__(self, client):
        self.client = client


class Model(BaseModel):
    Id: str
    client: object = None

    @property
    def short_id(self):
        return self.Id[:12]


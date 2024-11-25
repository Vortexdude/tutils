from saturo.api.api import ApiMixing
from containers import ContainerCollection

class Docker:
    def __init__(self, *args, **kwargs):
        self.api = ApiMixing()

    @classmethod
    def from_env(cls, **kwargs):
        # from here you can remove or add the parameter as per the this
        # method from_env like this -
        # kwargs['timeout'] = 20
        return cls(**kwargs)

    @property
    def containers(self):
        return ContainerCollection(client=self)

    @property
    def config(self):
        return

    @property
    def images(self):
        return

def main():
    dk = Docker()
    client = dk.from_env()
    # reposn = client.containers.create("nginx", name="saturo_gojo")
    # print(reposn)
    for con in client.containers.list(all_containers=True):
        csd = con.rename("new_name")
        print(csd)



if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()

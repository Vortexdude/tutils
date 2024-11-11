import string
import random
from typing import Optional, List
from dataclasses import dataclass


def id_generate(size=6, chars=string.ascii_uppercase + string.digits) -> str:
    return "".join(random.choice(chars) for _ in range(size))


@dataclass
class ContainerConfig(object):
    image: str
    name: Optional[str] = None
    cmd: Optional[List[str]] = None
    hostname: Optional[str] = None
    domain_name: Optional[str] = None
    user: Optional[str] = None
    tty: Optional[str] = None

    def to_dict(self) -> dict:
        data = {
            "image": self.image,
            "name": self.name or f"{self.image}_{id_generate()}"
        }

        optional_field = {
            "cmd": self.cmd,
            "hostname": self.hostname,
            "domain_name": self.domain_name,
            "user": self.user,
            "tty": self.tty
        }

        data.update({k:v for k, v in optional_field.items() if v is not None})

        return data

from typing import List, Optional
from dataclasses import dataclass
import string
import random
import json



def _id_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))



@dataclass
class DockerConfig:
    image: str
    image: Optional[str] = None
    cmd: Optional[List[str]] = None
    hostname: Optional[str] = None
    domain_name: Optional[str] = None
    user: Optional[str] = None
    tty: Optional[bool] = None

    def to_dict(self):
        pass


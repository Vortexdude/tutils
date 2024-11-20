from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, Union, List, Dict

class Model(BaseModel):
    Id: str

    @property
    def short_id(self) -> str:
        return self.Id[:12]

class Port(BaseModel):
    IP: Optional[str]
    PrivatePort: int
    PublicPort: int
    Type: str


class Labels(BaseModel):
    maintainer: Optional[str] = None


class HostConfig(BaseModel):
    NetworkMode: str


class NetworkDetails(BaseModel):
    IPAMConfig: Optional[dict]
    Links: Optional[Union[List[str], None]]
    Aliases: Optional[Union[List[str], None]]
    MacAddress: Optional[str]
    DriverOpts: Optional[dict]
    NetworkID: str
    EndpointID: str
    Gateway: str
    IPAddress: str
    IPPrefixLen: int
    IPv6Gateway: str
    GlobalIPv6Address: str
    GlobalIPv6PrefixLen: int
    DNSNames: Optional[Union[List[str], None]]


class NetworkSettings(BaseModel):
    Networks: Dict[str, NetworkDetails]


class Container(Model):
    Id: str
    Name: str
    Image: str
    ImageID: Optional[str] = None
    Command: Optional[str] = None
    Created: Optional[str | int | None] = None
    Ports: Optional[List[Port]] = None
    Labels: Optional[Dict] = None
    State: str
    Status:  Optional[str] = None
    HostConfig: HostConfig
    NetworkSettings: NetworkSettings
    Mounts: List

    @model_validator(mode="before")
    @classmethod
    def check_values(cls, data):
        if "Names" in data:
            data['Name'] = data['Names'][0].lstrip("/") if "/" in data['Names'][0] else data['Names'][0]
            data.pop("Names", None)

        if 'Status' not in data:
            data['State'] = data['State']['Status']

        if 'Config' in data:
            data["ImageID"] = data['Config']['Image']
            data["ImageID"] = data['Config']['Image']

        return data


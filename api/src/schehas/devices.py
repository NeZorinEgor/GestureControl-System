from pydantic import BaseModel

class DeviceBase(BaseModel):
    mac_addr: str
    descriptions: str

class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int

from pydantic import BaseModel


class DeviceSchema(BaseModel):
    id: str
    name: str


class ScenariosSchema(BaseModel):
    id: str
    name: str
    is_active: bool


class RoomsSchema(BaseModel):
    id: str
    name: str
    household_id: str
    devices: list[str]


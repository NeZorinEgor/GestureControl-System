from pydantic import BaseModel


class FingerBase(BaseModel):
    name: str
    fingers: str


class FingerCreate(FingerBase):
    pass


class Finger(FingerBase):
    id: int
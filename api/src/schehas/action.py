from pydantic import BaseModel


class ActionBase(BaseModel):
    name: str
    path_to_file: str
    descriptions: str

class ActionCreate(ActionBase):
    pass

class ActionUpdate(ActionBase):
    pass

class Action(ActionBase):
    id: int

from pydantic import BaseModel


class ScenarioBase(BaseModel):
    name: str


class ScenarioCreate(ScenarioBase):
    pass


class Scenario(ScenarioBase):
    id: int

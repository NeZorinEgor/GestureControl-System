from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.actions import ScenariosModel
from src.schehas.action import ScenarioCreate, Scenario

router = APIRouter(
    prefix="/scenarios",
)


@router.post("/",)
async def create_scenario(
        scenario: ScenarioCreate,
        db: AsyncSession = Depends(get_session)
):
    db_scenario = ScenariosModel(**scenario.__dict__)
    db.add(db_scenario)
    await db.commit()
    return db_scenario


@router.get("/",)
async def read_scenarios(
        db: AsyncSession = Depends(get_session)
):
    scenarios = await db.execute(text("SELECT * FROM scenarios;"))
    return [Scenario(id=i[0], name=i[1]) for i in scenarios]


@router.delete("/{scenario_id")
async def delete_scenario(
        scenario_id: int,
        db: AsyncSession = Depends(get_session)
):
    delete_stmt = text("DELETE FROM scenarios WHERE id=:id;")
    await db.execute(delete_stmt, {"id": scenario_id})
    await db.commit()
    return "delete"

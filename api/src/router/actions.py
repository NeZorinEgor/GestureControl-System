from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.actions import ActionsModel
from src.schehas.action import ActionCreate, Action

router = APIRouter(
    prefix="/actions",
)


@router.post("/",)
async def create_action(
        action: ActionCreate,
        db: AsyncSession = Depends(get_session)):
    db_action = ActionsModel(**action.__dict__)
    db.add(db_action)
    await db.commit()
    return db_action


@router.get("/", )
async def read_actions(
        db: AsyncSession = Depends(get_session)
):
    actions = await db.execute(text("SELECT * FROM actions;"))
    return [Action(id=i[0], name=i[1], path_to_file=i[2], descriptions=i[3]) for i in actions]


@router.delete("/{action_id}")
async def delete_action(
        action_id: int,
        db: AsyncSession = Depends(get_session)
):
    delete_stmt = text("DELETE FROM actions WHERE id=:id;")
    await db.execute(delete_stmt, {"id": action_id})
    await db.commit()
    return "delete"

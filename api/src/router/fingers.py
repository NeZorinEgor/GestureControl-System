from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models.fingers import FingerModel
from src.schehas.finger import FingerCreate, Finger



router = APIRouter(
    prefix="/fingers",
)

@router.post("/", )
async def create_finger(
        finger: FingerCreate,
        db: AsyncSession = Depends(get_session)
):
    db_finger = FingerModel(**finger.__dict__)
    db.add(db_finger)
    await db.commit()
    return db_finger


@router.get("/", )
async def read_fingers(
        db: AsyncSession = Depends(get_session)
):
    fingers = await db.execute(text("SELECT * FROM fingers'"))
    return [Finger(id=i[0], name=i[1], fingers=i[2]) for i in fingers]


@router.delete("/{finger_id}")
async def delete_finger(
        finger_id: int,
        db: AsyncSession = Depends(get_session)
):
    delete_stmt = text("DELETE FROM fingers WHERE id=:id;")
    await db.execute(delete_stmt, {"id": finger_id})
    await db.commit()
    return "delete"
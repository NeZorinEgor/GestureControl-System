from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schehas.devices import DeviceCreate

router = APIRouter(
    prefix="/device",
)


@router.post("/",)
async def create_device(
        device: DeviceCreate,
        db: AsyncSession = Depends(get_session)
):
    from sqlalchemy import text
    create_device_stmt = text("INSERT INTO devices (mac_addr, descriptions) VALUES (:mac_addr, :descriptions)")
    await db.execute(create_device_stmt, {"mac_addr": device.mac_addr, "descriptions": device.descriptions})
    await db.commit()
    return "ok"

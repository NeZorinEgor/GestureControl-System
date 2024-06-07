from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.database import get_session
from src.schehas.devices import DeviceCreate

from src.schehas.devices import Device

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


@router.get("/", )
async def read_device(
        db: AsyncSession = Depends(get_session)
):
    devices = await db.execute(text("SELECT * FROM devises;"))
    return [Device(id=i[0], mac_addr=i[1], descriptions=i[2]) for i in devices]


@router.delete("/{device_id}")
async def delete_device(
        device_id: int,
        db: AsyncSession = Depends(get_session)
):
    delete_stmt = text("DELETE FROM devices WHERE id=:id;")
    await db.execute(delete_stmt, {"id": device_id})
    await db.commit()
    return "delete"
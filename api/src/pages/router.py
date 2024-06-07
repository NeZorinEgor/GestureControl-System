from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.yandex_client.router import get_devices, get_scenarios, get_rooms

router = APIRouter(
    prefix="/index",
    tags=["pages"],
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
def index(
        request: Request,
        devices=Depends(get_devices),
        rooms=Depends(get_rooms),
        scenarios=Depends(get_scenarios),
):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "devices": devices,
            "scenarios": scenarios,
            "rooms": rooms,
        })


@router.get("/device")
def device(
        request: Request,
        devices=Depends(get_devices),
):
    return templates.TemplateResponse("devices.html", {"request": request, "devices": devices, })


@router.get("/rooms")
def device(
        request: Request,
        rooms=Depends(get_rooms),
):
    return templates.TemplateResponse("rooms.html", {"request": request, "rooms": rooms, })


@router.get("/scenarios")
def device(
        request: Request,
        scenarios=Depends(get_scenarios),
):
    return templates.TemplateResponse("scenarios.html", {"request": request, "scenarios": scenarios,})

from fastapi import APIRouter, Request, Depends
import requests

from src.yandex_client.schema import DeviceSchema, ScenariosSchema, RoomsSchema

router = APIRouter(
    prefix="/yandex",
    tags=["YandexService"],
)

# Dependency
def get_home_info(
    request: Request,
):
    token = request.cookies.get("FBKI-token-home")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(
        url="https://api.iot.yandex.net/v1.0/user/info",
        headers=headers).json()


@router.get("/devices")
def get_devices(
        home_list: dict = Depends(get_home_info)
):
    return [DeviceSchema(
        id=device["id"],
        name=device["name"]
    ) for device in home_list["devices"]]


@router.get("/rooms")
def get_rooms(
        home_list: dict = Depends(get_home_info)
):
    return [RoomsSchema(
        id=room["id"],
        name=room["name"],
        household_id=room["household_id"],
        devices=room["devices"]
    ) for room in home_list["rooms"]]


@router.get("/scenarios")
def get_scenarios(
        home_list: dict = Depends(get_home_info)
):
    return [ScenariosSchema(
        id=scenario["id"],
        name=scenario["name"],
        is_active=scenario["is_active"]
    ) for scenario in home_list["scenarios"]]


@router.post("/execute-scenario")
def execute_scenario(
        scenario_id: str,
        request: Request
):
    url = f"https://api.iot.yandex.net/v1.0/scenarios/{scenario_id}/actions"
    token = request.cookies.get("FBKI-token-home")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    if not response.status_code == 200:
        return f"Ошибка при выполнении сценария: {response.status_code} - {response.text}"
    return f"Сценарий с ID {scenario_id} успешно выполнен."

from fastapi import APIRouter, Request
import requests

router = APIRouter(
    prefix="/yandex",
)


@router.get("/devices")
def get_devices(
        request: Request,
):
    token = request.cookies.get("FBKI-token-home")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return requests.get(
        url="https://api.iot.yandex.net/v1.0/user/info",
        headers=headers).json()


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


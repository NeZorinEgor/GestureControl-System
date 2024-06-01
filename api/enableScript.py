import requests

OAUTH_TOKEN = ''

def execute_scenario(scenario_id):
    url = f"https://api.iot.yandex.net/v1.0/scenarios/{scenario_id}/actions"
    headers = {
        'Authorization': f'Bearer {OAUTH_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(f"Сценарий с ID {scenario_id} успешно выполнен.")
    else:
        print(f"Ошибка при выполнении сценария: {response.status_code} - {response.text}")

# Пример использования
scenario_id = ''  # Замените на ID вашего сценария
execute_scenario(scenario_id)

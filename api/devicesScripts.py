import requests

OAUTH_TOKEN = ''

def get_devices():
    url = "https://api.iot.yandex.net/v1.0/user/info"
    headers = {
        'Authorization': f'Bearer {OAUTH_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        devices = response.json()["devices"]
        scenarios = response.json()["scenarios"]
        print(devices)
        for device in devices:
            print(f"Device ID: {device['id']}, Name: {device['name']}")
        for scenarie in scenarios:
            print(f"Scenario ID: {scenarie['id']}, Name: {scenarie['name']}")
    else:
        print("Ошибка при получении списка устройств:", response.text)

# Получение списка устройств
get_devices()

import requests
import sys


params = sys.argv[1:]
base_url = params[0]
scenario_id = params[1]
oauth_token = params[2]



# Параметры запроса
params = {
    'scenario_id': scenario_id
}

# Заголовки запроса, если необходимы
headers = {
    'Content-Type': 'application/json',
    # Добавьте другие заголовки, если необходимо
}

# Куки для запроса
cookies = {
    'FBKI-token-home': oauth_token
}

# Дополнительные данные для POST запроса, если необходимы
data = {
    # 'key1': 'value1',
    # 'key2': 'value2',
}

# Отправка POST запроса
response = requests.post(base_url, params=params, json=data, headers=headers, cookies=cookies)

# Обработка ответа
if response.status_code == 200:
    print('Запрос выполнен успешно:', response.json())
else:
    print('Ошибка выполнения запроса:', response.status_code, response.text)

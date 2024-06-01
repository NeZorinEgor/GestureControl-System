import webbrowser
import requests
from flask import Flask, request

app = Flask(__name__)

CLIENT_ID = ''  # Замените на ваш реальный client_id
CLIENT_SECRET = ''  # Замените на ваш реальный client_secret
REDIRECT_URI = 'http://localhost:8000/callback'

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://oauth.yandex.ru/token'
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        print(f"Access Token: {access_token}")
        return "Token received. Check console for details."
    else:
        print("Error:", response.text)
        return "Error retrieving token."

if __name__ == '__main__':
    # Открытие URL авторизации в веб-браузере
    authorization_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    webbrowser.open(authorization_url)
    
    # Запуск Flask сервера
    app.run(port=8000)

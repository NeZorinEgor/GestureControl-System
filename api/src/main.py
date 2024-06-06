import webbrowser

import requests
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse

from src.config import settings
from src.yandex_client.router import router as yandex_router


app = FastAPI(
    title="Yandex-Client",
    docs_url="/"
)


app.include_router(yandex_router)


REDIRECT_URI = 'http://localhost:8000/callback'


auth_token = None

@app.on_event("startup")
def startup():
    global auth_token
    authorization_url = f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    webbrowser.open(authorization_url)
    print("start")


@app.get('/callback')
async def callback(
        request: Request,
        response: Response,
):
    code = request.query_params.get('code')
    token_url = 'https://oauth.yandex.ru/token'

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }

    res = requests.post(
        allow_redirects=True,
        url=token_url,
        data=data
    )
    # return res.json()
    response.set_cookie("FBKI-token-home", res.json()["access_token"])
    return RedirectResponse(
        url="/"
    )

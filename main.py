#Нужен тг бот,и  внесение данных о боте в файл settings.py
import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


from django_telegram_login.widgets.constants import (
    MEDIUM,
    DISABLE_USER_PHOTO,
)
from django_telegram_login.widgets.generator import (
    create_redirect_login_widget,
)
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError, 
    TelegramDataIsOutdatedError,
)
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

#в файле settings.py нужно добавить переменные 
bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN
redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL

@app.get('/')
def redirect(request: Request):
    telegram_login_widget = create_redirect_login_widget(
        redirect_url, bot_name, size=MEDIUM, user_photo=DISABLE_USER_PHOTO
    )

    context = {"request": request, 'telegram_login_widget': telegram_login_widget}
    return templates.TemplateResponse('redirect.html', context)

@app.get('/redirect')
def redirect_to_url(request: Request):
    user_data = dict(request)
    #data = int(str(user_data['query_string'])[2:].split('&')[0].split('=')[1])
    data = str(user_data['query_string'])[2:].split('&')
    print(data)

    return "redirect url"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
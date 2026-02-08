import json
from fastapi import FastAPI, Body, HTTPException, Depends
from starlette.responses import HTMLResponse
from typing import Dict
from config_data.api_config import verify_telegram_init_data, create_access_token, get_current_user_id
from config_data.config import BOT_TOKEN

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "habit_backend"}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/webapp", response_class=HTMLResponse)
def webapp():
    return """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Auth</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
  <h3>Авторизация...</h3>

  <script>
    const tg = window.Telegram.WebApp;
    tg.ready();

    const initData = tg.initData;

    if (!initData || initData.length === 0) {
      document.body.innerText = "initData пустой. Открой мини-приложение через WebApp кнопку/меню.";
    } else {
      fetch("https://habit-backend-awul.onrender.com/auth/telegram-webapp", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ init_data: initData })
      })
      .then(async r => {
        const data = await r.json();
        if (!r.ok) {
          document.body.innerText = "Ошибка авторизации: " + JSON.stringify(data);
          return;
        }
        tg.sendData(JSON.stringify(data));
        tg.close();
      })
      .catch(err => {
        document.body.innerText = "Ошибка авторизации: " + err;
      });
    }
  </script>
</body>
</html>
"""


@app.post('/auth/telegram-webapp')
def auth_telegram_webapp(payload: Dict = Body(...)):
    """
    Сюда приходит initData
    В функции идёт проверка подписи и создании сессии
    :param payload:
    :return: session_id
    """
    init_data = payload.get('init_data')
    print("PAYLOAD:", payload)
    if not init_data:
        raise HTTPException(status_code=400, detail='initData is required')

    try:
        parsed = verify_telegram_init_data(init_data, BOT_TOKEN)
        user = json.loads(parsed['user'])
        tg_user_id = int(user['id'])
        access_token = create_access_token(tg_user_id)
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid Telegram InitData')
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/me')
def me(user_id: int = Depends(get_current_user_id)):
    return {'user_id': user_id}


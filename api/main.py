import json
from fastapi import FastAPI, Body, HTTPException, Depends
from starlette.responses import HTMLResponse
from typing import Dict
from config_data.api_config import verify_telegram_init_data, create_access_token, get_current_user_id
from config_data.config import BOT_TOKEN
from database.notify_user import notify_user, upsert_token
from database.init_db import init_db

app = FastAPI()

MAIN_MENU_MARKUP = {
    "keyboard": [
        [{"text": "📋Привычки📋"}, {"text": "✅Сегодня✅"}],
        [{"text": "➕Добавить➕"}, {"text": "🔔Уведомление🔔"}],
    ],
    "resize_keyboard": True,
}


@app.on_event("startup")
def on_startup():
    init_db()


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

    function readInitDataFromUrl() {
      const href = window.location.href || "";
      const match = href.match(/[?&#]tgWebAppData=([^&]+)/);
      if (!match || !match[1]) return "";
      try {
        return decodeURIComponent(match[1]);
      } catch (_) {
        return match[1];
      }
    }

    const initData = tg.initData || readInitDataFromUrl();

    if (!initData || initData.length === 0) {
      document.body.innerText = "initData пустой. Открой мини-приложение кнопкой «🔐 Войти» в личном чате с ботом и обнови Telegram до последней версии.";
    } else {
      (async () => {
        try {
          const r = await fetch("/auth/telegram-webapp", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ init_data: initData })
          });

          const raw = await r.text();
          let data = null;
          try {
            data = raw ? JSON.parse(raw) : {};
          } catch (_) {
            throw new Error("Невалидный ответ сервера: " + raw.slice(0, 300));
          }

          if (!r.ok) {
            document.body.innerText = "Ошибка авторизации: " + JSON.stringify(data);
            return;
          }

          document.body.innerText = "Отправляю токен в бота...";
          try {
            tg.sendData(JSON.stringify(data));
          } catch (e) {
            document.body.innerText = "sendData ERROR: " + (e?.message || e);
            throw e;
          }

          setTimeout(() => {
            document.body.innerText = "Отправлено. Закрываю...";
            tg.close();
          }, 1200);
        } catch (err) {
          document.body.innerText = "Ошибка авторизации: " + (err?.message || err);
        }
      })();
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
    if not init_data:
        raise HTTPException(status_code=400, detail='initData is required')

    try:
        parsed = verify_telegram_init_data(init_data, BOT_TOKEN)
        print('Verify ok')
        user = json.loads(parsed['user'])
        tg_user_id = int(user['id'])
        access_token = create_access_token(tg_user_id)
        print('Token ok')
    except Exception as e:
        print('auth error:', repr(e))
        raise HTTPException(status_code=401, detail='Invalid Telegram InitData')

    try:
        upsert_token(tg_user_id, access_token)
    except Exception as e:
        print("token save error:", repr(e))
        raise HTTPException(status_code=500, detail='Token save failed')

    try:
        notify_user(tg_user_id, "✅Авторизация прошла успешно✅\n\n"
                        "Главное меню:\n\n"
                        "Привычки - показывает список привычек\n"
                        "Сегодня - Отметить привычку сделанная или нет\n"
                        "Добавить - добавить привычки\n"
                        "Уведомление - настройка уведомлений",
                    reply_markup=MAIN_MENU_MARKUP)
    except Exception as e:
        print("notify error:", repr(e))
    return {"ok": True, "access_token": access_token, "token_type": "bearer"}


@app.get('/me')
def me(user_id: int = Depends(get_current_user_id)):
    return {'user_id': user_id}

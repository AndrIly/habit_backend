from fastapi import FastAPI, Body
from starlette.responses import HTMLResponse
import uuid
from typing import Dict


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

  document.body.innerText = "1) Telegram WebApp OK. Запрашиваю session_id...";

  fetch("https://habit-backend-awul.onrender.com/auth/telegram-webapp", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ init_data: tg.initData })
  })
  .then(r => r.json())
  .then(data => {
    document.body.innerText = "2) Ответ backend: " + JSON.stringify(data) + "\\n3) Отправляю в бот...";
    tg.sendData(JSON.stringify(data));
    document.body.innerText += "\\n4) sendData вызван ✅ (страницу не закрываю для проверки)";
    // tg.close(); // временно выключено
  })
  .catch(err => {
    document.body.innerText = "Ошибка: " + err;
  });
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
    return {"session_id": str(uuid.uuid4())}


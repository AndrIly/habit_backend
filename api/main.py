from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/webapp", response_class=HTMLResponse)
def webapp_page():
    return """
    ``<!doctype html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>Auth</title>
      <script src="https://telegram.org/js/telegram-web-app.js"></script>
    </head>
    <body>
      <h3>Авторизация...</h3>
      <p id="status">Подключаемся</p>
    
      <script>
        const tg = window.Telegram.WebApp;
        tg.ready();
    
        const initData = tg.initData; // строка initData
    
        async function auth() {
          try {
            const res = await fetch("/auth/telegram-webapp", {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({ init_data: initData })
            });
    
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "Auth failed");
    
            // Отправляем session_id в бот
            tg.sendData(JSON.stringify({ session_id: data.session_id, expires_at: data.expires_at }));
            document.getElementById("status").innerText = "Готово! Возвращаюсь в бот...";
            tg.close();
          } catch (e) {
            document.getElementById("status").innerText = "Ошибка авторизации: " + e.message;
          }
        }
    
        auth();
      </script>
    </body>
    </html>
    """
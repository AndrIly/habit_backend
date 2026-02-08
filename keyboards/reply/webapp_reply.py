from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

WEBAPP_URL = 'https://habit-backend-awul.onrender.com/webapp'
def auth_reply():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton(
            "🔐 Войти",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    return kb
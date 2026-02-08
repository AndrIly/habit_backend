from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

def auth_reply():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton(
            "🔐 Войти",
            web_app=WebAppInfo(url="https://habit-backend-awul.onrender.com/webapp")
        )
    )
    return kb
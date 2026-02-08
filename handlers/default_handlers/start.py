from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telebot.types import Message
from loader import bot

WEBAPP_URL = "https://habit-backend-awul.onrender.com/webapp"

def auth_inline():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔐 Войти", web_app=WebAppInfo(url=WEBAPP_URL)))
    return kb

@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(message.chat.id, "Нажми кнопку для авторизации:", reply_markup=auth_inline())




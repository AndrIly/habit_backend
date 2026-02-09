from telebot import types
from telebot.types import Message
from loader import bot

WEBAPP_URL = "https://habit-backend-awul.onrender.com/webapp"

@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=types.MenuButtonWebApp(
            type = 'web_app',
            text="Открыть приложение",
            web_app=types.WebAppInfo(url=WEBAPP_URL)
        )
    )
    bot.send_message(message.chat.id, "Открой мини-приложение через кнопку меню «Открыть приложение».")


from telebot import types
from telebot.types import Message
from loader import bot
from keyboards.reply.webapp_reply import auth_reply

@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=types.MenuButtonCommands(type='commands')
    )
    bot.send_message(
        message.chat.id,
        "Нажми кнопку «🔐 Войти» ниже для авторизации.",
        reply_markup=auth_reply()
    )

from telebot import types
from telebot.types import Message
from loader import bot

@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=types.MenuButtonCommands(type='commands')
    )

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔐 Войти", callback_data="login_inline"))
    bot.send_message(
        message.chat.id,
        "Нажми кнопку «🔐 Войти» ниже для авторизации.",
        reply_markup=kb
    )

import json

from telebot.types import Message

from database.tokens import upsert_token
from keyboards.reply.button_reply import main_menu
from loader import bot


@bot.message_handler(content_types=['web_app_data'])
def on_webapp_data(message: Message):
    raw = message.web_app_data.data if message.web_app_data else ''
    try:
        data = json.loads(raw) if raw else {}
    except Exception:
        bot.send_message(message.chat.id, "Ошибка: не удалось прочитать данные авторизации.")
        return

    token = data.get('access_token')
    if not token:
        bot.send_message(message.chat.id, "Ошибка: токен авторизации не пришел.")
        return

    upsert_token(message.from_user.id, token)
    bot.send_message(
        message.chat.id,
        "✅Авторизация прошла успешно✅",
        reply_markup=main_menu()
    )

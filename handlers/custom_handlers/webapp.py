import json
from telebot.types import Message
from database.tokens import upsert_token
from keyboards.reply.button_reply import main_menu
from loader import bot




@bot.message_handler(content_types=["web_app_data"])
def on_webapp_data(message: Message):
    data = json.loads(message.web_app_data.data)

    tokens = data.get('access_token')
    if not tokens:
        bot.send_message(message.chat.id, 'Не пришёл access_token')
        return

    upsert_token(message.from_user.id, tokens)
    bot.send_message(message.chat.id, '✅Авторизация прошла успешно✅', reply_markup=main_menu())
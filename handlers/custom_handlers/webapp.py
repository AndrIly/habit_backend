import json
from telebot.types import Message
from database.tokens import upsert_token
from keyboards.reply.button_reply import main_menu
from loader import bot

@bot.message_handler(content_types='web_app_data')
def on_webapp_data(message: Message):
    print('Я работаю')
    data = json.loads(message.web_app_data.data)
    bot.send_message(message.chat.id, "web_app_data получен")
    token = data.get('access_token')
    if not token:
        bot.send_message(message.chat.id, f'Не пришёл access_token\n Пришло: {data}')
        return

    upsert_token(message.from_user.id, token)
    bot.send_message(message.chat.id, '✅Авторизация прошла успешно✅', reply_markup=main_menu())


import json
from telebot.types import Message
from database.tokens import upsert_token
from keyboards.reply.button_reply import main_menu
from config_data.api_config import create_access_token
from loader import bot


def do_local_auth(message: Message):
    token = create_access_token(message.from_user.id)
    upsert_token(message.from_user.id, token)
    bot.send_message(
        message.chat.id,
        "✅Авторизация прошла успешно✅",
        reply_markup=main_menu()
    )


@bot.message_handler(commands=["login"])
def auth_from_command(message: Message):
    do_local_auth(message)


@bot.callback_query_handler(func=lambda call: call.data == "login_inline")
def auth_from_inline(call):
    bot.answer_callback_query(call.id)
    do_local_auth(call.message)


@bot.message_handler(func=lambda m: ((m.text or "").strip().lower() in {"🔐 войти", "войти"}))
def auth_from_reply_button(message: Message):
    do_local_auth(message)


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

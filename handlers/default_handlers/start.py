from telebot import types
from telebot.types import Message
from loader import bot
from config_data.config import WEBAPP_URL


@bot.callback_query_handler(func=lambda call: True)
def debug_callback(call):
    print("CALLBACK ARRIVED:", call.data)

@bot.message_handler(commands=["start"])
def start(message: Message):
    print('Handler start')
    bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=types.MenuButtonCommands(type='commands')
    )
    bot.send_message(message.chat.id,
                     'Этот бот помогает выстроить и поддерживать полезные привычки\n'
                     'Функционал бота:\n\n'
                     '\t- Создать привычки (например: спорт, чтения, режим сна);'
                     '\n\t- Настроить напоминание по времени;\n'
                     '\t- Отмечать выполненые привычки каждый день;\n'
                     '\t- Видеть, какие привычки выполнены, а какие пропущены.\n\n'
                     'Чтоб пользоватся ботом нужно авторизаваться')
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "🔐 Войти",
        web_app=types.WebAppInfo(url=WEBAPP_URL)
    ))
    bot.send_message(
        message.chat.id,
        "Нажми «🔐 Войти», чтобы открыть сайт и авторизоваться.",
        reply_markup=kb
    )

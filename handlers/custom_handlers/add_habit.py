from telebot.types import Message
from loader import bot
from database.habits import create_habit
from keyboards.reply.button_reply import add_btn, main_menu
from typing import Dict

USER_STATE: Dict[int, str] = {}


@bot.message_handler(func= lambda message: message.text == add_btn)
def add_start(message: Message):
   USER_STATE[message.from_user.id] = 'Ждем название привычки'
   bot.send_message(message.chat.id, 'Напиши название привычки')


@bot.message_handler(func = lambda message: USER_STATE.get(message.from_user.id) == 'Ждем название привычки')
def add_finish(message: Message):
    title = (message.text or '').strip()
    if not title:
        bot.send_message(message.chat.id, 'Название пустое. Напиши ещё раз.')
        return

    create_habit(tg_user_id=message.from_user.id, title=title)
    USER_STATE.pop(message.from_user.id, None)

    bot.send_message(message.chat.id, 'Привычка {title} добавлена'.format(title=title), reply_markup=main_menu())

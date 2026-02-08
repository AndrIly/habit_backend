from telebot.types import Message
from loader import bot
from database.habits import get_user_habits
from keyboards.reply.button_reply import habits_btn

@bot.message_handler(func = lambda message: message.text == habits_btn)
def list_habits_handler(message: Message):
    rows = get_user_habits(tg_user_id=message.from_user.id)
    if not rows:
        bot.send_message(message.chat.id, 'Пока нет привычек.')
        return

    text = 'Список твоих привычек:\n\n'
    for r in rows:
        habit, title = r[0], r[1]
        text += '{title}\n'.format(title=title)

    bot.send_message(message.chat.id, text)
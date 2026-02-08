from telebot.types import Message
from loader import bot
from database.logs import mark_done, mark_undone, get_today_status

@bot.message_handler(commands=['done'])
def done_handler(message: Message):
    parts = message.text.split(' ')

    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id,
                         'Используется: /done ID')
        return

    habit_id = int(parts[1])
    ok = mark_done(tg_user_id=message.from_user.id, habit_id=habit_id)

    if not ok:
        bot.send_message(message.chat.id, "Привычка не найдена")
        return

    bot.send_message(message.chat.id, "Отмечено выполненным (ID {habit})".format(habit=habit_id))


@bot.message_handler(commands=['undone'])
def undone_handler(message: Message):
    parts = message.text.split(' ')
    if len(parts) != 2 or not parts[1].isdigit():
        bot.send_message(message.chat.id, 'Используйте: /undone ID')
        return

    habit_id = int(parts[1])
    ok = mark_undone(tg_user_id=message.from_user.id, habit_id=habit_id)
    if not ok:
        bot.send_message(message.chat.id, 'Привычка не обнаруженна')
        return

    bot.send_message(message.chat.id, 'Отметил что привычка не выполненна')


@bot.message_handler(func=lambda message: message.text == '')
def today_handler(message: Message):
    rows, day = get_today_status(tg_user_id=message.from_user.id)

    if not rows:
        bot.send_message(message.chat.id, 'у тебя пока нет привычек. Добавь: /add_habit Название')
        return

    done = []
    todo = []

    for r in rows:
        habit_id = r[0]
        title = r[1]
        is_done = r[2]

        line = '{habit}. {title}'.format(habit=habit_id, title=title)
        if is_done:
            done.append(line)
        else:
            todo.append(line)

    text = (f'Сегодня: {day}\n\n'
            'Сделано: \n' + ('\n'.join(done) if done else '') + '\n\n'
            'Не сделано: \n' + ('\n'.join(todo) if todo else '') + '\n\n'
            'Отметить: /done ID \nСнять: /undone ID')
    bot.send_message(message.chat.id, text)
from telebot.types import Message, CallbackQuery
from loader import bot
from database.logs import get_today_status, mark_done, mark_undone
from keyboards.inline.today_inline import today_habit
from database.habits import delete_habit


@bot.message_handler(func = lambda m: m.text == '✅Сегодня✅')
def today_list(message: Message):
    rows, day = get_today_status(tg_user_id=message.from_user.id)

    if not rows:
        bot.send_message(message.chat.id, 'Пока нет привычек. Чтобы добавить нажми ➕')
        return

    bot.send_message(message.chat.id, 'Сегодня: {day}'.format(day=day))

    for r in rows:
        habit_id, title, is_done = r[0], r[1], r[2]
        if is_done:
            status = '✅'
        else:
            status = '➖'

        bot.send_message(message.chat.id,
                         '{status}  {title}'.format(
                             status=status,  title=title
                         ),
                         reply_markup=today_habit(habit_id=habit_id, is_done=is_done, has_reminder=False))


@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith('done:'))
def done_habit(call: CallbackQuery):
    habit_id = int(call.data.split(':')[1])
    done = mark_done(tg_user_id=call.from_user.id, habit_id=habit_id)

    if not done:
        bot.answer_callback_query(call.id, 'Привычка не найдена', show_alert = True)
        return

    old_text = call.message.text
    if old_text.startswith('➖'):
        new_text = old_text.replace('➖', '✅', 1)
    else:
        new_text = old_text

    bot.edit_message_text(text=new_text,
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=today_habit(habit_id=habit_id, is_done = 1, has_reminder = False))

    bot.answer_callback_query(call.id,
                              'Отмечено ✅')


@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith('undone:'))
def undone_habit(call: CallbackQuery):
    habit_id = int(call.data.split(':')[1])
    undone = mark_undone(tg_user_id=call.from_user.id, habit_id=habit_id)

    if not undone:
        bot.answer_callback_query(call.message.chat.id, 'Привычка не еайдена', show_alert = True)
        return
    old_text = call.message.text
    if old_text.startswith('✅'):
        new_text = old_text.replace('✅', '➖', 1)
    else:
        new_text = old_text
    bot.edit_message_text(text=new_text,
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=today_habit(habit_id=habit_id, is_done=0, has_reminder=False))

    bot.answer_callback_query(call.id,'Снято ⏪')


@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith('del:'))
def del_habit(call: CallbackQuery):
    habit_id = int(call.data.split(':')[1])
    delete_habit(tg_user_id=call.from_user.id, habits_id=habit_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.message.chat.id, 'Удалено🗑️')


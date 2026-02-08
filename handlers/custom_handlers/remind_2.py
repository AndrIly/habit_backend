from telebot.types import CallbackQuery
from loader import bot
from database.habits import toggle_habit_reminder, get_habits_reminder_info
from keyboards.inline.reminder_inline import reminder_inline


@bot.callback_query_handler(func=lambda call: call.data  and call.data.startswith('r_toggle:'))
def cd_reminder(call: CallbackQuery):
    """
    Переключатель ВКЛ\ВЫКЛ на экране уведомление
    Используется функции: toggle_habit_reminder, get_habits_reminder_info, reminder_inline
    :param call: CallbackQuery
    :return: None
    """
    parts = call.data.split(':', 1)
    if len(parts) != 2 or not parts[1].strip().isdigit():
        bot.answer_callback_query(call.id, 'Ошибка данных', show_alert=True)
        return

    habit_id = int(parts[1].strip())
    func = toggle_habit_reminder(call.from_user.id, habit_id)
    if not func:
        bot.answer_callback_query(call.id, 'Привычка не найдена', show_alert=True)
        return

    rows = get_habits_reminder_info(call.from_user.id, habit_id)
    if not rows:
        bot.answer_callback_query(call.id, 'Привычка не найдена', show_alert=True)
        return

    title, reminder_time, reminder_active = rows[1], rows[2], rows[3]

    time_text = reminder_time if reminder_time else '--'
    status = '🔔' if reminder_active and reminder_time else '🔕'

    new_text = '{status}  {title} \nВремя: {time_text}'.format(
        status=status,
        title=title,
        time_text=time_text
    )
    bot.edit_message_text(text=new_text,
                          chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          reply_markup=reminder_inline(habit_id, reminder_active))
    bot.answer_callback_query(call.id, 'Готово')




from telebot.types import Message, CallbackQuery
from database.habits import get_user_habits
from loader import bot
from keyboards.inline.reminder_inline import reminder_inline


def render_reminder(chat_id: int, user_id: int) -> None:
    """
    Функция экрана напоминания чтоб её в будущем можно было вызываеть
    Используемые функции: reminder_inline
    :param chad_id:
    :param user_id:
    :return: None
    """
    rows = get_user_habits(user_id)

    if not rows:
        bot.send_message(chat_id, 'Пока нет привычек')
        return

    bot.send_message(chat_id, '🔔Напоминание по привычкам:')
    for r in rows:
        habit_id = r[0]
        title = r[1]
        reminder_active = r[4]
        reminder_time = r[3]

        time_text = reminder_time if reminder_time else ' -- '
        status = '🔔' if reminder_active else '🔕'

        bot.send_message(chat_id, '{status} {title}. \nВремя: {time_text}'.format(
            status=status,
            title=title,
            time_text=time_text
        ), reply_markup=reminder_inline(habit_id, reminder_active))


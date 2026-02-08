from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


def reminder_inline(habit_id: int, reminder_active: int):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('⏰Время', callback_data='r_settime:{habit_id}'.format(habit_id=habit_id)),
        InlineKeyboardButton('🔕Выкл' if reminder_active else '🔔Вкл', callback_data='r_toggle: {habit_id}'.format(
            habit_id=habit_id)
    ))
    return keyboard
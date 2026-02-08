from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def today_habit(habit_id: int, is_done: int, has_reminder: bool):
    keyboard = InlineKeyboardMarkup()

    if is_done:
        keyboard.add(InlineKeyboardButton('🏗️Снять', callback_data = 'undone: {habit}'.format(habit = habit_id)))
    else:
        keyboard.add(InlineKeyboardButton('✅Сделал', callback_data = 'done: {habit}'.format(habit = habit_id)))

    keyboard.add(InlineKeyboardButton('⏱️Время', callback_data = 'settime: {habit}'.format(habit = habit_id)))
    keyboard.add(InlineKeyboardButton('🗑️Удалить', callback_data = 'del: {habit}'.format(habit = habit_id)))
    return keyboard
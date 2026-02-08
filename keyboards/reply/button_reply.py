from telebot.types import ReplyKeyboardMarkup, KeyboardButton

today_btn = '✅Сегодня✅'
habits_btn = '📋Привычки📋'
add_btn = '➕Добавить➕'
reminder_btn = '🔔Уведомление🔔'

def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton(habits_btn), KeyboardButton(today_btn))
    keyboard.row(KeyboardButton(add_btn), KeyboardButton(reminder_btn))
    return keyboard
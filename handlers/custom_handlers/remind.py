from telebot.types import Message, CallbackQuery
from loader import bot
from database.habits import set_habit_reminder
from typing import Dict
from keyboards.reply.button_reply import reminder_btn
from keyboards.inline.remind_screen import render_reminder

wait_time: Dict[int, int] = {}

def valid_time(value: str) -> bool:
    """
    Функция которая проверяет формат времени. Проверяет часы и минуты
    :param value: str
    :return: bool
    """
    try:
        h, m = value.split(':')
        h = int(h)
        m = int(m)
        return 0 <= h <= 23 and 0 <= m <= 59
    except Exception:
        return False

@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith('settime:'))
def set_reminder(call: CallbackQuery):
    """
    Кнопка время в меню Сегодня, запрос к пользователю чтоб отправил время
    Внешние переменные: wait_time
    :param call: CallbackQuery
    :return: None
    """
    habit_id = int(call.data.split(':')[1])
    wait_time[call.from_user.id] = habit_id
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Напиши время для привычки в формате HH:MM')


@bot.message_handler(
    func=lambda message: message.from_user
    and wait_time.get(message.from_user.id) is not None
    and (message.text or '').strip().lower() not in {'🔐 войти', 'войти'}
)
def settime_finished(message: Message):
    """
    Настройка времени
    Внешние переменные: wait_time
    Используется функции: valid_time, set_habit_reminder, render_reminder
    :param message: Message
    :return:
    """
    habit_id = wait_time[message.from_user.id]
    value = (message.text or '').strip()
    valid_bool = valid_time(value)
    if not valid_bool:
        bot.send_message(message.chat.id, 'Неверный формат ввода времени')
        return
    set_habit_reminder(tg_user_id=message.from_user.id, habit_id=habit_id, reminder_time=value)
    wait_time.pop(message.from_user.id, None)
    bot.send_message(message.chat.id, 'Время установлено: {}'.format( value))
    render_reminder(message.chat.id, message.from_user.id)


@bot.message_handler(func=lambda message: message.text == reminder_btn)
def reminders_screen(message: Message):
    """
    Экран уведомления
    :param message: Message
    :return: None
    """
    render_reminder(message.chat.id, message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith('r_settime:'))
def set_reminder_from_screen(call: CallbackQuery):
    """
    Кнопка время на экране уведомления. ВЫЗЫВАЕТСЯ r-settime:
    Внешние переменные: wait_time
    :param call:
    :return: None
    """
    parts = call.data.split(':', 1)

    if len(parts) != 2 or not parts[1].isdigit():
        bot.answer_callback_query(call.id, 'Ошибка данных', show_alert=True)
        return
    habit_id = int(parts[1].strip())
    wait_time[call.from_user.id] = habit_id
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Напиши время для привычки в формате HH:MM')

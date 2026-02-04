from telebot.types import Message
from loader import bot
from keyboards.button_reply import choice_in_main, setting_reply, done_reply, notification_reply

@bot.message_handler(func=lambda message: message.text and message.text in ('Главное меню🚪', '🚪 - Назад в главное меню'))
def menu(message: Message):
    bot.send_message(message.chat.id,
                     'Главное меню:\n'
                     '\t⚙️️ - Настройка трекинга;\n'
                     '\t✅ - Выполненные привычки;\n'
                     '\t🔔 - Привычки с уведомлением',
                     reply_markup=choice_in_main())


@bot.message_handler(func=lambda message: message.text == '⚙️️')
def settings_habit(message: Message):
    bot.send_message(message.chat.id,
                     "Настройка трекинга:\n"
                     "\t✍️ - Создать привычку;\n"
                     "\t🗑️ - Удалить привычку;\n"
                     "\t📝 - Редактировать имеющиеся привычку;",
                     reply_markup=setting_reply()
                     )


@bot.message_handler(func=lambda message: message.text == '✅')
def done_habit(message: Message):
    bot.send_message(message.chat.id,
                     'Выберите что хотите сделать:\n'
                     '\t📋- Посмотреть полностью список привычек;\n'
                     '\t☑️- Отметить привычку: выполнил / не выполнил;\n'
                     '\t❎- Посмотреть список с не выполненными привычками;\n',
                     reply_markup=done_reply(),)


@bot.message_handler(func=lambda message: message.text == '🔔')
def notification(message: Message):
    bot.send_message(message.chat.id,
                     'Выберите что хотите сделать:\n'
                     '\t📋🔔 - Посмотреть привычки с уведомлением;\n'
                     '\t⚙️🔔 - Добавить или удалить действие с уведомлением\n'
                     '\t🔕 - Отключить полностью уведомления',
                     reply_markup=notification_reply()
                     )

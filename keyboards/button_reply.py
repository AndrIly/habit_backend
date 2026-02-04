from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def menu_button():
    button = KeyboardButton('Главное меню🚪')
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(button)
    return keyboard


def choice_in_main():
    button_1 = KeyboardButton('⚙️️')
    button_2 = KeyboardButton('✅')
    button_3 = KeyboardButton('🔔')

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(button_1, button_2, button_3)
    return keyboard


def setting_reply():
    button_1 = KeyboardButton('✍️')
    button_2 = KeyboardButton('🗑️')
    button_3 = KeyboardButton('📝')
    button_4 = KeyboardButton('🚪 - Назад в главное меню')

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(button_1, button_2, button_3, button_4)
    return keyboard


def done_reply():
    button_1 = KeyboardButton('📋')
    button_2 = KeyboardButton('☑️')
    button_3 = KeyboardButton('❎')
    button_4 = KeyboardButton('🚪 - Назад в главное меню')
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(button_1, button_2, button_3, button_4)
    return keyboard


def notification_reply():
    button_1 = KeyboardButton('📋🔔')
    button_2 = KeyboardButton('⚙️🔔️')
    button_3 = KeyboardButton('🔕')
    button_4 = KeyboardButton('🚪 - Назад в главное меню')
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(button_1, button_2, button_3, button_4)
    return keyboard
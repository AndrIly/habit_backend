from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def auth_inline():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Войти🔐', web_app = WebAppInfo(url=webapp_url)))
    return keyboard
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
def auth_reply():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🔐 Войти"))
    return kb

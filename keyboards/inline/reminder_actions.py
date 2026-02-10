from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def reminder_actions(habit_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("✅ Сделал", callback_data=f"rem_done:{habit_id}"),
        InlineKeyboardButton("⏳ Позже", callback_data=f"rem_later:{habit_id}"),
    )
    return kb

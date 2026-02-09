from database import init_db
from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from database.init_db import init_db
from scheduler import start_scheduler


init_db()
start_scheduler()
if __name__ == "__main__":
    set_default_commands(bot)
    bot.infinity_polling(skip_pending=True)

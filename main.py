from database import init_db
from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from database.init_db import init_db
from scheduler import start_scheduler


#init_db()
start_scheduler()
import os

RUN_POLLING = os.getenv("RUN_POLLING", "0") == "1"

if __name__ == "__main__":
    if RUN_POLLING:
        bot.infinity_polling(skip_pending=True)
    else:
        print("Polling disabled")

#if __name__ == "__main__":
#    set_default_commands(bot)
#   bot.infinity_polling(skip_pending=True)

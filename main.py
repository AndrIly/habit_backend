from loader import bot
from utils.set_bot_commands import set_default_commands
from database.init_db import init_db
from scheduler import start_scheduler
import logging

init_db()
start_scheduler()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
       print("Starting bot...")
       logger.info("Starting bot...")
       set_default_commands(bot)
       bot.infinity_polling()

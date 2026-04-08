from fastapi import FastAPI
import telebot
import json
import logging
from loader import bot
from utils.set_bot_commands import set_default_commands
from database.init_db import init_db
from scheduler import start_scheduler
import handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()
    set_default_commands(bot)
    print(bot.get_me())
    print("Starting bot...")


@app.post("/telegram/webhook")
def telegram_webhook(update: dict):
    print("WEBHOOK UPDATE ARRIVED:", update)
    tg_update = telebot.types.Update.de_json(json.dumps(update))
    bot.process_new_updates([tg_update])
    return {"ok": True}
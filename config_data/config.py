import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALG = 'HS256'
ACCESS_TOKEN_EXPIRATION_SECONDS = 60

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)

from database.db import get_connection
import requests
from config_data.config import BOT_TOKEN

def upsert_token(tg_user_id: int, access_token: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tokens (tg_user_id, access_token)
        VALUES (?, ?)
        ON CONFLICT(tg_user_id) DO UPDATE SET
            access_token=excluded.access_token,
            created_at=CURRENT_TIMESTAMP
    """, (tg_user_id, access_token))
    conn.commit()
    conn.close()


def notify_user(tg_user_id: int, text: str):
    r = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": tg_user_id, "text": text},
        timeout=10
    )
    r.raise_for_status()
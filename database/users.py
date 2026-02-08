from database.db import get_connection

def upsert_user(tg_user_id: int, username: str | None, first_name: str | None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (tg_user_id, username, first_name)
    VALUES (?, ?, ?)
    ON CONFLICT (tg_user_id) DO UPDATE SET
        username = excluded.username,
        first_name = excluded.first_name
    """, (tg_user_id, username, first_name))

    conn.commit()
    conn.close()



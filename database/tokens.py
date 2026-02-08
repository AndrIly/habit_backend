from database.db import get_connection

def upsert_token(tg_user_id: int, access_token: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT Into tokens (tg_user_id, access_token)
    VALUES (?, ?)
    ON CONFLICT (tg_user_id) DO UPDATE SET
        access_token = EXCLUDED.access_token,
        created_at = CURRENT_TIMESTAMP
                   """, (tg_user_id, access_token))
    conn.commit()
    cursor.close()


def get_tokens(tg_user_id: int) -> str | None:
     conn = get_connection()
     cursor = conn.cursor()

     cursor.execute("""
    SELECT access_tokens
    FROM tokens
    WHERE tg_user_id = ?
    """, (tg_user_id,))

     row = cursor.fetchone()
     return row[0] if row else None


def delete_tokens(tg_users_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM tokens
    WHERE tg_user_id = ?
    """, (tg_users_id,))
    conn.commit()
    cursor.close()


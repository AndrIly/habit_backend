from database.db import get_connection

def upsert_session(tg_user_id: int, session):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO user_sessions (tg_user_id, session_id)
    VALUES (?, ?) 
    ON CONFLICT (tg_user_id) DO UPDATE SET
        session_id = excluded.session_id,
        created_at = CURRENT_TIMESTAMP
        ''', (tg_user_id, session))

    conn.commit()
    conn.close()


def get_session(tg_user_id: int) -> int | None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT session_id
    FROM sessions
    WHERE tg_user_id = ?''',
                   (tg_user_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row['session_id']
    else:
        return None
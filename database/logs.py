from datetime import date
from database.db import get_connection


def mark_done(tg_user_id: int, habit_id: int, day: str | None = None) -> bool:

    if day is None:
        day = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id
    FROM habits
    WHERE id = ? AND tg_user_id = ?''',
                   (habit_id, tg_user_id))

    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    cursor.execute('''
    INSERT INTO habit_logs (habit_id, day, is_done)
    VALUES (?, ?, 1)
    ON CONFLICT (habit_id, day) DO UPDATE SET
            is_done = 1
    ''', (habit_id, day))

    conn.commit()
    conn.close()
    return True


def mark_undone(tg_user_id: int, habit_id: int, day: str | None = None) -> bool:
    if day is None:
        day = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id
    FROM habits
    WHERE id = ? AND tg_user_id = ?''',
                   (habit_id, tg_user_id))

    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    cursor.execute('''
    INSERT INTO habit_logs (habit_id, day, is_done)
    VALUES (?, ?, 0)
    ON CONFLICT (habit_id, day) DO UPDATE SET
        is_done = 0''', (habit_id, day))
    conn.commit()
    conn.close()
    return True


def get_today_status(tg_user_id: int,  day: str | None = None):
    if day is None:
        day = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT  
        h.id, 
        h.title,
        COALESCE(hl.is_done, 0) AS is_done
        FROM habits as h
        LEFT JOIN habit_logs as hl 
            ON hl.habit_id = h.id AND hl.day = ?
        WHERE h.tg_user_id = ?
        ORDER BY h.created_at ''',
                   (day, tg_user_id))

    rows = cursor.fetchall()
    conn.close()
    return rows, day
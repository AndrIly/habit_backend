from database.db import get_connection

def create_habit(tg_user_id: int, title: str, description: str | None = None) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO habits( tg_user_id, title, description ) 
    VALUES (?, ?, ?)
    ''', (tg_user_id, title, description))

    conn.commit()
    conn.close()


def get_user_habits(tg_user_id: int) -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id,
            title,
            description,
            reminder_time,
            reminder_active,
            created_at
    FROM habits
    WHERE tg_user_id = ?
    ORDER BY created_at
    ''', (tg_user_id,))

    habits = cursor.fetchall()
    conn.close()
    return habits


def delete_habit(habits_id: int, tg_user_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM habits 
    WHERE id = ? AND tg_user_id = ?''', (habits_id, tg_user_id))

    conn.commit()
    conn.close()


def set_habit_reminder(tg_user_id: int, habit_id: int, reminder_time: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE habits
    SET reminder_time = ?, reminder_active = 1
    WHERE id = ? AND tg_user_id = ?
    ''', (reminder_time, habit_id, tg_user_id))
    conn.commit()
    conn.close()


def disable_habit_reminder(tg_user_id: int, habits_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE habits
    SET reminder_active = 0
    WHERE id = ? AND tg_user_id = ?
    """, (habits_id, tg_user_id))

    conn.commit()
    conn.close()


def toggle_habit_reminder(tg_user_id: int, habit_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE habits
    SET reminder_active = CASE reminder_active WHEN 1 THEN 0 ELSE 1 END
    WHERE id = ? AND tg_user_id = ?
    """, (habit_id, tg_user_id))
    changed = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return changed


def get_habits_reminder_info(tg_user_id: int, habit_id: int):
    """
    :param tg_user_id: int
    :param habits_id: int
    :return: habit_id, title, reminder_time, reminder_active
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id,
        title,
        reminder_time,
        reminder_active
    FROM habits
    WHERE id = ? AND tg_user_id = ?
    ''', (habit_id, tg_user_id))
    row = cursor.fetchone()
    conn.close()
    return row
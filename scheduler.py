import time as t
from datetime import date
from threading import Thread
import schedule
from loader import bot
from database.db import get_connection

def send_due_habit_reminder():
    now = t.strftime('%H:%M')
    today = date.today().isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
    SELECT id,
        tg_user_id,
        title
    FROM habits
    WHERE reminder_active = 1 AND reminder_time = ?''', (now,))

    habits = cursor.fetchall()

    for h in habits:
        habit_id, tg_user_id, title = h[0], h[1], h[2]

        try:
            cursor.execute('''
            INSERT INTO reminder_sends (
                habit_id,
                day,
                time)
            VALUES (?, ?, ?) 
            ''', (habit_id, today, now))
            connection.commit()
        except Exception:
            continue

        bot.send_message(tg_user_id, 'Пора: {title}\n\n Отметить выполненным: /done {habit} \n Статус: /today'.format(
            title=title, habit=habit_id
        ))
    connection.close()


def run_scheduler():
    schedule.every(1).minutes.do(send_due_habit_reminder)
    while True:
        schedule.run_pending()
        t.sleep(1)


def start_scheduler():
    Thread(target=run_scheduler, daemon=True).start()
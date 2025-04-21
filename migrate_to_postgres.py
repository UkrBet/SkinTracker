import os
import sqlite3
from urllib.parse import urlparse

import psycopg2

from config.config import DATABASE_URL  # Імпортуйте DATABASE_URL з config.py

# Конфігурація SQLite
SQLITE_DATABASE = 'brawl_stars_bot.db'


def migrate_skins():
    """Переносить дані про скіни з SQLite до PostgreSQL."""
    if not os.path.exists(SQLITE_DATABASE):
        print(f"Файл бази даних SQLite {SQLITE_DATABASE} не знайдено.")
        return

    sqlite_conn = sqlite3.connect(SQLITE_DATABASE)
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute("SELECT character_name, last_date, skin_name FROM skins")
    skins_data = sqlite_cursor.fetchall()
    sqlite_conn.close()

    if not DATABASE_URL:
        print("Змінна конфігурації DATABASE_URL не встановлена для PostgreSQL.")
        return

    parsed_url = urlparse(DATABASE_URL)
    pg_conn = psycopg2.connect(
        host=parsed_url.hostname,
        port=parsed_url.port,
        user=parsed_url.username,
        password=parsed_url.password,
        database=parsed_url.path[1:]
    )
    pg_cursor = pg_conn.cursor()

    for name, date, skin in skins_data:
        try:
            pg_cursor.execute(
                "INSERT INTO skins (character_name, last_date, skin_name) VALUES (%s, %s, %s) ON CONFLICT (character_name) DO NOTHING",
                (name, date, skin)
            )
        except Exception as e:
            print(f"Помилка при спробі вставки {name}: {e}")

    pg_conn.commit()
    pg_cursor.close()
    pg_conn.close()
    print("Міграція даних про скіни до PostgreSQL завершена.")


if __name__ == "__main__":
    migrate_skins()

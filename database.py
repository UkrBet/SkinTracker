# database.py
import logging
import sqlite3

logger = logging.getLogger(__name__)
DATABASE_NAME = 'brawl_stars_bot.db'


def get_connection():
    """Повертає об'єкт підключення до бази даних SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def close_connection(connection):
    """Закриває підключення до бази даних SQLite."""
    if connection:
        connection.close()


def create_tables():
    """Створює необхідні таблиці, якщо вони не існують."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skins (
                character_name TEXT PRIMARY KEY,
                last_date TEXT,
                skin_name TEXT
            )
        ''')

        conn.commit()
        logger.info("Таблиці 'admins' та 'skins' успішно створено (або вже існували).")

    except sqlite3.Error as e:
        logger.error(f"Помилка при створенні таблиць: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            close_connection(conn)


def add_admin(user_id: int):
    """Додає нового адміністратора до бази даних."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"Помилка при додаванні адміністратора: {e}")
        if conn:
            conn.rollback()
        return False  # Адміністратор вже існує
    finally:
        if conn:
            close_connection(conn)


def get_admins_from_db():
    """Отримує список всіх адміністраторів з бази даних."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM admins")
        admins = [row[0] for row in cursor.fetchall()]
        return admins
    except sqlite3.Error as e:
        logger.error(f"Помилка при отриманні адміністраторів: {e}")
        return []
    finally:
        if conn:
            close_connection(conn)


def add_skin(character_name: str, last_date: str, skin_name: str):
    """Додає інформацію про нового бравлера та його скін до бази даних."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO skins (character_name, last_date, skin_name) VALUES (?, ?, ?)",
                       (character_name, last_date, skin_name))
        conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"Помилка при додаванні скіна: {e}")
        if conn:
            conn.rollback()
        return False  # Бравлер вже існує
    finally:
        if conn:
            close_connection(conn)


def update_skin(character_name: str, last_date: str, skin_name: str):
    """Оновлює інформацію про останній скін бравлера."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE skins SET last_date=?, skin_name=? WHERE character_name=?",
                       (last_date, skin_name, character_name))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Помилка при оновленні скіна: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            close_connection(conn)


def get_skin(character_name: str):
    """Отримує інформацію про скін конкретного бравлера."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT last_date, skin_name FROM skins WHERE character_name=?", (character_name,))
        result = cursor.fetchone()
        if result:
            return result[0], result[1]  # Повертаємо кортеж
        return None
    except sqlite3.Error as e:
        logger.error(f"Помилка при отриманні скіна: {e}")
        return None
    finally:
        if conn:
            close_connection(conn)


def get_all_skins():
    """Отримує інформацію про всі скіни з бази даних."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT character_name, last_date, skin_name FROM skins")
        return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Помилка при отриманні всіх скінів: {e}")
        return []
    finally:
        if conn:
            close_connection(conn)


create_tables()  # Викликаємо створення таблиць при імпорті

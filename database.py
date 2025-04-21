from urllib.parse import urlparse

import psycopg2

from config.config import DATABASE_URL


def get_connection():
    """Повертає об'єкт підключення до бази даних PostgreSQL."""
    if not DATABASE_URL:
        raise ValueError("Змінна конфігурації DATABASE_URL не встановлена.")
    parsed_url = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        host=parsed_url.hostname,
        port=parsed_url.port,
        user=parsed_url.username,
        password=parsed_url.password,
        database=parsed_url.path[1:]
    )
    return conn


def close_connection(connection):
    """Закриває підключення до бази даних."""
    if connection:
        connection.close()


def create_tables():
    """Створює необхідні таблиці, якщо вони не існують."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            user_id BIGINT PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skins (
            character_name TEXT PRIMARY KEY,
            last_date DATE,
            skin_name TEXT
        )
    ''')

    conn.commit()
    close_connection(conn)


def add_admin(user_id: int):
    """Додає нового адміністратора до бази даних."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO admins (user_id) VALUES (%s)", (user_id,))
        conn.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False  # Адміністратор вже існує
    finally:
        close_connection(conn)


def get_admins_from_db():
    """Отримує список всіх адміністраторів з бази даних."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM admins")
    admins = [row[0] for row in cursor.fetchall()]
    close_connection(conn)
    return admins


def add_skin(character_name: str, last_date: str, skin_name: str):
    """Додає інформацію про нового бравлера та його скін до бази даних."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO skins (character_name, last_date, skin_name) VALUES (%s, %s, %s)",
                       (character_name, last_date, skin_name))
        conn.commit()
        return True
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False  # Бравлер вже існує
    finally:
        close_connection(conn)


def update_skin(character_name: str, last_date: str, skin_name: str):
    """Оновлює інформацію про останній скін бравлера."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE skins SET last_date=%s, skin_name=%s WHERE character_name=%s",
                   (last_date, skin_name, character_name))
    conn.commit()
    close_connection(conn)


def get_skin(character_name: str):
    """Отримує інформацію про скін конкретного бравлера."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT last_date, skin_name FROM skins WHERE character_name=%s", (character_name,))
    result = cursor.fetchone()
    close_connection(conn)
    return result


def get_all_skins():
    """Отримує інформацію про всіх бравлерів та їхні скіни."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT character_name, last_date, skin_name FROM skins")
    skins = cursor.fetchall()
    close_connection(conn)
    return skins


def delete_skin(character_name: str):
    """Видаляє інформацію про бравлера з бази даних."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skins WHERE character_name=%s", (character_name,))
    conn.commit()
    close_connection(conn)


# Виклик для створення таблиць при першому запуску бота
create_tables()

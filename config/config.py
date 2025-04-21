import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN_BOT = os.getenv('TELEGRAM_TOKEN_BOT')
SKINS_FILE = "Skins.txt"  # Цей рядок більше не потрібен, якщо ви повністю перейшли на PostgreSQL
ADMIN_ID = os.getenv('ADMIN_ID')
DATABASE_URL = os.getenv('DATABASE_URL')  # Не працює

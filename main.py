import inspect
import logging

from telegram.ext import ApplicationBuilder

import handlers
from config.config import TELEGRAM_TOKEN_BOT
from database import create_tables  # Імпортуємо функцію

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    create_tables()  # Явно викликаємо створення таблиць

    app = ApplicationBuilder().token(TELEGRAM_TOKEN_BOT).build()

    for name, obj in inspect.getmembers(handlers):
        if inspect.isclass(obj) and issubclass(obj, handlers.BaseHandler):
            obj.register(app)

    app.run_polling()

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from handlers.base_handler import BaseHandler


class StartHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("start", StartHandler.handle))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Привет! Я бот для отслеживания последней даты выхода скинов. Используйте команды:\n\n"
            "/add <имя_персонажа> <дата (ГГГГ-ММ-ДД)> — добавить персонажа\n"
            "/list — показать всех персонажей\n"
            "/update <имя_персонажа> <новая_дата> — обновить дату последнего скина"
        )

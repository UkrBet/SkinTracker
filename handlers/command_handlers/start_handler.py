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
            "Привет! Я бот для отслеживания последней даты выхода скинов.\n\n"

            "Команды для смертных:\n"
            "/list — посмотреть всех бравлеров\n"
            "/list name — посмотреть всех бравлеров в алфавитном порядке\n"
            "/list new — посмотреть самый новый скин (Недавно вышел скин)\n"
            "/list old — посмотреть самый старый скин (Давно не выходил скин)\n"
            "/list <количество рядков> — посмотреть нужное количество бравлеров\n"
            "/view <имя_бравлера> — посмотреть последний скин на нужного бравлера\n\n"

            "Команды для всевышних:\n"
            "/add <имя_бравлера>, <дата (ГГГГ-ММ-ДД), <название_скина> — добавить бравлера\n"
            "Используй 'today' или 'сегодня', чтобы установить текущую дату.\n"
            "/upd <имя_бравлера>, <дата (ГГГГ-ММ-ДД), <название_скина> — обновить дату последнего скина\n\n"
            
            "Все аргументы должны быть разделены запятыми!\n"
        )

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
            "Привет! Я бот для отслеживания последней даты выхода скинов. Используй команды:\n\n\n"
            "/add <имя_персонажа>, <дата (ГГГГ-ММ-ДД) | today/сегодня>, <название_скина> — добавить персонажа\n"
            "Используй 'today' или 'сегодня', чтобы установить текущую дату.\n\n"

            "/list — посмотреть всех персонажей\n"
            "/list name — посмотреть всех персонажей в алфавитном порядке\n"
            "/list new — посмотреть самый новый скин (Недавно вышел скин)\n"
            "/list old — посмотреть самый старый скин (Давно не выходил скин)\n\n"

            "/upd <имя_персонажа>, <дата (ГГГГ-ММ-ДД) | today/сегодня>, <название_скина> — обновить дату последнего скина\n"
            "Используй 'today' или 'сегодня', чтобы установить текущую дату.\n\n"

            "Все аргументы должны быть разделены запятыми!\n"
        )

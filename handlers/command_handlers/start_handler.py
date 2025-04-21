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
            "Привет! Я бот для отслеживания последней даты выхода скинов в игре Brawl Stars.\n"
            "Информация о скинах не обновлялась с момента 35-го сезона 'Good Randoms'. (Если что пишите мне в лс)\n\n"

            "**Что вы можете делать:**\n"
            "/list — посмотреть всех бравлеров\n"
            "/list name — посмотреть всех бравлеров в алфавитном порядке\n"
            "/list new — посмотреть самый недавно вышедший скин\n"
            "/list old — посмотреть самый давно вышедший скин\n"
            "/list <количество рядков> — посмотреть нужное количество бравлеров\n"
            "/view <имя_бравлера> — посмотреть последний скин на нужного бравлера\n\n"

            "**Команды для администраторов (если у вас есть права):**\n"
            "/add <имя_бравлера>, <дата (ГГГГ-ММ-ДД)>, <название_скина> - Добавить нового бравлера или информацию о его первом скине.\n"
            "   Используйте 'today' или 'сегодня', чтобы установить текущую дату выхода скина.\n"
            "/upd <имя_бравлера>, <дата (ГГГГ-ММ-ДД)>, <название_скина> - Обновить дату выхода и название последнего скина для существующего бравлера.\n\n"

            "**Важно:** Все аргументы в командах /add и /upd должны быть разделены запятой (,).\n"
            "Пример: /add Леон, 2023-10-27, Акула Леон\n"
        )

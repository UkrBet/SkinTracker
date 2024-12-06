from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config.config import SKINS_FILE
from handlers.base_handler import BaseHandler


class ViewAllSkinsHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("list", ViewAllSkinsHandler.handle))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            args = context.args

            with open(SKINS_FILE, "r", encoding="utf-8") as file:
                lines = file.readlines()

            if not lines:
                await update.message.reply_text("Список персонажей пуст.")
                return

            skins = []
            for line in lines:
                name, date, skin_name = line.strip().split(",", 2)
                days_passed = (datetime.now() - datetime.strptime(date, "%Y-%m-%d")).days
                skins.append((name, skin_name, date, days_passed))

            sort_description = "по порядку из файла"
            if args:
                sort_option = args[0].lower()
                if sort_option == "name":
                    skins.sort(key=lambda x: x[0])
                    sort_description = "в алфавитном порядке"
                elif sort_option == "new":
                    skins.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"), reverse=True)
                    sort_description = "по самым новым (Недавно вышел скин)"
                elif sort_option == "old":
                    skins.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d"))
                    sort_description = "по самым старым (Долго не было скина)"
                else:
                    raise ValueError("Некорректный параметр сортировки.")

            header = f"Список персонажей ({len(skins)}):\nСортировка {sort_description}.\n\n"

            response = header + "\n".join(
                [f"{i + 1}. {name}: {date} ({skin_name}) (прошло {days} дней)" for i, (name, date, skin_name, days) in
                 enumerate(skins)]
            )
            await update.message.reply_text(response)
        except ValueError:
            await update.message.reply_text(
                "Используйте команду в формате: /list [name|new|old]\n"
                "- name: сортировка по имени\n"
                "- new: сортировка по новым датам\n"
                "- old: сортировка по старым датам"
            )

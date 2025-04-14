from datetime import datetime
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config.config import SKINS_FILE
from handlers.base_handler import BaseHandler


class ViewSingleSkinHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("view", ViewSingleSkinHandler.handle))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            args = context.args
            if not args or len(args) != 1:
                await update.message.reply_text(
                    "Укажите имя бравлера в формате: /view <имя_бравлера>"
                )
                return

            character_name = args[0].strip()

            # Читання файлу з персонажами
            with open(SKINS_FILE, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Пошук персонажа
            for line in lines:
                try:
                    name, date, skin_name = line.strip().split(",")
                    if name.lower() == character_name.lower():
                        days_passed = (datetime.now() - datetime.strptime(date, "%Y-%m-%d")).days
                        await update.message.reply_text(
                            f"Бравлер: {name}\n"
                            f"Последний скин: {skin_name}\n"
                            f"Дата: {date} (прошло {days_passed} дней)"
                        )
                        return
                except ValueError:
                    continue

            await update.message.reply_text(f"Бравлер '{character_name}' не найден.")
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {str(e)}")

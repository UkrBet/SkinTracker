from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database import get_skin
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
                    "Вкажіть ім'я бравлера у форматі: /view <ім'я_бравлера>"
                )
                return

            character_name = args[0].strip()
            skin_data = get_skin(character_name)

            if skin_data:
                last_date_str, skin_name = skin_data
                try:
                    days_passed = (datetime.now() - datetime.strptime(last_date_str, "%Y-%m-%d")).days
                    await update.message.reply_text(
                        f"Бравлер: {character_name}\n"
                        f"Останній скін: {skin_name}\n"
                        f"Дата: {last_date_str} (пройшло {days_passed} днів)"
                    )
                except ValueError:
                    await update.message.reply_text(
                        f"Бравлер: {character_name}\n"
                        f"Останній скін: {skin_name}\n"
                        f"Дата: {last_date_str} (некоректний формат)"
                    )
            else:
                await update.message.reply_text(f"Бравлер '{character_name}' не знайдений.")

        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {str(e)}")

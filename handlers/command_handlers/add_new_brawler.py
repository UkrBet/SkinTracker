from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config.config import SKINS_FILE
from handlers.base_handler import BaseHandler

MY_USER_ID = 646771905


class AddNewBrawlerHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("add", AddNewBrawlerHandler.handle))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.from_user.id != MY_USER_ID:
            await update.message.reply_text(
                "Ты не имеешь доступа к этому боту. Ты можешь только смотреть список по команде /list [name|new|old]")
            return

        try:
            args = context.args
            if len(args) < 1 or len(args) > 2:
                raise ValueError

            character_name = args[0]

            if len(args) == 2:
                last_date = args[1]
            else:
                last_date = datetime.now().strftime("%Y-%m-%d")

            with open(SKINS_FILE, "a", encoding="utf-8") as file:
                file.write(f"{character_name},{last_date}\n")

            await update.message.reply_text(
                f"Добавлен новый персонаж: {character_name} с датой {last_date}."
            )
        except ValueError:
            await update.message.reply_text(
                "Используйте формат команды: /add <имя_персонажа> [дата (ГГГГ-ММ-ДД)]"
            )

from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config.config import SKINS_FILE
from handlers.base_handler import BaseHandler

MY_USER_ID = 646771905


class UpdateLastSkinHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("update", UpdateLastSkinHandler.handle))

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
                new_date = args[1]
            else:
                new_date = datetime.now().strftime("%Y-%m-%d")

            updated = False
            with open(SKINS_FILE, "r", encoding="utf-8") as file:
                lines = file.readlines()

            with open(SKINS_FILE, "w", encoding="utf-8") as file:
                for line in lines:
                    name, date = line.strip().split(",")
                    if name == character_name:
                        file.write(f"{name},{new_date}\n")
                        updated = True
                    else:
                        file.write(line)

            if updated:
                await update.message.reply_text(
                    f"Дата последнего скина для {character_name} обновлена на {new_date}."
                )
            else:
                await update.message.reply_text(
                    f"Персонаж {character_name} не найден в базе данных."
                )
        except ValueError:
            await update.message.reply_text(
                "Используйте формат команды: /update <имя_персонажа> [дата (ГГГГ-ММ-ДД)]"
            )

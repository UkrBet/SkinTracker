from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config.config import SKINS_FILE
from handlers.base_handler import BaseHandler

MY_USER_ID = 646771905


class UpdateLastSkinHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("upd", UpdateLastSkinHandler.handle))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.from_user.id != MY_USER_ID:
            await update.message.reply_text(
                "Ты не имеешь доступа к этому боту так как ты смертный. Напиши /start чтобы узнать что могут смертные"
            )
            return

        try:
            args = context.args

            if len(args) < 1:
                raise ValueError

            input_data = " ".join(args)
            parts = input_data.split(",")

            if len(parts) < 2:
                raise ValueError

            character_name = parts[0].strip()
            date_input = parts[1].strip()
            skin_name = parts[2].strip() if len(parts) > 2 else "Без названия"

            if date_input.lower() in ["today", "сегодня"]:
                new_date = datetime.now().strftime("%Y-%m-%d")
            else:
                try:
                    new_date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    await update.message.reply_text(
                        "Некорректный формат даты. Используйте формат: ГГГГ-ММ-ДД")
                    return

            updated = False
            with open(SKINS_FILE, "r", encoding="utf-8") as file:
                lines = file.readlines()

            with open(SKINS_FILE, "w", encoding="utf-8") as file:
                for line in lines:
                    name, date, skin = line.strip().split(",", 2)
                    if name == character_name:
                        file.write(f"{name},{new_date},{skin_name}\n")
                        updated = True
                    else:
                        file.write(line)

            if updated:
                await update.message.reply_text(
                    f"Дата последнего скина для {character_name} обновлена на {new_date} с новым скином: {skin_name}.")
            else:
                await update.message.reply_text(f"Бравлер {character_name} не найден в базе данных.")
        except ValueError:
            await update.message.reply_text(
                "Используйте формат команды: "
                "/update <имя_бравлера>, <дата (ГГГГ-ММ-ДД), <название_скина>"
                "\nВсе аргументы должны быть разделены запятыми!"
            )

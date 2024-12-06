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
                "Ты не имеешь доступа к этому боту. Ты можешь только смотреть список по команде /list [name|new|old]."
            )
            return

        try:
            # Получаем все аргументы команды
            args = context.args
            if len(args) < 1 or len(args) > 3:
                raise ValueError

            # Объединяем все аргументы в один строковый ввод и разбиваем по запятой
            input_data = " ".join(args)
            parts = input_data.split(",")  # Разделяем по запятой

            # Проверка на минимум два элемента
            if len(parts) < 2:
                raise ValueError

            # Убираем пробелы в начале и в конце
            character_name = parts[0].strip()
            last_date = parts[1].strip() if len(parts) > 1 else "today"
            skin_name = parts[2].strip() if len(parts) > 2 else "Без названия"

            # Проверка на корректность даты
            if last_date.lower() in ["today", "сегодня"]:
                last_date = datetime.now().strftime("%Y-%m-%d")

            # Открываем файл и добавляем персонажа
            with open(SKINS_FILE, "a", encoding="utf-8") as file:
                file.write(f"{character_name},{last_date},{skin_name}\n")

            await update.message.reply_text(
                f"Добавлен новый бравлер: {character_name} с датой {last_date}. Скин: {skin_name}."
            )
        except ValueError:
            await update.message.reply_text(
                "Используйте формат команды: "
                "/add <имя_бравлера>, <дата (ГГГГ-ММ-ДД) | today/сегодня>, <название_скина>"
                "\nВсе аргументы должны быть разделены запятыми!"
            )

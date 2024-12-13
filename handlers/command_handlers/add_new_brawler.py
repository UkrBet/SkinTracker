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
                "Ты не имеешь доступа к этому боту так как ты смертный. Напиши /start чтобы узнать что могут смертные"
            )
            return

        try:
            # Получаем все аргументы команды
            args = context.args
            print(f"Получены аргументы: {args}")  # Логирование аргументов

            # Проверяем, что аргументы переданы
            if not args:
                raise ValueError("Аргументы команды отсутствуют.")

            # Объединяем аргументы в одну строку и разбиваем по запятой
            input_data = " ".join(args)
            print(f"Объединенные данные: {input_data}")  # Логирование объединенных данных
            parts = [part.strip() for part in input_data.split(",")]

            # Проверка количества частей
            if len(parts) < 2:
                print(f"Неверное количество частей после разделения: {parts}")  # Логирование частей
                raise ValueError("Неверный формат команды.")

            # Убираем пробелы в начале и в конце
            character_name = parts[0]
            last_date = parts[1] if len(parts) > 1 else "today"
            skin_name = parts[2] if len(parts) > 2 else "Без названия"

            print(f"Имя: {character_name}, Дата: {last_date}, Скин: {skin_name}")  # Логирование переменных

            # Проверка и преобразование даты
            if last_date.lower() in ["today", "сегодня"]:
                last_date = datetime.now().strftime("%Y-%m-%d")
            else:
                try:
                    datetime.strptime(last_date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Неверный формат даты. Используйте ГГГГ-ММ-ДД.")

            # Открываем файл и добавляем персонажа
            with open(SKINS_FILE, "a", encoding="utf-8") as file:
                file.write(f"{character_name},{last_date},{skin_name}\n")

            await update.message.reply_text(
                f"Добавлен новый бравлер: {character_name} с датой {last_date}. Скин: {skin_name}."
            )
        except ValueError as ve:
            print(f"Ошибка значения: {ve}")  # Логирование ошибки
            await update.message.reply_text(
                "Используйте формат команды: \n"
                "/add <имя_бравлера>, <дата (ГГГГ-ММ-ДД), <название_скина>\n"
                "Все аргументы должны быть разделены запятыми!"
            )
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")  # Логирование ошибок
            await update.message.reply_text(f"Произошла ошибка: {e}")

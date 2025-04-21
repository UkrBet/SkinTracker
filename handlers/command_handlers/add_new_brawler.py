from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database import add_skin
from handlers.base_handler import BaseHandler


class AddNewBrawlerHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("add", AddNewBrawlerHandler.handle))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not BaseHandler.is_admin(update.effective_user.id):
            await update.message.reply_text(
                "Ти не маєш доступу до цього боту так як ти смертний - твої можливості обмежені.\n"
                "Напиши /start щоб дізнатися що можуть смертні"
            )
            return

        try:
            args = context.args
            if not args:
                raise ValueError("Аргументи команди відсутні.")

            input_data = " ".join(args)
            parts = [part.strip() for part in input_data.split(",")]

            if len(parts) < 2:
                raise ValueError("Невірний формат команди.")

            character_name = parts[0]
            last_date_str = parts[1]
            skin_name = parts[2] if len(parts) > 2 else "Без назви"

            if last_date_str.lower() in ["today", "сегодня"]:
                last_date = datetime.now().strftime("%Y-%m-%d")
            else:
                try:
                    datetime.strptime(last_date_str, "%Y-%m-%d")
                    last_date = last_date_str
                except ValueError:
                    raise ValueError("Невірний формат дати. Використовуйте РРРР-ММ-ДД.")

            if add_skin(character_name, last_date, skin_name):
                await update.message.reply_text(
                    f"Додано нового бравлера: {character_name} з датою {last_date}. Скін: {skin_name}."
                )
            else:
                await update.message.reply_text(f"Бравлер {character_name} вже існує.")

        except ValueError as ve:
            await update.message.reply_text(
                "Використовуйте формат команди: \n"
                "/add <ім'я_бравлера>, <дата (РРРР-ММ-ДД)>, <назва_скіна>\n"
                "Всі аргументи повинні бути розділені комами!"
            )
        except Exception as e:
            print(f"Невідома помилка: {e}")
            await update.message.reply_text(f"Произошла ошибка: {e}")

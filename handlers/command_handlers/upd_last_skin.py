from datetime import datetime

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database import update_skin, get_skin
from handlers.base_handler import BaseHandler


class UpdateLastSkinHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("upd", UpdateLastSkinHandler.handle))

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
            if len(args) < 1:
                raise ValueError

            input_data = " ".join(args)
            parts = [part.strip() for part in input_data.split(",")]

            if len(parts) < 2:
                raise ValueError

            character_name = parts[0]
            date_input = parts[1]
            skin_name = parts[2] if len(parts) > 2 else "Без назви"

            if date_input.lower() in ["today", "сегодня"]:
                new_date = datetime.now().strftime("%Y-%m-%d")
            else:
                try:
                    datetime.strptime(date_input, "%Y-%m-%d")
                    new_date = date_input
                except ValueError:
                    await update.message.reply_text(
                        "Некоректний формат дати. Використовуйте формат: РРРР-ММ-ДД")
                    return

            existing_skin_data = get_skin(character_name)
            if existing_skin_data:
                update_skin(character_name, new_date, skin_name)
                await update.message.reply_text(
                    f"Дата останнього скіна для {character_name} оновлена на {new_date}. Скін: {skin_name}.")
            else:
                await update.message.reply_text(f"Бравлер {character_name} не знайдений в базі даних.")

        except ValueError:
            await update.message.reply_text(
                "Використовуйте формат команди: "
                "/upd <ім'я_бравлера>, <дата (РРРР-ММ-ДД)>, <назва_скіна>"
                "\nВсі аргументи повинні бути розділені комами!"
            )
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {e}")

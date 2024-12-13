from datetime import datetime
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config.config import SKINS_FILE
from handlers.base_handler import BaseHandler


class ListSkinsHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("list", ListSkinsHandler.handle))

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
                parts = line.strip().split(",", 2)
                if len(parts) == 3:
                    name, date, skin_name = parts
                    try:
                        days_passed = (datetime.now() - datetime.strptime(date, "%Y-%m-%d")).days
                    except ValueError:
                        days_passed = "Некорректная дата"
                    skins.append((name, skin_name, date, days_passed))

            sort_description = "по порядку из файла"

            # Обработка параметров сортировки и количества
            count = None
            if args:
                if args[0].isdigit():
                    count = int(args[0])
                else:
                    sort_option = args[0].lower()

                    if sort_option == "name":
                        skins.sort(key=lambda x: x[0])
                        sort_description = "в алфавитном порядке"
                    elif sort_option == "new":
                        skins.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"), reverse=True)
                        sort_description = "по самым новым (Недавно вышел скин)"
                    elif sort_option == "old":
                        skins.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"))
                        sort_description = "по самым старым (Долго не было скина)"
                    else:
                        raise ValueError("Некорректный параметр сортировки.")

                    # Проверка на количество строк
                    if len(args) > 1 and args[1].isdigit():
                        count = int(args[1])
                    elif len(args) > 1:
                        await update.message.reply_text("Укажите корректное количество строк.")
                        return
            # Обрезка до указанного количества строк
            if count is not None:
                skins = skins[:count]

            header = f"Список персонажей ({len(skins)}):\nСортировка {sort_description}.\n\n"

            response = header + "\n".join(
                [f"{i + 1}. {name}: {skin_name} ({date}) (прошло {days} дней)"
                 for i, (name, skin_name, date, days) in enumerate(skins)]
            )

            footer = "\n\nКонец списка."
            response += footer

            await update.message.reply_text(response)

        except ValueError:
            await update.message.reply_text(
                "Используйте команду в формате: /list [name|new|old] [количество]\n"
                "- name: сортировка по имени\n"
                "- new: сортировка по новым датам\n"
                "- old: сортировка по старым датам\n"
                "Можно также указать только количество строк, например: /list 5"
            )
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            await update.message.reply_text(f"Произошла ошибка: {e}")

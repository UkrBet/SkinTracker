from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler

from database import get_all_skins
from handlers.base_handler import BaseHandler

ITEMS_PER_PAGE = 10


class ListSkinsHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("list", ListSkinsHandler.handle))
        app.add_handler(CallbackQueryHandler(ListSkinsHandler.handle_page, pattern=r'^list_page_(\d+)$'))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        skins_data_tuples = get_all_skins()
        skins_data = []
        for name, date_str, skin_name in skins_data_tuples:
            try:
                days_passed = (datetime.now() - datetime.strptime(date_str, "%Y-%m-%d")).days
            except ValueError:
                days_passed = "Некоректна дата"
            skins_data.append((name, skin_name, date_str, days_passed))

        sort_description = "за порядком з бази даних"

        args = context.args
        if args:
            sort_option = args[0].lower()
            if sort_option == "name":
                skins_data.sort(key=lambda x: x[0])
                sort_description = "в алфавітному порядку"
            elif sort_option == "new":
                skins_data.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"), reverse=True)
                sort_description = "по найновішим (Нещодавно вийшов скін)"
            elif sort_option == "old":
                skins_data.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"))
                sort_description = "по найстарішим (Давно не було скіна)"
            elif args[0].isdigit():
                pass  # Кількість елементів буде оброблена пізніше
            else:
                await update.message.reply_text("Некоректний параметр сортування.")
                return

        context.user_data['all_skins'] = skins_data
        context.user_data['sort_description'] = sort_description

        await ListSkinsHandler.show_page(update, context, page=0)

    @staticmethod
    async def show_page(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int):
        skins_data = context.user_data.get('all_skins')
        sort_description = context.user_data.get('sort_description', "за порядком з бази даних")

        if not skins_data:
            await update.message.reply_text("Список персонажів пустий.")
            return

        start_index = page * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        current_page_skins = skins_data[start_index:end_index]

        if not current_page_skins:
            if page > 0:
                await ListSkinsHandler.show_page(update, context, page - 1)
            else:
                await update.message.reply_text("Список персонажів пустий.")
            return

        response_lines = [
            f"{i + 1 + start_index}. {name}: {skin_name} ({date}) (пройшло {days} днів)"
            for i, (name, skin_name, date, days) in enumerate(current_page_skins)
        ]

        header = f"Список персонажів ({len(skins_data)}):\nСортування {sort_description}.\n\n"
        response = header + "\n".join(response_lines)

        keyboard = []
        if page > 0:
            keyboard.append(InlineKeyboardButton("⬅️ Назад", callback_data=f'list_page_{page - 1}'))
        if end_index < len(skins_data):
            keyboard.append(InlineKeyboardButton("➡️ Вперед", callback_data=f'list_page_{page + 1}'))

        if keyboard:
            reply_markup = InlineKeyboardMarkup([keyboard])
        else:
            reply_markup = None

        if update.callback_query:
            await update.callback_query.edit_message_text(text=response, reply_markup=reply_markup)
        else:
            await update.message.reply_text(text=response, reply_markup=reply_markup)

    @staticmethod
    async def handle_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        page = int(query.data.split('_')[-1])
        await ListSkinsHandler.show_page(update, context, page)

import os

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config.config import ADMIN_ID
from handlers.base_handler import BaseHandler

ADMIN_LIST_FILE = "Admin_ids.txt"


def load_additional_admins():
    if not os.path.exists(ADMIN_LIST_FILE):
        return set()
    with open(ADMIN_LIST_FILE, "r") as f:
        return set(map(int, f.read().splitlines()))


def save_additional_admins(admins):
    with open(ADMIN_LIST_FILE, "w") as f:
        for admin_id in admins:
            f.write(f"{admin_id}\n")


def is_admin(user_id):
    return user_id == int(ADMIN_ID) or user_id in load_additional_admins()


class AddAdminHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("addadmin", AddAdminHandler.handle))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        if user_id != int(ADMIN_ID):
            await update.message.reply_text("У вас немає прав додавати адмінів.")
            return

        if not context.args or not context.args[0].isdigit():
            await update.message.reply_text(
                "Вкажіть ID користувача, якого потрібно зробити адміном.\nПриклад: /addadmin 123456789")
            return

        new_admin_id = int(context.args[0])
        admins = load_additional_admins()

        if new_admin_id in admins:
            await update.message.reply_text(f"Користувач {new_admin_id} вже є у списку адмінів.")
            return

        admins.add(new_admin_id)
        save_additional_admins(admins)

        await update.message.reply_text(f"Користувача з ID {new_admin_id} додано до адмінів.")

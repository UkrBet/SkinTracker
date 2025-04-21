from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from database import add_admin, get_admins_from_db
from handlers.base_handler import BaseHandler


class AddAdminHandler(BaseHandler):
    @staticmethod
    def register(app):
        app.add_handler(CommandHandler("addadmin", AddAdminHandler.handle))

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        if not BaseHandler.is_admin(user_id):  # Використовуємо метод з BaseHandler
            await update.message.reply_text("У вас немає прав додавати адмінів.")
            return

        if not context.args or not context.args[0].isdigit():
            await update.message.reply_text(
                "Вкажіть ID користувача, якого потрібно зробити адміном.\nПриклад: /addadmin 123456789")
            return

        new_admin_id = int(context.args[0])

        if add_admin(new_admin_id):
            await update.message.reply_text(f"Користувача з ID {new_admin_id} додано до адмінів.")
        else:
            await update.message.reply_text(f"Користувач {new_admin_id} вже є у списку адмінів.")

    @staticmethod
    def get_admins() -> list:
        # Отримуємо адміністраторів з бази даних та додаємо головного адміна з config
        from config.config import ADMIN_ID
        admins_from_db = get_admins_from_db()
        admins_from_db.append(int(ADMIN_ID))
        return list(set(admins_from_db))

    @staticmethod
    def is_admin(user_id: int) -> bool:
        from config.config import ADMIN_ID
        admins_from_db = get_admins_from_db()
        return user_id == int(ADMIN_ID) or user_id in admins_from_db

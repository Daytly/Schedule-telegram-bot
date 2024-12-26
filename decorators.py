from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from database import SessionLocal
from models import Admin


async def check_is_admin(effective_user):
    with SessionLocal() as session:
        admin = session.query(Admin).filter_by(user_id=effective_user.id).first()
        if not admin:
            return False
    return True


def its_admin_command(function_to_decorate):
    async def check_admin(update: Update, context: CallbackContext):
        if await check_is_admin(update.effective_user):
            return await function_to_decorate(update, context)
        else:
            sent_message = "Доступ закрыт"
            await update.message.reply_text(sent_message)
            return ConversationHandler.END

    return check_admin

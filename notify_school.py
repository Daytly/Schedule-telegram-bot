from telegram import Update
from telegram.ext import CallbackContext

from database import SessionLocal
from decorators import its_admin_command
from logger import logger
from models import User


@its_admin_command
async def notify_all(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Используйте команду /notify_all <сообщение>")
        return

    message = ' '.join(context.args)

    with SessionLocal() as session:
        users = session.query(User).all()
        for user in users:
            try:
                await context.bot.send_message(chat_id=user.user_id, text=message)
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение пользователю {user.user_id}: {e}")

    await update.message.reply_text("Сообщение успешно отправлено всем пользователям.")


@its_admin_command
async def notify_class(update: Update, context: CallbackContext) -> None:
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Используйте команду /notify_class <класс> <сообщение>")
        return

    class_name = context.args[0].upper()
    message = ' '.join(context.args[1:])

    with SessionLocal() as session:
        users = session.query(User).filter_by(class_name=class_name).all()
        for user in users:
            try:
                await context.bot.send_message(chat_id=user.user_id, text=message)
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение пользователю {user.user_id}: {e}")

    await update.message.reply_text(f"Сообщение успешно отправлено пользователям класса {class_name}.")

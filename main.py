from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, Application, filters, CommandHandler, MessageHandler
from bot_handlers import start, help_command, schedule_bells_handler, class_schedule_handler, change_class, \
    class_schedule_short_handler, about
from admin_commands import add_admin, change_schedule
from notify_school import notify_all, notify_class
from database import init_db, engine
from logger import logger
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

TOKEN = '7636937652:AAEBBTcIG-NPSo1ZNhboiWqUZ584JXKPANE'


async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(f"Вы написали: {update.message.text}")


async def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Инициализируем базу данных
    init_db(engine)

    application = Application.builder().token(TOKEN).read_timeout(30).write_timeout(30).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("schedule_bells", schedule_bells_handler))
    application.add_handler(CommandHandler("class_schedule", class_schedule_handler))
    application.add_handler(CommandHandler("change_class", change_class))
    application.add_handler(CommandHandler("schedule", class_schedule_short_handler))

    # Команды для администраторов
    application.add_handler(CommandHandler("add_admin", add_admin))
    application.add_handler(CommandHandler("change_schedule", change_schedule))
    application.add_handler(CommandHandler("notify_all", notify_all))
    application.add_handler(CommandHandler("notify_class", notify_class))

    # Регистрируем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Обработка ошибок
    application.add_error_handler(error)
    application.run_polling()
    logger.info("Bot started")


if __name__ == '__main__':
    main()

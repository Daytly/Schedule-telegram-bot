from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from database import SessionLocal
from models import User, ClassSchedule


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"

    # Сохраняем пользователя в базу данных, если он еще не сохранен
    with SessionLocal() as session:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            new_user = User(user_id=user_id, username=username)
            session.add(new_user)
            session.commit()
            await update.message.reply_text(
                f"Привет! Похоже ты тут в первый раз. Я бот для просмотра расписания в школе. "
                f"/change_class <класс>  - Установить свой класс (например, 7A)."
                f"А затем можешь список всех команд /help.")
        else:
            await update.message.reply_text(
                f"Снова привет! Я бот для просмотра расписания в школе. Для начала используйте команду /help.")


async def about(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Данный бот был создан для ИУП, учеником Лицея №129 Гороховым Ильёй")


async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/about - Информация о создателе\n"
        "/help - Получить помощь\n"
        "/schedule_bells - Просмотреть общее расписание звонков школы\n"
        "/class_schedule <класс> - Просмотреть расписание конкретного класса (например, 7A)\n"
        "/schedule <класс> - Просмотреть расписание своего класса\n"
        "/change_class <класс>  - Установить свой класс (например, 7A)"
    )
    await update.message.reply_text(help_text)


async def schedule_bells_handler(update: Update, context: CallbackContext) -> None:
    # Здесь можно добавить логику для получения и показа общего расписания школы
    general_schedule = (
        "Общее звонков школы:\n"
        "1:08:00 - 8:40 10 мин\n"
        "2:08:50 - 9:30 15 мин\n"
        "3:09:45 - 10:25 20 мин\n"
        "4:10:45 - 11:25 20 мин\n"
        "5:11:45 - 12:25 15 мин\n"
        "6:12:40 - 13:20 10 мин\n"
        "7:13:30 - 14:10\n"
    )
    await update.message.reply_text(general_schedule, parse_mode=ParseMode.MARKDOWN)


async def class_schedule_short_handler(update: Update, context: CallbackContext) -> None:
    with SessionLocal() as session:
        user = session.query(User).filter_by(user_id=update.effective_user.id).first()
        if not user:
            await update.message.reply_text("Сначала веди свой класс командой: /change_class <класс>")
            return
        schedule = session.query(ClassSchedule).filter_by(class_name=user.class_name).first()
        if schedule:
            with open(schedule.schedule, "r", encoding="utf-8") as f:
                stripper = '\n'
                await update.message.reply_text(f"Расписание:\n{stripper.join(f.readlines())}",
                                                parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(
                f"Расписание для класса {user.class_name} не найдено. Пожалуйста, убедитесь, что вы ввели правильное "
                f"название класса.")


async def class_schedule_handler(update: Update, context: CallbackContext) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Используйте команду /class_schedule <класс> (например, 7A)")
        return

    class_name = context.args[0].upper()

    with SessionLocal() as session:
        schedule = session.query(ClassSchedule).filter_by(class_name=class_name).first()
        if schedule:
            with open(schedule.schedule, "r", encoding="utf-8") as f:
                stripper = '\n'
                await update.message.reply_text(f"Расписание для класса {class_name}:\n{stripper.join(f.readlines())}",
                                                parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(
                f"Расписание для класса {class_name} не найдено. Пожалуйста, убедитесь, что вы ввели правильное "
                f"название класса.")


async def change_class(update: Update, context: CallbackContext) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Используйте команду /change_schedule <класс> (например, 7A)")
        return
    with SessionLocal() as session:
        user = session.query(User).filter_by(user_id=update.effective_user.id).first()
        if not user:
            await update.message.reply_text("Сначала веди свой класс командой: /change_class <класс>")
            return
        user.class_name = context.args[0].upper()
        session.merge(user)
        session.commit()
    await update.message.reply_text("Сохранено")


# Пример функции для обработки сообщений
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Вы написали: {update.message.text}")

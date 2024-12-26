from telegram import Update
from telegram.ext import CallbackContext

from database import SessionLocal
from decorators import its_admin_command
from models import User, Admin, ClassSchedule


@its_admin_command
async def add_admin(update: Update, context: CallbackContext) -> None:
    if not context.args or len(context.args) != 1:
        await update.message.reply_text("Используйте команду /add_admin <user_id>")
        return

    admin_user_id = int(context.args[0])

    with SessionLocal() as session:
        user = session.query(User).filter_by(user_id=admin_user_id).first()
        if not user:
            await update.message.reply_text(f"Пользователь с ID {admin_user_id} не найден в базе данных.")
            return

        admin = Admin(user_id=admin_user_id)
        session.add(admin)
        session.commit()

    await update.message.reply_text(f"Пользователь с ID {admin_user_id} добавлен в список администраторов.")


@its_admin_command
async def change_schedule(update: Update, context: CallbackContext) -> None:
    if not context.args or len(context.args) < 1:
        await update.message.reply_text("Используйте команду /change_schedule <класс> <расписание>")
        return

    class_name = context.args[0].upper()
    new_schedule = ' '.join(context.args[1:])
    with SessionLocal() as session:
        schedule = session.query(ClassSchedule).filter_by(class_name=class_name).first()
        if not schedule:
            new_class_schedule = ClassSchedule(class_name=class_name, schedule=new_schedule)
            session.add(new_class_schedule)
        else:
            schedule.schedule = new_schedule
        session.commit()

    await update.message.reply_text(f"Расписание для класса {class_name} успешно изменено.")

import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.chains.base.kb import start_kb
from bot.chains.get_report.kb import choose, cancel_kb
from bot.chains.get_report.state import ReportEvents
from bot.chains.record_event.state import RecordEvent
from bot.core import dp, bot
from db.config import BASE_DIR
from db.models.user import User
from presentation.presentation_creator import create_presentation
from db.models.events import Event


@dp.callback_query_handler(lambda x: x.data == "event_report_cancel", state="*")
async def cancel(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    await state.finish()
    await bot.send_message(
        c.from_user.id, "Скасовано створення звіту про захід", reply_markup=start_kb
    )
    await c.answer("Скасовано")


@dp.message_handler(regexp="Отримати звіт", state="*")
async def auth(msg: types.Message, state: FSMContext):
    await ReportEvents.wait_for_password.set()
    data_state = await msg.answer(
        "Напишіть пароль, який був наданий адміністратором.", reply_markup=cancel_kb
    )
    await state.update_data({"message": data_state})


@dp.message_handler(state=ReportEvents.wait_for_password)
async def report_event_choose(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await data.get("message").delete_reply_markup()
    check_password = await User.check_password(msg.text)
    if not check_password:
        await msg.answer("Друже, це невірний пароль.", reply_markup=cancel_kb)
    else:
        user_data = await User.user_data(msg.text)
        await state.update_data(
            {
                "username": user_data["name"],
                "faculty": user_data["faculty"],
                "user": user_data["id"],
            }
        )
        answer = await msg.answer(
            f'Привіт, {user_data["name"]}! {user_data["faculty"]} найкращий! \n\n'
            f"Хочеш, щоб я тобі згенерував звіт?",
            reply_markup=choose,
        )
        await RecordEvent.wait_event_name.set()
        await state.update_data({"message": answer})


@dp.callback_query_handler(lambda x: x.data == "event_report_approve", state="*")
async def generate_presentation(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    data = await state.get_data()
    events = await Event.query.where(User.id == data.get("user")).gino.all()
    create_presentation(
        [events[k].event_name for k in range(len(events))],
        [await events[j].photo for j in range(len(events))],
        data.get("faculty"),
    )
    pres_file = open(
        os.path.join(BASE_DIR, f'presentations/{data.get("faculty")}_report.pptx'), "rb"
    )
    await bot.send_message(
        c.from_user.id,
        "В тебе дуже круто виходить організовувати заходи! \n\n"
        "Тримай презентацію та приходь до мене ще ;)",
    )
    await bot.send_document(c.from_user.id, pres_file)
    await state.finish()

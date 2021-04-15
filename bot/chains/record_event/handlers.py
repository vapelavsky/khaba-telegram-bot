from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User as TgUser

from bot.chains.base.kb import start_kb
from bot.chains.record_event.kb import cancel_record
from bot.chains.record_event.state import RecordEvent
from bot.core import dp, bot
from db.models.users_events import User, Event, Photos


@dp.callback_query_handler(lambda x: x.data == 'event_record_cancel', state='*')
async def cancel(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    await state.finish()
    await bot.send_message(c.from_user.id, 'Скасовано створення звіту про захід', reply_markup=start_kb)
    await c.answer('Скасовано')


@dp.message_handler(regexp='Захід', state='*')
async def auth(msg: types.Message, state: FSMContext):
    await RecordEvent.wait_password.set()
    data_state = await msg.answer('Напишіть пароль, який був наданий адміністратором.', reply_markup=cancel_record)
    await state.update_data({'message': data_state})


@dp.message_handler(state=RecordEvent.wait_password)
async def record_event_start(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await data.get('message').delete_reply_markup()
    check_password = await User.check_password(msg.text)
    if not check_password:
        await msg.answer('Друже, це невірний пароль.', reply_markup=cancel_record)
    else:
        user_data = await User.user_data(msg.text)
        await state.update_data({'username': user_data["name"],
                                 'faculty': user_data["faculty"]})
        answer = await msg.answer(f'Привіт, {user_data["name"]}! {user_data["faculty"]} найкращий! \n\n'
                                  f'Поділися зі мною назвою заходу, який Ви провели :)', reply_markup=cancel_record)
        await RecordEvent.wait_event_name.set()
        await state.update_data({'message': answer})


@dp.message_handler(state=RecordEvent.wait_event_name)
async def record_event_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await data.get('message').delete_reply_markup()
    await msg.answer(f'{data.get("username")}, {data.get("faculty")}, {msg.text}.'
                     f'Це типу тестовий стенд, як виводяться дані, ага.', reply_markup=cancel_record)
    await RecordEvent.wait_event_photos.set()
    await state.update_data("event_name": msg.text)

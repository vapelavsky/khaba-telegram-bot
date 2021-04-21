from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.chains.base.kb import start_kb
from bot.chains.get_report.kb import choose, cancel_kb
from bot.chains.get_report.state import ReportEvents
from bot.chains.record_event.state import RecordEvent
from bot.core import dp, bot
from db.models.user import User
from presentation.generator import create_presentation
from db.models.events import Event
from db.models.photos import Photos


@dp.callback_query_handler(lambda x: x.data == 'event_report_cancel', state='*')
async def cancel(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    await state.finish()
    await bot.send_message(c.from_user.id, 'Скасовано створення звіту про захід', reply_markup=start_kb)
    await c.answer('Скасовано')


@dp.message_handler(regexp='Отримати звіт', state='*')
async def auth(msg: types.Message, state: FSMContext):
    await ReportEvents.wait_for_password.set()
    data_state = await msg.answer('Напишіть пароль, який був наданий адміністратором.', reply_markup=cancel_kb)
    await state.update_data({'message': data_state})


@dp.message_handler(state=ReportEvents.wait_for_password)
async def report_event_choose(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await data.get('message').delete_reply_markup()
    check_password = await User.check_password(msg.text)
    if not check_password:
        await msg.answer('Друже, це невірний пароль.', reply_markup=cancel_kb)
    else:
        user_data = await User.user_data(msg.text)
        await state.update_data({'username': user_data["name"],
                                 'faculty': user_data["faculty"],
                                 'user': user_data["id"]})
        answer = await msg.answer(f'Привіт, {user_data["name"]}! {user_data["faculty"]} найкращий! \n\n'
                                  f'Хочеш, щоб я тобі згенерував звіт?', reply_markup=choose)
        await RecordEvent.wait_event_name.set()
        await state.update_data({'message': answer})


@dp.callback_query_handler(lambda x: x.data == 'event_report_approve', state='*')
async def generate(c: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    events = await Event.query.where(User.id == data.get('user')).gino.all()
    image = await events[0].photo
    print(image)
    event_photos_proc = [await Photos.select('photo_path').where(Photos.parent_id == event_name[i]).gino.all()
                         for i in range(len(event_name))]
    event_photos = {f'{event_name[i]}': [str(event_photos_proc[i][k]).strip('\'(,)')
                                         for k in range(len(event_photos_proc[i]))]
                    for i in range(len(event_name))}
    print(event_photos)
    print(event_photos)
    print(len(event_photos.get('Іюнька')))
    print(event_photos.get('Іюнька'))
    for i in range(len(event_name)):
        create_presentation(event_name, event_photos.get(f'{event_name[i]}'), data.get('faculty'))

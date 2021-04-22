import hashlib
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User as TgUser

from bot.chains.admin_panel.kb import admin_start_kb, cancel_kb
from bot.chains.admin_panel.state import AdminPanel
from bot.config import ADMIN_CHAT_ID
from bot.core import dp, bot
from db import Event
from db.config import BASE_DIR
from db.models.user import User
from presentation.presentation_creator import create_presentation


@dp.callback_query_handler(lambda x: x.data == 'cancel_activity', state='*')
async def cancel(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    await state.finish()
    await bot.send_message(c.from_user.id, 'Скасовано', reply_markup=admin_start_kb)
    await c.answer('Скасовано')


@dp.message_handler(regexp='Залогінитися як адмін 😎', state='*')
async def admin_start(msg: types.Message, state: FSMContext):
    if TgUser.get_current().id != int(ADMIN_CHAT_ID):
        await msg.answer("Тобі сюди не можна, друже.")
    else:
        await msg.answer('Вітаю, мій господар! \n\n Скажи, що я можу для тебе зробити.', reply_markup=admin_start_kb)


@dp.callback_query_handler(lambda x: x.data == 'user_creation', state='*')
async def name_head(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    await AdminPanel.wait_name.set()
    answer = await bot.send_message(c.from_user.id, "Напиши ПІБ студентського декана, директора або ректора.",
                                    reply_markup=cancel_kb)
    await state.update_data({'message': answer})


@dp.message_handler(state=AdminPanel.wait_name)
async def faculty_head(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await data.get('message').delete_reply_markup()
    answer = await msg.answer(f"Напишіть факультет або інститут, головою ОСС якого є {msg.text}. \n\n"
                              f"Якщо це студентський ректор - просто напишіть 'Студректорат'",
                              reply_markup=cancel_kb)
    await state.update_data({'name': msg.text,
                             'message': answer})
    await AdminPanel.wait_faculty.set()


@dp.message_handler(state=AdminPanel.wait_faculty)
async def password_head(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await data.get('message').delete_reply_markup()
    answer = await msg.answer("Вигадайте пароль для користувача", reply_markup=cancel_kb)
    await state.update_data({'faculty': msg.text,
                             'message': answer})
    await AdminPanel.wait_password.set()


@dp.message_handler(state=AdminPanel.wait_password)
async def creating_user(msg: types.Message, state: FSMContext):
    await state.update_data({'password': msg.text})
    data = await state.get_data()
    await data.get('message').delete_reply_markup()
    await User.create(name=data.get('name'),
                      faculty=data.get('faculty'),
                      password=hashlib.md5(data.get('password').encode("utf-8")).hexdigest()
                      )
    await msg.answer("Молодець! Юзера створено. \n\n Може ще чимось допомогти?", reply_markup=admin_start_kb)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data == 'user_delete', state='*')
async def delete_user_start(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    await AdminPanel.wait_name_delete.set()
    answer = await bot.send_message(c.from_user.id, "Напиши ПІБ користувача, якого ти хочеш вилучити.",
                                    reply_markup=cancel_kb)
    await state.update_data({'message': answer})


@dp.message_handler(state=AdminPanel.wait_name_delete)
async def deleting(msg: types.Message, state: FSMContext):
    await state.update_data({'name': msg.text})
    data = await state.get_data()
    await data.get('message').delete_reply_markup()
    await User.delete.where(User.name == data.get('name')).gino.first()
    await msg.answer("Шкода, що ти видалив юзера. Напевно, так треба."
                     "\n\n Може ще чимось допомогти?", reply_markup=admin_start_kb)
    await state.finish()


@dp.callback_query_handler(lambda x: x.data == 'list_user', state='*')
async def get_list(c: types.CallbackQuery):
    users = await User.query.gino.all()
    message_pattern = [f'{users[i].id}. {users[i].name}, {users[i].faculty} \n' for i in range(len(users))]

    await bot.send_message(c.from_user.id, f'{"".join(message_pattern)}\n\n '
                                           f'Чи можу ще чимось допомогти?', reply_markup=admin_start_kb)

import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User as TgUser

from bot import files
from bot.chains.base.kb import start_kb
from bot.chains.create_event.kb import cancel_kb
from bot.chains.create_event.state import CreateEvent
from bot.config import ADMIN_CHAT_ID
from bot.core import dp, bot
from bot.tree import DocsPath

Docs = files.loadFile(DocsPath)


def mapping_json(nd, p):
    return Docs[0][nd][f'{p}']


def mapping_signs(nd):
    return Docs[0][nd.lower()]['significants']


@dp.callback_query_handler(lambda x: x.data == 'event_creation_cancel', state='*')
async def cancel(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    await state.finish()
    await bot.send_message(c.from_user.id, 'Скасовано', reply_markup=start_kb)
    await c.answer('Скасовано')


@dp.message_handler(regexp='Організувати захід 🎉', state='*')
async def create_event_start(msg: types.Message, state: FSMContext):
    await CreateEvent.wait_event.set()
    data_state = await msg.answer('Напишіть тип заходу, який ви хочете провести', reply_markup=cancel_kb)
    await state.update_data({'message': data_state})


@dp.message_handler(state=CreateEvent.wait_event)
async def list_event(msg: types.Message, state: FSMContext):
    data_state = await state.get_data()
    await data_state.get('message').delete_reply_markup()
    answer = await msg.answer('Напишіть списком, що вам потрібно для заходу.\n'
                              'Наприклад:\n'
                              '1. Кава-брейк\n'
                              '2. Аудиторія\n'
                              '3. Транспорт\n', reply_markup=cancel_kb)
    await CreateEvent.wait_list.set()
    await state.update_data({'message': answer})


@dp.message_handler(state=CreateEvent.wait_list)
async def list_event(msg: types.Message, state: FSMContext):
    data_state = await state.get_data()
    await data_state.get('message').delete_reply_markup()
    await state.update_data({'description': msg.text})
    need_docs = re.findall(r'\S+', msg.text)
    message_pattern = [f"<a href='{mapping_json(need_docs[i].lower(), 'link')}'>" \
                       f"{mapping_json(need_docs[i].lower(), 'name')}</a>\n" \
                       f"У кого підписати: {', '.join(mapping_signs(need_docs[i]))} \n"
                       for i in range(len(need_docs))]
    message = '\n'.join(message_pattern)
    answer = await msg.answer(f"Отже, для цього заходу тобі потрібно: \n\n"
                              f"{message}",
                              reply_markup=cancel_kb,
                              parse_mode="HTML")

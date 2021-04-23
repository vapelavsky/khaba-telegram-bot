from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User as TgUser

from bot.chains.base.kb import start_kb
from bot.core import dp


@dp.message_handler(commands="start", state="*")
async def start_command(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(
        f"Привіт,  {TgUser().get_current().first_name}!\n\n"
        f"Я - той, хто допоможе тобі робити вітер у студентському самоврядуванні :)\n\n"
        f"Ти мені пишеш, який захід хочеш організувати, що для цього треба, "
        f"а я тобі розповідаю як це все втілити у життя.",
        reply_markup=start_kb,
    )

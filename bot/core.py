from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor

from bot.config import TELEGRAM_BOT_TOKEN
from middlewares.throttling import ThrottlingMiddleware

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode='HTML')

dp = Dispatcher(bot=bot, storage=MemoryStorage())

dp.middleware.setup(ThrottlingMiddleware())

executor = Executor(dp, skip_updates=True)

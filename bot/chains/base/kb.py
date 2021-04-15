from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Організувати захід 🎉'),
            KeyboardButton(text='Захід'),
            KeyboardButton(text='Залогінитися як адмін 😎')

        ]],
    resize_keyboard=True
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_record = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Скасувати', callback_data='event_record_cancel')]
    ],
    resize_keyboard=True)

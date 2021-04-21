from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_record = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Скасувати', callback_data='event_record_cancel')]
    ],
    resize_keyboard=True)

done_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Готово', callback_data='done_photos')]
    ],
    resize_keyboard=True)

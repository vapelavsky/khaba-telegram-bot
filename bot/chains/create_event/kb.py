from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Скасувати", callback_data="event_creation_cancel")]
    ],
    resize_keyboard=True,
)

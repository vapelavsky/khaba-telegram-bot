from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choose = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Так", callback_data="event_report_approve"),
            InlineKeyboardButton("Ні", callback_data="event_report_cancel"),
        ]
    ],
    resize_keyboard=True,
)

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Скасувати", callback_data="event_report_cancel")]
    ]
)

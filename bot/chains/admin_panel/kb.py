from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Додати користувача", callback_data="user_creation"),
            InlineKeyboardButton("Вилучити користувача", callback_data="user_delete"),
            InlineKeyboardButton("Список користувачів", callback_data="list_user"),
        ]
    ],
    resize_keyboard=False,
)

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Скасувати", callback_data="activity_cancel")]
    ]
)

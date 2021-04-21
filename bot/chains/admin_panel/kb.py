from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Додати користувача', callback_data='user_creation'),
         InlineKeyboardButton('Переглянути звіти на факультетах', callback_data='activity_report'),
         InlineKeyboardButton('Вилучити користувача', callback_data='user_delete'),
         InlineKeyboardButton('Список користувачів', callback_data='list_user')]
    ],
    resize_keyboard=False)

faculty_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('ЕлІТ', callback_data='ELIT'),
         InlineKeyboardButton('БІЕМ', callback_data='BIEM'),
         InlineKeyboardButton('МІ', callback_data='MI'),
         InlineKeyboardButton('ІФСК', callback_data='IFSK'),
         InlineKeyboardButton('ТеСЕТ', callback_data='TeSET'),
         InlineKeyboardButton('ННІ Права', callback_data='Pravo'),
         InlineKeyboardButton('Скасувати', callback_data='cancel_activity')]
    ]
)

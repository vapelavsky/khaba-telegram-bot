from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminPanel(StatesGroup):
    wait_name = State()
    wait_faculty = State()
    wait_password = State()
    wait_faculty_event = State()
    wait_name_delete = State()
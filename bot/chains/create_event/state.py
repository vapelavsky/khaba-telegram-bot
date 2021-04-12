from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateEvent(StatesGroup):
    wait_event = State()
    wait_list = State()

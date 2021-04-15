from aiogram.dispatcher.filters.state import StatesGroup, State


class RecordEvent(StatesGroup):
    wait_password = State()
    wait_event_name = State()
    wait_event_photos = State()

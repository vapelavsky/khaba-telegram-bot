from aiogram.dispatcher.filters.state import StatesGroup, State


class ReportEvents(StatesGroup):
    wait_for_password = State()

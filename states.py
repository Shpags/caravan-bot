from aiogram.fsm.state import State, StatesGroup


class EventForm(StatesGroup):
    choosing_dishes = State()
    waiting_for_guests = State()
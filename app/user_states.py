from aiogram.fsm.state import State, StatesGroup


class SearchForm(StatesGroup):
    waiting_for_code = State()
    text = State()
    gender = State()
    age_from = State()
    age_to = State()
    employment = State()
    experience = State()
    order_by = State()
    vacancy_id = State()
    education_level = State()

from aiogram.fsm.state import State, StatesGroup


class AddApplication(StatesGroup):
    """Class with all states in add application menu."""

    job_position = State()
    vacancy_url = State()
    company_name = State()
    salary = State()
    job_description = State()
    contacts = State()
    applied_date = State()

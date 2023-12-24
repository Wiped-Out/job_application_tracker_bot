from aiogram.fsm.state import State, StatesGroup


class MainMenu(StatesGroup):
    """Class with all states in main menu."""

    main_menu = State()

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from modules.bot.keyboards.keyboards import main_menu_kb
from modules.bot.states.main_menu import MainMenu
from modules.bot.static import messages


async def switch_to_main_menu(
        message: Message,
        state: FSMContext,
        is_from_start_menu: bool = False,
):
    """
    Switch user to main menu.

    Sets state and sends message with reply markup.

    :param message: Message from user
    :param state: FSM
    :param is_from_start_menu: Is function called from /start command
    """
    await state.set_state(MainMenu.main_menu)
    await message.answer(
        text=messages.START_MESSAGE if is_from_start_menu else messages.MAIN_MENU,
        reply_markup=main_menu_kb,
    )

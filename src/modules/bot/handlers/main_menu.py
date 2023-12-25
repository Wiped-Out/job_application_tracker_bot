from aiogram import F, Router  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from modules.bot.states.main_menu import MainMenu
from modules.bot.static import buttons, messages
from modules.bot.switchers import switchers

router = Router()


@router.message(MainMenu.main_menu, F.text == buttons.my_applications)
async def my_applications_menu(message: Message):
    """
    Handle the button "my_applications".

    :param message: Message from user
    """
    # todo continue development
    await message.answer(text=messages.IN_DEVELOPMENT)


@router.message(MainMenu.main_menu, F.text == buttons.new_application)
async def new_application_menu(message: Message, state: FSMContext):
    """
    Handle the button "new_application".

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_sending_job_position_menu(message=message, state=state)

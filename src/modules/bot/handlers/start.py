from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db.postgres import get_async_sessionmaker
from modules.bot.switchers import switchers
from modules.users.services.users_service import UsersService

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    """
    Handle the message from user with /start command.

    Adds user to database.
    If user already exists, it updates user's data like first name, last name etc.

    :param message: Message object from Telegram
    :param state: FSM
    """
    users_service = UsersService(async_session=await get_async_sessionmaker())

    await users_service.add_user(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
    )

    await switchers.switch_to_main_menu(message=message, state=state, is_from_start_menu=True)

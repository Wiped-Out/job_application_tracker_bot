from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from db.postgres import get_async_sessionmaker
from modules.applications.services.applications_service import \
    ApplicationsService
from modules.bot.static import messages

router = Router()


@router.message(Command('statistic'))
async def command_statistic(message: Message):
    """
    Handle the message from user with /statistic command.

    :param message: Message object from Telegram
    """
    applications_service = ApplicationsService(async_session=await get_async_sessionmaker())
    await message.answer(
        text=messages.STATISTIC.format(
            applications_count_made_today=await applications_service.get_applications_count_made_today(  # noqa: E501
                user_id=message.from_user.id,
            ),
        ),
    )

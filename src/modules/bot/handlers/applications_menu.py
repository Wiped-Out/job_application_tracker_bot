from aiogram import F, Router  # noqa: WPS347
from aiogram.types import CallbackQuery

from modules.bot.static import callback_data, messages
from modules.bot.switchers import switchers

router = Router()


@router.callback_query(F.data.startswith(callback_data.applications_page_prefix))
async def switch_to_another_page(callback_query: CallbackQuery):
    """
    Handle arrow buttons presses to change the page.

    :param callback_query: Callback query from user
    """
    await switchers.switch_to_applications_menu(
        message_or_query=callback_query,
        page=int(callback_query.data.split(':')[-1]),
    )


@router.callback_query(F.data.startswith(callback_data.application_prefix))
async def application_menu(callback_query: CallbackQuery):
    """
    Handle press on an application.

    :param callback_query: Callback query from user
    """
    # todo continue development
    await callback_query.answer(text=messages.IN_DEVELOPMENT)

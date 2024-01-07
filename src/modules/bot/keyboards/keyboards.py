import math

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.applications.models.application import ApplicationModel
from modules.bot.static import buttons, callback_data

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.new_application)],
        [KeyboardButton(text=buttons.my_applications)],
    ],
    resize_keyboard=True,
)

back_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.back)],
    ],
    resize_keyboard=True,
)

back_and_skip_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.skip)],
        [KeyboardButton(text=buttons.back)],
    ],
    resize_keyboard=True,
)

back_and_today_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.today)],
        [KeyboardButton(text=buttons.back)],
    ],
    resize_keyboard=True,
)


def applications_kb(
        applications: list[ApplicationModel],
        page: int,
        count_on_page: int = 10,
) -> InlineKeyboardMarkup:
    """
    Return keyboard with application on the page.

    :param applications: User's applications
    :param page: Page
    :param count_on_page: Count of elements on one page
    :returns: Keyboard
    """
    builder = InlineKeyboardBuilder()

    max_pages = math.ceil(len(applications) / count_on_page)

    if page + 1 > max_pages:
        next_page = 1
    else:
        next_page = page + 1

    if page - 1 < 1:
        previous_page = max_pages
    else:
        previous_page = page - 1

    for application in applications[(page - 1) * count_on_page: page * count_on_page]:
        builder.add(
            InlineKeyboardButton(
                text=application.job_position,
                callback_data=f'{callback_data.application_prefix}:{application.id}',
            ),
        )

    builder.row(
        InlineKeyboardButton(
            text='⬅️',
            callback_data=f'{callback_data.applications_page_prefix}:{previous_page}',
        ),
        InlineKeyboardButton(
            text='➡️',
            callback_data=f'{callback_data.applications_page_prefix}:{next_page}',
        ),
    )

    return builder.as_markup()

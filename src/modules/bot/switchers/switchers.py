from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db.postgres import get_async_sessionmaker
from modules.applications.services.applications_service import \
    ApplicationsService
from modules.bot.keyboards import keyboards
from modules.bot.states.add_application import AddApplication
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

    if is_from_start_menu:
        await message.answer(
            text=messages.START_MESSAGE,
            reply_markup=keyboards.main_menu_kb,
        )
    else:
        applications_service = ApplicationsService(async_session=await get_async_sessionmaker())
        await message.answer(
            text=messages.MAIN_MENU.format(
                applications_count_made_today=await applications_service.get_applications_count_made_today(  # noqa: E501
                    user_id=message.from_user.id,
                ),
            ),
            reply_markup=keyboards.main_menu_kb,
        )


async def switch_to_sending_job_position_menu(message: Message, state: FSMContext):
    """
    Switch user to sending job position.

    :param message: Message from user
    :param state: FSM
    """
    await state.set_state(AddApplication.job_position)
    await message.answer(text=messages.SEND_JOB_POSITION, reply_markup=keyboards.back_kb)


async def switch_to_sending_vacancy_url_menu(message: Message, state: FSMContext):
    """
    Switch user to sending vacancy url.

    :param message: Message from user
    :param state: FSM
    """
    await state.set_state(AddApplication.vacancy_url)
    await message.answer(text=messages.SEND_VACANCY_URL, reply_markup=keyboards.back_and_skip_kb)


async def switch_to_sending_company_name_menu(message: Message, state: FSMContext):
    """
    Switch user to sending company name.

    :param message: Message from user
    :param state: FSM
    """
    await state.set_state(AddApplication.company_name)
    await message.answer(text=messages.SEND_COMPANY_NAME, reply_markup=keyboards.back_kb)


async def switch_to_sending_salary_menu(message: Message, state: FSMContext):
    """
    Switch user to sending salry.

    :param message: Message from user
    :param state: FSM
    """
    await state.set_state(AddApplication.salary)
    await message.answer(text=messages.SEND_SALARY, reply_markup=keyboards.back_and_skip_kb)


async def switch_to_send_job_description_menu(message: Message, state: FSMContext):
    """
    Switch user to sending job description.

    :param message: Message from user
    :param state: FSM
    """
    await state.set_state(AddApplication.job_description)
    await message.answer(
        text=messages.SEND_JOB_DESCRIPTION,
        reply_markup=keyboards.back_and_skip_kb,
    )


async def switch_to_send_contacts_menu(message: Message, state: FSMContext):
    """
    Switch user to sending contacts.

    :param message: Message from user
    :param state: FSM
    """
    await state.set_state(AddApplication.contacts)
    await message.answer(
        text=messages.SEND_CONTACTS,
        reply_markup=keyboards.back_and_skip_kb,
    )


async def switch_to_send_location_menu(message: Message, state: FSMContext):
    """
    Switch user to sending location of job.

    :param message: Message from user
    :param state: FSM
    """
    await state.set_state(AddApplication.location)
    await message.answer(
        text=messages.SEND_LOCATION,
        reply_markup=keyboards.back_and_skip_kb,
    )


async def switch_to_send_applied_date_menu(message: Message, state: FSMContext):
    """
    Switch user to sending applied date.

    :param message: Message from user
    :param state: FSM
    """
    await state.set_state(AddApplication.applied_date)
    await message.answer(
        text=messages.SEND_APPLIED_DATE,
        reply_markup=keyboards.back_and_today_kb,
    )


async def switch_to_applications_menu(
        message_or_query: Message | CallbackQuery,
        page: int = 1,
):
    """
    Switch user to job applications menu.

    :param message_or_query: Message or CallbackQuery from user
    :param page: Page
    """
    applications_service = ApplicationsService(async_session=await get_async_sessionmaker())
    applications = await applications_service.get_applications_for_user(
        user_id=message_or_query.from_user.id,
    )

    if isinstance(message_or_query, Message):
        await message_or_query.answer(
            text=messages.JOB_APPLICATIONS_MENU,
            reply_markup=keyboards.applications_kb(applications=applications, page=page),
        )
    else:
        await message_or_query.message.edit_text(
            text=messages.JOB_APPLICATIONS_MENU,
            reply_markup=keyboards.applications_kb(applications=applications, page=page),
        )

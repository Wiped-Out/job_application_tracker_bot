from datetime import date, datetime

from aiogram import F, Router  # noqa: WPS347
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.bot_settings import bot_settings
from db.postgres import get_async_sessionmaker
from modules.applications.services.applications_service import \
    ApplicationsService
from modules.bot.states.add_application import AddApplication
from modules.bot.static import buttons, messages
from modules.bot.switchers import switchers

router = Router()


@router.message(AddApplication.job_position, F.text == buttons.back)
async def back_to_main_menu(message: Message, state: FSMContext):
    """
    Handle press of "Back" button at the stage of sending the job position.

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_main_menu(message=message, state=state)


@router.message(AddApplication.job_position)
async def send_job_position(message: Message, state: FSMContext):
    """
    Handle a job position from user.

    :param message: Message from user
    :param state: FSM
    :returns: None
    """
    if len(message.text) > bot_settings.job_position_max_length:
        return await message.reply(
            text=messages.YOUR_MESSAGE_IS_TOO_LONG.format(
                max_length=bot_settings.job_position_max_length,
            ),
        )

    await state.update_data(job_position=message.text)
    await switchers.switch_to_sending_vacancy_url_menu(message=message, state=state)


@router.message(AddApplication.vacancy_url, F.text == buttons.back)
async def back_to_job_position_menu(message: Message, state: FSMContext):
    """
    Handle press of "Back" button at the stage of sending vacancy url.

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_sending_job_position_menu(message=message, state=state)


@router.message(AddApplication.vacancy_url, F.text == buttons.skip)
async def skip_entering_vacancy_url(message: Message, state: FSMContext):
    """
    Handle press of "Skip" button at the stage of sending vacancy url.

    :param message: Message from user
    :param state: FSM
    """
    await state.update_data(vacancy_url=None)
    await switchers.switch_to_sending_company_name_menu(message=message, state=state)


@router.message(AddApplication.vacancy_url)
async def send_vacancy_url(message: Message, state: FSMContext):
    """
    Handle a vacancy url from user.

    :param message: Message from user
    :param state: FSM
    """
    if len(message.text) > bot_settings.vacancy_url_max_length:
        await message.reply(
            text=messages.YOUR_MESSAGE_IS_TOO_LONG.format(
                max_length=bot_settings.vacancy_url_max_length,
            ),
        )
        return

    await state.update_data(vacancy_url=message.text)
    await switchers.switch_to_sending_company_name_menu(message=message, state=state)


@router.message(AddApplication.company_name, F.text == buttons.back)
async def back_to_vacany_url_menu(message: Message, state: FSMContext):
    """
    Handle press of "Back" button at the stage of sending company name.

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_sending_vacancy_url_menu(message=message, state=state)


@router.message(AddApplication.company_name)
async def send_company_name(message: Message, state: FSMContext):
    """
    Handle company name from user.

    :param message: Message from user.
    :param state: FSM
    :returns: None
    """
    if len(message.text) > bot_settings.company_name_max_length:
        return await message.reply(
            text=messages.YOUR_MESSAGE_IS_TOO_LONG.format(
                max_length=bot_settings.company_name_max_length,
            ),
        )

    await state.update_data(company_name=message.text)
    await switchers.switch_to_sending_salary_menu(message=message, state=state)


@router.message(AddApplication.salary, F.text == buttons.back)
async def back_to_company_name_menu(message: Message, state: FSMContext):
    """
    Handle press of "Back" button at the stage of sending salary.

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_sending_company_name_menu(message=message, state=state)


@router.message(AddApplication.salary, F.text == buttons.skip)
async def skip_entering_salary(message: Message, state: FSMContext):
    """
    Handle press of "Skip" button at the stage of sending salary.

    :param message: Message from user
    :param state: FSM
    """
    await state.update_data(salary=None)
    await switchers.switch_to_send_job_description_menu(message=message, state=state)


@router.message(AddApplication.salary)
async def send_salary(message: Message, state: FSMContext):
    """
    Handle a salary from user.

    :param message: Message from user
    :param state: FSM
    :returns: None
    """
    if len(message.text) > bot_settings.salary_max_length:
        return await message.reply(
            text=messages.YOUR_MESSAGE_IS_TOO_LONG.format(
                max_length=bot_settings.salary_max_length,
            ),
        )

    await state.update_data(salary=message.text)
    await switchers.switch_to_send_job_description_menu(message=message, state=state)


@router.message(AddApplication.job_description, F.text == buttons.back)
async def back_to_salary_menu(message: Message, state: FSMContext):
    """
    Handle press of "Back" button at the stage of sending job description.

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_sending_salary_menu(message=message, state=state)


@router.message(AddApplication.job_description, F.text == buttons.skip)
async def skip_entering_job_description(message: Message, state: FSMContext):
    """
    Handle press of "Skip" button at the stage of sending job description.

    :param message: Message from user
    :param state: FSM
    """
    await state.update_data(job_description=None)
    await switchers.switch_to_send_contacts_menu(message=message, state=state)


@router.message(AddApplication.job_description)
async def send_job_description(message: Message, state: FSMContext):
    """
    Handle a job description from user.

    :param message: Message from user
    :param state: FSM
    :returns: None
    """
    if len(message.text) > bot_settings.job_description_max_length:
        return await message.reply(
            text=messages.YOUR_MESSAGE_IS_TOO_LONG.format(
                max_length=bot_settings.job_description_max_length,
            ),
        )

    await state.update_data(job_description=message.text)
    await switchers.switch_to_send_contacts_menu(message=message, state=state)


@router.message(AddApplication.contacts, F.text == buttons.back)
async def back_to_job_description_menu(message: Message, state: FSMContext):
    """
    Handle press of "Back" button at the stage of sending contacts.

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_send_job_description_menu(message=message, state=state)


@router.message(AddApplication.contacts, F.text == buttons.skip)
async def skip_entering_contacts(message: Message, state: FSMContext):
    """
    Handle press of "Skip" button at the stage of sending contacts.

    :param message: Message from user
    :param state: FSM
    """
    await state.update_data(contacts=None)
    await switchers.switch_to_send_location_menu(message=message, state=state)


@router.message(AddApplication.contacts)
async def send_contacts(message: Message, state: FSMContext):
    """
    Handle contacts from user.

    :param message: Message from user
    :param state: FSM
    :returns: None
    """
    if len(message.text) > bot_settings.contacts_max_length:
        return await message.reply(
            text=messages.YOUR_MESSAGE_IS_TOO_LONG.format(
                max_length=bot_settings.contacts_max_length,
            ),
        )

    await state.update_data(contacts=message.text)
    await switchers.switch_to_send_location_menu(message=message, state=state)


@router.message(AddApplication.location, F.text == buttons.back)
async def back_to_contacts_menu(message: Message, state: FSMContext):
    """
    Handle press of "Back" button at the stage of sending location.

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_send_contacts_menu(message=message, state=state)


@router.message(AddApplication.location, F.text == buttons.skip)
async def skip_entering_location(message: Message, state: FSMContext):
    """
    Handle press of "Skip" button at the stage of sending location.

    :param message: Message from user
    :param state: FSM
    """
    await state.update_data(location=None)
    await switchers.switch_to_send_applied_date_menu(message=message, state=state)


@router.message(AddApplication.location)
async def send_location(message: Message, state: FSMContext):
    """
    Handle location from user.

    :param message: Message from user
    :param state: FSM
    :returns: None
    """
    if len(message.text) > bot_settings.location_max_length:
        return await message.reply(
            text=messages.YOUR_MESSAGE_IS_TOO_LONG.format(
                max_length=bot_settings.location_max_length,
            ),
        )

    await state.update_data(location=message.text)
    await switchers.switch_to_send_applied_date_menu(message=message, state=state)


@router.message(AddApplication.applied_date, F.text == buttons.back)
async def back_to_location_menu(message: Message, state: FSMContext):
    """
    Handle press of "Back" button at the stage of sending applied date.

    :param message: Message from user
    :param state: FSM
    """
    await switchers.switch_to_send_location_menu(message=message, state=state)


@router.message(AddApplication.applied_date, F.text == buttons.today)
async def applied_date_today(message: Message, state: FSMContext):
    """
    Handle press of "Today" button at the stage of sending applied date.

    :param message: Message from user
    :param state: FSM
    """
    await process_application_data(message=message, state=state, applied_date=date.today())


@router.message(AddApplication.applied_date)
async def send_applied_date(message: Message, state: FSMContext):
    """
    Handle applied date from user.

    :param message: Message from user
    :param state: FSM
    :returns: None
    """
    try:
        applied_date = datetime.strptime(message.text, '%d.%m.%Y').date()
    except Exception:
        await message.reply(text=messages.INCORRECT_INPUT)
        return

    await process_application_data(message=message, state=state, applied_date=applied_date)


async def process_application_data(  # noqa: WPS217
        message: Message,
        state: FSMContext,
        applied_date: date,
):
    """
    Process entered data.

    Saves data to database and switches user to main menu.

    :param message: Message from user
    :param state: FSM
    :param applied_date: Applied date
    """
    state_data = await state.get_data()

    applications_service = ApplicationsService(async_session=await get_async_sessionmaker())
    await applications_service.add_application(
        user_id=message.from_user.id,
        job_position=state_data['job_position'],
        vacancy_url=state_data['vacancy_url'],
        company_name=state_data['company_name'],
        salary=state_data['salary'],
        job_description=state_data['job_description'],
        contacts=state_data['contacts'],
        location=state_data['location'],
        applied_date=applied_date,
    )

    await state.clear()
    await message.reply(text=messages.APPLICATION_SAVED)
    await switchers.switch_to_main_menu(message=message, state=state)

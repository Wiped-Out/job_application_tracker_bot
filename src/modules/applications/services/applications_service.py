from datetime import date

from db.postgres import DatabaseService
from enums import OnConflict
from modules.applications.models.application import ApplicationModel


class ApplicationsService(DatabaseService):
    """A service that encapsulates the logic of working with database table of applications."""

    model = ApplicationModel

    async def add_application(  # noqa: WPS211
            self,
            user_id: int,
            job_position: str,
            vacancy_url: str | None,
            company_name: str,
            salary: str | None,
            job_description: str | None,
            contacts: str | None,
            location: str,
            applied_date: date,
    ):
        """
        Add application to database.

        :param user_id: ID of user, which created an application
        :param job_position: Job position
        :param vacancy_url: Vacanry URL
        :param company_name: Company name
        :param salary: Salary
        :param job_description: Job description
        :param contacts: Contacts of recruiter
        :param location: Job location
        :param applied_date: Applied date
        """
        await self._add(
            job_position=job_position,
            vacancy_url=vacancy_url,
            company_name=company_name,
            salary=salary,
            job_description=job_description,
            contacts=contacts,
            location=location,
            applied_date=applied_date,
            user_id=user_id,
        )

    async def add_user(  # noqa: WPS211
            self,
            telegram_id: int,
            first_name: str,
            last_name: str | None,
            username: str | None,
            language_code: str,
    ):
        """
        Add user to database.

        If user exists, updates data like first name, last name etc.

        :param telegram_id: Telegram ID of user
        :param first_name: User's first name
        :param last_name: User's last name
        :param username: User's username
        :param language_code: Language code of the user application
        """
        await self._add(
            index_elements=['telegram_id'],
            on_conflict=OnConflict.do_update,
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            language_code=language_code,
        )

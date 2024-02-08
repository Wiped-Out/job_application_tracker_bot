from datetime import date, datetime, timedelta

from sqlalchemy import and_

from db.postgres import DatabaseService
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

    async def get_applications_for_user(self, user_id: int) -> list[ApplicationModel]:
        """
        Get applications for user.

        :param user_id: ID of user
        :returns: list of applications
        """
        return await self._get_all(self.model.user_id == user_id)

    async def get_applications_count_made_today(self, user_id: int) -> int:
        """
        Get user's applications count made today.

        :param user_id: ID of user

        :returns: applications count made today
        """
        now = datetime.now()
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return await self._count(
            self.model.user_id == user_id,
            and_(
                self.model.created_at >= now,
                self.model.created_at <= now + timedelta(days=1),
            ),
        )

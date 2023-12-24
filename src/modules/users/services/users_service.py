from db.postgres import DatabaseService
from enums import OnConflict
from modules.users.models.user import UserModel


class UsersService(DatabaseService):
    """A service that encapsulates the logic of working with database table of users."""

    model = UserModel

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

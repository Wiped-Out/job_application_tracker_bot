from datetime import datetime

from sqlalchemy import BIGINT, func
from sqlalchemy.orm import Mapped, mapped_column

from db.postgres import ModelBase


class UserModel(ModelBase):
    """Model of users table."""

    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    language_code: Mapped[str] = mapped_column(nullable=False)

    first_bot_launch: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(),
    )

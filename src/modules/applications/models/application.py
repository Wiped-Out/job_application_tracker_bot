from datetime import date, datetime

from sqlalchemy import BIGINT, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from db.postgres import ModelBase
from enums import ApplicationStatus


class ApplicationModel(ModelBase):
    """Model of applications table."""

    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    job_position: Mapped[str] = mapped_column(nullable=False)
    vacancy_url: Mapped[str] = mapped_column(nullable=True)
    company_name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=True)
    salary: Mapped[str] = mapped_column(nullable=True)
    job_description: Mapped[str] = mapped_column(nullable=True)
    contacts: Mapped[str] = mapped_column(nullable=True)
    applied_date: Mapped[date] = mapped_column(nullable=False)

    follow_up_date: Mapped[date] = mapped_column(nullable=True)

    status: Mapped[ApplicationStatus] = mapped_column(
        nullable=False,
        default=ApplicationStatus.applied,
    )

    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey('users.telegram_id'),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now,
        server_default=func.now(),
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now,
        server_default=func.now(),
    )

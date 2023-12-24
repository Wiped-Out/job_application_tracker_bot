from typing import Any, Generic, Type, TypeVar, cast

from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, joinedload
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.elements import BinaryExpression

from core.postgres_settings import postgres_settings
from enums import OnConflict


class ModelBase(DeclarativeBase):
    """Base model for SQLAlchemy models."""


engine = create_async_engine(
    postgres_settings.get_sqlalchemy_dsn(),
    future=True,
)


async def get_async_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """
    Return async sessionmaker.

    :returns: Async sessionmaker
    """
    return async_sessionmaker(engine, expire_on_commit=False)


ASTERISK = '*'  # Переменная для Астерикса в запросе SQL

# Переменные для type-hint
SQLAlchemyModel = TypeVar('SQLAlchemyModel', bound=ModelBase)
ExpressionType = BinaryExpression | ClauseElement | bool


class DatabaseService(Generic[SQLAlchemyModel]):  # noqa: WPS214
    """Base service for interaction with database."""

    model: Type[SQLAlchemyModel]

    def __init__(
            self,
            async_session: async_sessionmaker[AsyncSession],
            query_model: Type[SQLAlchemyModel] | None = None,
    ) -> None:
        """
        Initialize service.

        :param async_session: Async session
        :param query_model: SQLAlchemy model
        """
        self.async_session = async_session
        self.model = query_model or self.model

    async def _add(
            self,
            index_elements: list[str] | None = None,
            on_conflict: OnConflict = OnConflict.do_nothing,
            **values: Any,  # noqa: WPS110
    ) -> SQLAlchemyModel | None:
        statement = insert(self.model).values(**values).returning(ASTERISK)
        if index_elements:
            if on_conflict == OnConflict.do_nothing:
                statement = statement.on_conflict_do_nothing(index_elements=index_elements)
            else:
                statement = statement.on_conflict_do_update(
                    index_elements=index_elements,
                    set_={key: statement.excluded[key] for key in values.keys()},
                )

        async with self.async_session() as session:
            session_result = await session.execute(statement)
            scalars = session_result.fetchone()
            await session.commit()

        return cast(SQLAlchemyModel, scalars)

    async def _add_many(
            self,
            list_of_dicts_to_add: list[dict],
            index_elements: list[str] | None = None,
            on_conflict: OnConflict = OnConflict.do_nothing,
    ):
        statement = insert(self.model).values(list_of_dicts_to_add).returning(ASTERISK)
        if index_elements:
            if on_conflict == OnConflict.do_nothing:
                statement = statement.on_conflict_do_nothing(index_elements=index_elements)
            else:
                statement = statement.on_conflict_do_update(
                    index_elements=index_elements,
                    set_={key: statement.excluded[key] for key in list_of_dicts_to_add[0].keys()},
                )

        async with self.async_session() as session:
            session_result = await session.execute(statement)
            scalars = session_result.fetchall()
            await session.commit()

        return cast(list[SQLAlchemyModel], scalars)

    async def _get_all(  # noqa: WPS210
            self,
            *clauses: ExpressionType,
            joinedload_attributes: tuple[Any, ...] | None = None,
    ) -> list[SQLAlchemyModel]:
        statement = select(self.model).where(*clauses)
        if joinedload_attributes is not None:
            for joinedload_attribute in joinedload_attributes:
                statement = statement.options(joinedload(joinedload_attribute))

        async with self.async_session() as session:
            session_result = await session.execute(statement)
            scalars = session_result.scalars().unique().all()

        return cast(list[SQLAlchemyModel], scalars)

    async def _get_all_with_limit_and_offset(  # noqa: WPS211
            self,
            *clauses: ExpressionType,
            page_size: int,
            page: int,
            joinedload_attributes: tuple[Any, ...] | None = None,
            order_by: Any | None = None,
    ) -> list[SQLAlchemyModel]:
        statement = select(
            self.model,
        ).where(
            *clauses,
        ).limit(
            page_size,
        ).offset(
            (page - 1) * page_size,
        )

        if joinedload_attributes is not None:
            for joinedload_attribute in joinedload_attributes:
                statement = statement.options(joinedload(joinedload_attribute))

        if order_by is not None:
            statement.order_by(order_by)

        async with self.async_session() as session:
            session_result = await session.execute(statement)
            scalars = session_result.scalars().unique().all()
        return cast(list[SQLAlchemyModel], scalars)

    async def _get_one(
            self,
            *clauses: ExpressionType,
            joinedload_attributes: tuple[Any, ...] | None = None,
    ) -> SQLAlchemyModel | None:
        statement = select(self.model).where(*clauses)

        if joinedload_attributes is not None:
            for joinedload_attribute in joinedload_attributes:
                statement = statement.options(joinedload(joinedload_attribute))

        async with self.async_session() as session:
            session_result = await session.execute(statement)
            first_scalar_result = session_result.scalars().first()
        return first_scalar_result

    async def _update(self, *clauses: ExpressionType, **values: Any):  # noqa: WPS110
        async with self.async_session() as session:
            statement = update(self.model).where(*clauses).values(**values)
            await session.execute(statement)
            await session.commit()

    async def _exists(self, *clauses: ExpressionType) -> bool:
        async with self.async_session() as session:
            statement = exists(self.model).where(*clauses).select()
            session_result = (await session.execute(statement)).scalar()
        return cast(bool, session_result)

    async def _delete(self, *clauses: ExpressionType) -> list[SQLAlchemyModel]:
        async with self.async_session() as session:
            statement = delete(self.model).where(*clauses).returning(ASTERISK)
            session_result = (await session.execute(statement)).scalars().all()
            await session.commit()
        return cast(list[SQLAlchemyModel], session_result)

    async def _count(self, *clauses: ExpressionType) -> int:
        statement = select(
            func.count(ASTERISK),
        ).select_from(
            self.model,
        ).where(
            *clauses,
        )

        async with self.async_session() as session:
            async_result = await session.execute(statement)
        return cast(int, async_result.scalar())

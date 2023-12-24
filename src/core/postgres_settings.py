from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    """Environment variables for postgres."""

    db: str
    user: str
    password: str
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

    def get_sqlalchemy_dsn(self) -> str:
        """
        Return the dsn string.

        :returns: DSN string
        """
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'  # noqa: E501, WPS221


postgres_settings = PostgresSettings()

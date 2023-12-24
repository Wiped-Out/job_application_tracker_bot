from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    """Environment variables for redis."""

    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix='REDIS_', extra='allow')


redis_settings = RedisSettings()

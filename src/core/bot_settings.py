from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Environment variables for bot."""

    token: str

    model_config = SettingsConfigDict(env_prefix='BOT_', extra='allow')


bot_settings = BotSettings()

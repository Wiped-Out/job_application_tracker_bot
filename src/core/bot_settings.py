from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Environment variables for bot."""

    token: str

    job_position_max_length: int = 128
    vacancy_url_max_length: int = 256
    company_name_max_length: int = 128
    salary_max_length: int = 64
    job_description_max_length: int = 1024
    contacts_max_length: int = 128

    model_config = SettingsConfigDict(env_prefix='BOT_', extra='allow')


bot_settings = BotSettings()

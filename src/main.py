import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from core.bot_settings import bot_settings
from core.redis_settings import redis_settings
from modules.bot.handlers import register_all_routes

dp = Dispatcher(
    storage=RedisStorage(
        redis=Redis(host=redis_settings.host, port=redis_settings.port),
    ),
)

register_all_routes(dp=dp)


async def main():
    """Initialize bot and start dispatcher."""
    bot = Bot(token=bot_settings.token, parse_mode='HTML')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

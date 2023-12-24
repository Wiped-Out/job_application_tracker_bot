from aiogram import Dispatcher

from modules.bot.handlers.main_menu import router as main_menu_router
from modules.bot.handlers.start import router as start_router


def register_all_routes(dp: Dispatcher):
    dp.include_router(router=start_router)
    dp.include_router(router=main_menu_router)

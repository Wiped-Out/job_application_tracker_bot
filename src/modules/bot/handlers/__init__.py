from aiogram import Dispatcher

from modules.bot.handlers.applications_menu import \
    router as applications_menu_router
from modules.bot.handlers.main_menu import router as main_menu_router
from modules.bot.handlers.new_application import \
    router as new_application_router
from modules.bot.handlers.start import router as start_router
from modules.bot.handlers.statistic import router as statistic_router


def register_all_routes(dp: Dispatcher):
    dp.include_router(router=start_router)
    dp.include_router(router=main_menu_router)
    dp.include_router(router=new_application_router)
    dp.include_router(router=applications_menu_router)
    dp.include_router(router=statistic_router)

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from modules.bot.static import buttons

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.new_application)],
        [KeyboardButton(text=buttons.my_applications)],
    ],
    resize_keyboard=True,
)

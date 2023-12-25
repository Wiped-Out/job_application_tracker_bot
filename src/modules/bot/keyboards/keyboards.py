from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from modules.bot.static import buttons

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.new_application)],
        [KeyboardButton(text=buttons.my_applications)],
    ],
    resize_keyboard=True,
)

back_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.back)],
    ],
    resize_keyboard=True,
)

back_and_skip_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.skip)],
        [KeyboardButton(text=buttons.back)],
    ],
    resize_keyboard=True,
)

back_and_today_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=buttons.today)],
        [KeyboardButton(text=buttons.back)],
    ],
    resize_keyboard=True,
)

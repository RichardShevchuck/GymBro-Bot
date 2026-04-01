from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить тренировку")],
            [KeyboardButton(text="Последние тренировки")],
        ],
        resize_keyboard=True,
    )
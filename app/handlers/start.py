from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.main import main_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "Привет! Я бот для учёта тренировок.\n\n"
        "Я могу:\n"
        "/add — добавить тренировку\n"
        "/history — показать последние тренировки\n\n"
        "Или используй кнопки ниже."
    )
    await message.answer(text, reply_markup=main_keyboard())
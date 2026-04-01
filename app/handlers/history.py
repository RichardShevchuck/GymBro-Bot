from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram import Router
from aiogram.types import Message

from app.database import SessionLocal
from app.services.workout_service import get_last_workouts

router = Router()


@router.message(lambda msg: msg.text == "Последние тренировки")
async def show_history(message: Message):
    async with SessionLocal() as session:
        workouts = await get_last_workouts(session, message.from_user.id)

    if not workouts:
        await message.answer("Нет тренировок")
        return

    text = ""

    for w in workouts:
        text += f"\n📅 {w.started_at.strftime('%Y-%m-%d %H:%M')}\n"

        for e in w.entries:
            weight = f"{e.weight} кг" if e.weight else "без веса"
            text += f"- {e.exercise_name}: {weight}, {e.sets}x{e.reps}\n"

    await message.answer(text)
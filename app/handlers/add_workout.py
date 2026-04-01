from decimal import Decimal

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database import SessionLocal
from app.services.workout_service import add_workout_entry, finish_workout
from app.states import AddWorkoutStates

router = Router()


async def check_stop(message: Message, state: FSMContext) -> bool:
    if message.text == "/stop":
        async with SessionLocal() as session:
            workout = await finish_workout(session, message.from_user.id)

        if not workout:
            await message.answer("У тебя нет активной тренировки 🤷‍♂️")
        else:
            await message.answer("Тренировка завершена 💪")

        await state.clear()
        return True
    return False


@router.message(F.text == "Добавить тренировку")
async def start(message: Message, state: FSMContext):
    await state.set_state(AddWorkoutStates.waiting_for_exercise)
    await message.answer("Введите упражнение (или /stop):")


@router.message(AddWorkoutStates.waiting_for_exercise)
async def exercise(message: Message, state: FSMContext):
    if await check_stop(message, state):
        return

    await state.update_data(exercise_name=message.text)
    await state.set_state(AddWorkoutStates.waiting_for_weight)
    await message.answer("Вес (или 0) (/stop для завершения):")


@router.message(AddWorkoutStates.waiting_for_weight)
async def weight(message: Message, state: FSMContext):
    if await check_stop(message, state):
        return

    try:
        text = message.text.replace(",", ".")
        weight = Decimal(text)

        await state.update_data(weight=None if weight == 0 else weight)
        await state.set_state(AddWorkoutStates.waiting_for_reps)
        await message.answer("Повторения (/stop для завершения):")

    except Exception:
        await message.answer(
            "Введите число, например:\n"
            "80\n"
            "80.5\n"
            "или 0 (если без веса)"
        )


@router.message(AddWorkoutStates.waiting_for_reps)
async def reps(message: Message, state: FSMContext):
    if await check_stop(message, state):
        return

    try:
        reps = int(message.text)
        await state.update_data(reps=reps)
        await state.set_state(AddWorkoutStates.waiting_for_sets)
        await message.answer("Подходы (/stop для завершения):")
    except:
        await message.answer("Введите целое число (например 10)")


@router.message(AddWorkoutStates.waiting_for_sets)
async def sets(message: Message, state: FSMContext):
    if await check_stop(message, state):
        return

    try:
        sets = int(message.text)
    except:
        await message.answer("Введите целое число (например 3)")
        return

    data = await state.get_data()

    async with SessionLocal() as session:
        await add_workout_entry(
            session=session,
            telegram_user_id=message.from_user.id,
            username=message.from_user.username,
            exercise_name=data["exercise_name"],
            weight=data["weight"],
            reps=data["reps"],
            sets=sets,
        )

    await state.set_state(AddWorkoutStates.waiting_for_exercise)

    await message.answer(
        "Упражнение добавлено 💪\n\n"
        "Введи следующее упражнение или напиши /stop"
    )
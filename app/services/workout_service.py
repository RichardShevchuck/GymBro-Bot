from datetime import datetime
from decimal import Decimal
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import User, Workout, WorkoutEntry


async def get_or_create_user(session, telegram_user_id, username):
    result = await session.execute(
        select(User).where(User.telegram_user_id == telegram_user_id)
    )
    user = result.scalar_one_or_none()

    if user:
        return user

    user = User(
        telegram_user_id=telegram_user_id,
        username=username,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_active_workout(session, telegram_user_id):
    result = await session.execute(
        select(Workout)
        .join(User)
        .where(User.telegram_user_id == telegram_user_id)
        .where(Workout.finished_at.is_(None))
    )
    return result.scalar_one_or_none()


async def start_workout(session, telegram_user_id, username):
    user = await get_or_create_user(session, telegram_user_id, username)

    workout = Workout(user_id=user.id)
    session.add(workout)
    await session.commit()
    await session.refresh(workout)
    return workout


async def get_or_create_active_workout(session, telegram_user_id, username):
    workout = await get_active_workout(session, telegram_user_id)
    if workout:
        return workout
    return await start_workout(session, telegram_user_id, username)


async def add_workout_entry(
    session,
    telegram_user_id,
    username,
    exercise_name,
    weight,
    reps,
    sets,
):
    workout = await get_or_create_active_workout(
        session, telegram_user_id, username
    )

    entry = WorkoutEntry(
        workout_id=workout.id,
        exercise_name=exercise_name,
        weight=weight,
        reps=reps,
        sets=sets,
    )
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


async def finish_workout(session, telegram_user_id):
    workout = await get_active_workout(session, telegram_user_id)
    if not workout:
        return None

    workout.finished_at = datetime.utcnow()
    await session.commit()
    return workout


async def get_last_workouts(session, telegram_user_id):
    result = await session.execute(
        select(Workout)
        .options(selectinload(Workout.entries))
        .join(User)
        .where(User.telegram_user_id == telegram_user_id)
        .order_by(Workout.started_at.desc())
        .limit(5)
    )
    return result.scalars().all()
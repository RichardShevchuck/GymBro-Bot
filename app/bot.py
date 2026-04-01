import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import get_settings
from app.handlers.add_workout import router as add_workout_router
from app.handlers.history import router as history_router
from app.handlers.start import router as start_router

logging.basicConfig(level=logging.INFO)

settings = get_settings()


async def main() -> None:
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(add_workout_router)
    dp.include_router(history_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
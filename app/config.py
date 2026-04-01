import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    bot_token: str
    database_url: str


def get_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN")
    database_url = os.getenv("DATABASE_URL")

    if not bot_token:
        raise ValueError("BOT_TOKEN is not set")
    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    return Settings(
        bot_token=bot_token,
        database_url=database_url,
    )
#!env python3
import asyncio
from dotenv import load_dotenv
from internal import db, logger
from internal.config import Config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from plugins import (
    login_router, logout_router, start_router, notify_router,
    text_router, help_router
)

load_dotenv()

dp = Dispatcher()

# Registers all the function to handle incoming Telegram messages that use the command.
dp.include_router(start_router)
dp.include_router(notify_router)
dp.include_router(login_router)
dp.include_router(logout_router)
dp.include_router(text_router)
dp.include_router(help_router)

async def main() -> None:
    await db.init_db()
    config = Config()
    if not config.botApi:
        logger.error("Missing botApi environment variable")
        return
    bot = Bot(config.botApi, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot Stopped, Bye Bye!")
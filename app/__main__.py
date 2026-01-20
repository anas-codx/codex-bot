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
    project_router, back_router

)

# Load environment variables from the .env file into the system environment
load_dotenv()

# Create an instance of Dispatcher to handle and route incoming updates/events
dp = Dispatcher()

# Registers all the function to handle incoming Telegram messages that use the command.
dp.include_router(start_router)
dp.include_router(notify_router)
dp.include_router(login_router)
dp.include_router(logout_router)
dp.include_router(project_router)
dp.include_router(back_router)

async def main() -> None:
    await db.init_db()
    config = Config()
    if not config.botApi: # if the botApi is missing it will raise an error
        logger.error("Missing botApi environment variable")
        return
    bot = Bot(config.botApi, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot Stopped, Bye Bye!")
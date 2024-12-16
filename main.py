import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from config_data.config import config
from database.database import create_tables
from handlers.prompt import router as general_router
from handlers.menu import router as menu_router
from handlers.settings import router as settings_router
from handlers.payments import router as about_router
from handlers.help import router as help_router

bot = Bot(token=config.tg_bot.token)


async def main():
    dp = Dispatcher()

    await create_tables()

    dp.include_router(general_router)
    dp.include_router(menu_router)
    dp.include_router(settings_router)
    dp.include_router(about_router)
    dp.include_router(help_router)
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
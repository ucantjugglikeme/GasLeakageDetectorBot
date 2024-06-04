import sys
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import data
import utils


# TODO: add gracefull close for session


bot = Bot(  
    token=data["bot_token"], 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
background_tasks = set()


async def main():
    loop = asyncio.get_event_loop()
    # Listen for mqtt messages in an (unawaited) asyncio task
    task = loop.create_task(utils.mqtt_listen())
    # Save a reference to the task so it doesn't get garbage collected
    background_tasks.add(task)
    task.add_done_callback(background_tasks.remove)

    from handlers import router
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    if sys.platform.lower() == "win32" or os.name.lower() == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

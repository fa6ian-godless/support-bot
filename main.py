import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from dotenv import load_dotenv
from handlers import router
import os

load_dotenv()

bot = Bot(token = os.getenv('BOT_TOKEN'))
dispatcher = Dispatcher()


async def main():
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutdown...')
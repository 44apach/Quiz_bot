import asyncio
from aiogram import Dispatcher, Bot
from decouple import config

from handlers import messages, admin



Btoken = config("Token",default="")

async def main():

    dp = Dispatcher()
    bot = Bot(Btoken)


    dp.include_router(messages.router)
    dp.include_router(admin.router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
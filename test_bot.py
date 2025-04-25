import asyncio
from telegram import Bot

async def test():
    bot = Bot("7777339725:AAHd7AkbFBYRrcUl4wwGdbDsKvBo0b0FMGk")
    me = await bot.get_me()
    print(me)

asyncio.run(test())
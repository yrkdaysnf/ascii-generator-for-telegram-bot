import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand, BotCommandScopeDefault, Message
from ascii import ascii, stop


TOKEN = 'TOKEN' # Put ur TOKEN here

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await bot.set_my_commands([BotCommand(command='ascii', 
                                          description='Start ascii'), 
                               BotCommand(command='ascii_inv', 
                                          description='Start inverted ascii'),
                               BotCommand(command='stop', 
                                          description='Stop ascii')],
                               BotCommandScopeDefault())
    
    dp.message.register(ascii, F.text.startswith('/ascii'))
    dp.message.register(stop, F.text.startswith('/stop'))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
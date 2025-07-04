import asyncio
from telegram_bot.telegram_bot import init_bot

async def main():
    app = await init_bot()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

if __name__ == "__main__":
    asyncio.run(main())

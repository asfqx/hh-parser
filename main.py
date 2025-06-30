import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.config import settings
from app.services.get_tokens import tokens


bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


async def main():
    tokens.load_tokens()
    print(tokens.access_token, tokens.refresh_token)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
    )
    try:
        print("Bot started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

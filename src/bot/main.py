import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from src.core.config import settings
from src.core.i18n import _

logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # Basic start handler without DB for now
    welcome_text = _("Choose your language", lang_code="fa")
    await message.answer(f"{welcome_text}\n\n1. 🇮🇷 فارسی\n2. 🇬🇧 English")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

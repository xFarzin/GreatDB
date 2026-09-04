import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from src.core.config import settings
from src.core.i18n import _

logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    welcome_text = _("Choose your language", lang_code="fa")

    # Inline keyboard for language selection
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇮🇷 فارسی", callback_data="lang_fa"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
            ]
        ]
    )

    await message.answer(f"{welcome_text}", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery):
    lang_code = callback.data.split("_")[1]

    # Normally we would save this to the DB here
    # await user_repo.update_language(callback.from_user.id, lang_code)

    response_text = _("Welcome to Search Platform", lang_code=lang_code)
    await callback.message.edit_text(response_text)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from src.core.config import settings
from src.core.i18n import _
from src.core.db.session import async_session
from src.core.db.repository import UserRepository

logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()

def get_main_menu(lang_code: str) -> ReplyKeyboardMarkup:
    """Returns the main menu based on language"""
    # Texts in Persian
    if lang_code == 'fa':
        menu = [
            [KeyboardButton(text="🔎 جستجو"), KeyboardButton(text="🗄 دیتابیس‌ها")],
            [KeyboardButton(text="💎 امتیازات من"), KeyboardButton(text="💳 خرید امتیاز")],
            [KeyboardButton(text="⭐ اشتراک"), KeyboardButton(text="👥 دعوت دوستان")],
            [KeyboardButton(text="🗄 ارسال دیتابیس"), KeyboardButton(text="📊 تاریخچه")],
            [KeyboardButton(text="👤 حساب کاربری"), KeyboardButton(text="🆘 پشتیبانی")]
        ]
    else:
        menu = [
            [KeyboardButton(text="🔎 Search"), KeyboardButton(text="🗄 Databases")],
            [KeyboardButton(text="💎 My Credits"), KeyboardButton(text="💳 Buy Credits")],
            [KeyboardButton(text="⭐ Subscription"), KeyboardButton(text="👥 Invite Friends")],
            [KeyboardButton(text="🗄 Submit Dataset"), KeyboardButton(text="📊 History")],
            [KeyboardButton(text="👤 Account"), KeyboardButton(text="🆘 Support")]
        ]

    return ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # First, let's create the user in the database or get existing
    async with async_session() as db:
        repo = UserRepository(db)
        user = await repo.get_by_telegram_id(message.from_user.id)
        if not user:
            user = await repo.create_user(message.from_user.id, language="fa")

        # We assume new users or users running /start want to set language
        welcome_text = _("Choose your language", lang_code=user.language)

        # Inline keyboard for language selection
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🇮🇷 فارسی", callback_data="lang_fa"),
                    InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
                ]
            ]
        )

        await message.answer(welcome_text, reply_markup=keyboard)

@dp.callback_query(F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery):
    lang_code = callback.data.split("_")[1]

    async with async_session() as db:
        repo = UserRepository(db)
        user = await repo.get_by_telegram_id(callback.from_user.id)
        if user:
            user.language = lang_code
            db.add(user)
            await db.commit()

    response_text = _("Welcome to Search Platform", lang_code=lang_code)

    # Edit the inline message to just say welcome
    await callback.message.edit_text(response_text)

    # Send the main menu keyboard in a new message
    menu = get_main_menu(lang_code)
    await callback.message.answer(response_text, reply_markup=menu)
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

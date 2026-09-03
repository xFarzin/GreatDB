import asyncio
import logging
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from sqlalchemy import select
from src.core.db.session import async_session
from src.core.models.user import User
from src.core.models.broadcast import Broadcast, BroadcastStatus
from src.core.config import settings

logger = logging.getLogger(__name__)
bot = Bot(token=settings.telegram_bot_token)
BATCH_SIZE = 100

async def process_broadcast(broadcast_id: int):
    async with async_session() as db:
        broadcast = await db.get(Broadcast, broadcast_id)
        if not broadcast or broadcast.status != BroadcastStatus.PENDING:
            return

        broadcast.status = BroadcastStatus.RUNNING
        await db.commit()

        try:
            # We fetch users in batches (keyset pagination recommended for production, using offset for simplicity here)
            offset = 0
            while True:
                result = await db.execute(
                    select(User.telegram_id, User.language)
                    .where(User.is_active == True)
                    .order_by(User.id)
                    .limit(BATCH_SIZE)
                    .offset(offset)
                )
                users = result.all()
                if not users:
                    break

                for tg_id, lang in users:
                    msg = broadcast.message_fa if lang == 'fa' else broadcast.message_en
                    # Fallback to the other language if missing
                    if not msg:
                        msg = broadcast.message_fa or broadcast.message_en

                    if not msg:
                        continue

                    try:
                        await bot.send_message(chat_id=tg_id, text=msg)
                        broadcast.sent_count += 1
                        # Respect rate limits (Telegram limit: ~30 msg/sec total)
                        await asyncio.sleep(0.05)
                    except TelegramRetryAfter as e:
                        logger.warning(f"Rate limited. Sleeping {e.retry_after} seconds.")
                        await asyncio.sleep(e.retry_after)
                        broadcast.failed_count += 1 # Or retry
                    except Exception as e:
                        logger.error(f"Failed to send to {tg_id}: {e}")
                        broadcast.failed_count += 1

                # Update progress
                await db.commit()
                offset += BATCH_SIZE

            broadcast.status = BroadcastStatus.COMPLETED
            await db.commit()

        except Exception as e:
            logger.exception(f"Broadcast {broadcast_id} failed completely.")
            broadcast.status = BroadcastStatus.FAILED
            await db.commit()
            raise e
        finally:
            await bot.session.close()

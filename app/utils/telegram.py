import asyncio

from telegram import Bot

from app.utils.config import config
from app.utils.logger import logger


class TelegramService:
    def __init__(self):
        self.bot = None
        self.chat_id = config.telegram.chat_id
        if config.telegram.token:
            self.bot = Bot(token=config.telegram.token)
            logger.info("Telegram bot initialized")
        else:
            logger.warning("Telegram token not found. Skipping initialization.")

    async def send_message(self, message: str):
        if not self.bot or not self.chat_id:
            return
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")

    def send_sync(self, message: str):
        """Wrapper to run async send_message synchronously"""
        if not self.bot:
            return
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we are already in a loop (e.g. async app), create a task
                loop.create_task(self.send_message(message))
            else:
                loop.run_until_complete(self.send_message(message))
        except RuntimeError:
            # Create new loop if none exists
            asyncio.run(self.send_message(message))
        except Exception as e:
            logger.error(f"Failed to send sync Telegram message: {e}")


telegram = TelegramService()

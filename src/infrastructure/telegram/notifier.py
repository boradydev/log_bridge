import asyncio
import logging

from aiogram import Bot

from src.presentation.log_dispatchers.abcs import INotifier


class TelegramNotifier(INotifier):
    def __init__(
        self,
        bot: Bot,
        chat_ids: list[str],
        logger: logging.Logger | None = None,
    ) -> None:
        self._bot = bot
        self._chat_ids = chat_ids
        self._logger = logger or logging.getLogger(__name__)

    async def send_message(
        self,
        message: str,
    ) -> None:
        for chat_id in self._chat_ids:
            while True:
                try:
                    await self._bot.send_message(chat_id, message)
                    break
                except Exception as exc:
                    self._logger.error(
                        f"Failed to send message to chat {chat_id}: {exc}"
                    )
                    await asyncio.sleep(5)

import asyncio

from aiogram import Bot

from src.presentation.log_dispatchers.abcs import INotifier


class TelegramNotifier(INotifier):
    def __init__(self, bot: Bot, chat_ids: list[str]) -> None:
        self._bot = bot
        self._chat_ids = chat_ids

    async def send_message(
        self,
        message: str,
    ) -> None:
        for chat_id in self._chat_ids:
            asyncio.create_task(self._bot.send_message(chat_id, message))

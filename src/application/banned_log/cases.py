from __future__ import annotations

import logging

from src.application.banned_log.abcs import ILogCase
from src.application.banned_log.dtos import BanLogRecordDTO
from src.core.locales.stub.ban import I18nContext
from src.presentation.log_dispatchers.abcs import INotifier


logger = logging.getLogger(__name__)


class BannedEventCase(ILogCase[BanLogRecordDTO]):
    def __init__(
        self,
        notifier: INotifier,
        messages: I18nContext,
    ) -> None:
        self.notifier = notifier
        self.messages = messages

    async def execute(self, dto: BanLogRecordDTO) -> None:
        match dto.action:
            case "BAN":
                message = self.messages.ban(
                    email=dto.email,
                    client_ip=dto.client_ip,
                )
            case "UNBAN":
                message = self.messages.unban(
                    email=dto.email,
                    client_ip=dto.client_ip,
                )
            case _:
                logger.warning(f"Unknown action: {dto.action}")
                return
        await self.notifier.send_message(message)

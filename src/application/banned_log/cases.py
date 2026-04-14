import logging
from typing import TYPE_CHECKING

from src.application.banned_log.abcs import ILogCase
from src.application.banned_log.dtos import BanLogRecord
from src.presentation.ban_log_dispatcher.abcs import INotifier


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.core.locales.ban import I18nContext as I18n


class BannedEventCase(ILogCase[BanLogRecord]):
    def __init__(
        self,
        notifier: INotifier,
        messages: I18n,
    ) -> None:
        self.notifier = notifier
        self.messages = messages

    async def execute(self, dto: BanLogRecord) -> None:
        match dto.action:
            case "BAN":
                message = self.messages.BAN(
                    email=dto.email,
                    client_ip=dto.client_ip,
                    duration=dto.duration,
                )
            case "UNBAN":
                message = self.messages.UNBAN(
                    email=dto.email,
                    client_ip=dto.client_ip,
                )
            case _:
                logger.warning(f"Unknown action: {dto.action}")
                return

        await self.notifier.send_message(message)

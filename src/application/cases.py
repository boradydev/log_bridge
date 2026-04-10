from src.application.abcs import ILogCase, ITelegramLogMessage
from src.application.dtos import BanLogRecord
from src.presentation.watch_events.abcs import INotifier


class BannedEventCase(ILogCase):
    def __init__(
        self,
        notifier: INotifier,
        message_map: ITelegramLogMessage[BanLogRecord],
    ) -> None:
        self.notifier = notifier
        self.message_map = message_map

    async def execute(self, dto: BanLogRecord) -> None:
        await self.notifier.notify(self.message_map.get(dto))

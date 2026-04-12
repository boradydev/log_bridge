import logging
import re
from datetime import datetime

from src.application.abcs import ILogCase
from src.application.dtos import BanLogRecord
from src.presentation.ban_log_dispatcher.abcs import IRoute


logger = logging.getLogger(__name__)


class BannedLogRoute(IRoute):
    def __init__(self) -> None:
        self._cases: list[ILogCase[BanLogRecord]] = []
        self._PATTERN = re.compile(
            r"(?P<timestamp>[\d/: ]+)\s+"
            r"(?P<action>BAN|UNBAN)\s+"
            r"\[Email] = (?P<email>[\w.-]+)\s+"
            r"\[IP] = (?P<client_ip>[\d.]+)"
            r"(?: banned for (?P<duration>\d+) seconds)?"
        )

    def add_cases(self, cases: ILogCase[BanLogRecord]) -> None:
        self._cases.append(cases)

    def match(self, line: str) -> re.Match[str] | None:
        return self._PATTERN.search(line)

    async def run(self, match: re.Match) -> None:
        for case in self._cases:
            try:
                await case.execute(self._dto_factory(match))
            except Exception as exc:
                logger.error(exc, exc_info=True)

    def _dto_factory(self, match: re.Match) -> BanLogRecord:
        raw = match.groupdict()
        return BanLogRecord(
            timestamp=datetime.strptime(raw["timestamp"], "%Y/%m/%d %H:%M:%S"),
            action=raw["action"],
            email=raw["email"],
            client_ip=raw["client_ip"],
            duration=int(raw["duration"]) if raw.get("duration") else None,
        )

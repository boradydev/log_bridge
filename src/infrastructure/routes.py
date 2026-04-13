import logging
import re
from datetime import datetime

from src.application.abcs import ILogCase, ILogger
from src.application.dtos import BanLogRecord
from src.presentation.ban_log_dispatcher.abcs import IRoute


class BannedLogRoute(IRoute):
    def __init__(self, logger: ILogger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self._cases: list[ILogCase[BanLogRecord]] = []
        self._PATTERN = re.compile(
            r"^"
            r"(?P<timestamp>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})\s+"
            r"(?P<action>BAN|UNBAN)\s+"
            r"\[Email\]\s*=\s*(?P<email>[^\s]+)\s+"
            r"\[IP\]\s*=\s*(?P<client_ip>\d{1,3}(?:\.\d{1,3}){3})"
            r".*?"
            r"\."
            r"$"
        )

    def add_cases(self, cases: ILogCase[BanLogRecord]) -> None:
        self._cases.append(cases)

    def match(self, line: str) -> re.Match[str] | None:
        return self._PATTERN.search(line)

    async def run(self, match: re.Match[str]) -> None:
        for case in self._cases:
            try:
                await case.execute(self._dto_factory(match))
            except Exception as exc:
                self._logger.error(exc, exc_info=True)

    def _dto_factory(self, match: re.Match[str]) -> BanLogRecord:
        raw = match.groupdict()
        return BanLogRecord(
            timestamp=datetime.strptime(raw["timestamp"], "%Y/%m/%d %H:%M:%S"),
            action=raw["action"],
            email=raw["email"],
            client_ip=raw["client_ip"],
        )

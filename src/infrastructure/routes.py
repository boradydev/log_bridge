import logging
from datetime import datetime
from typing import Final

from src.application.banned_log import vals
from src.application.banned_log.abcs import ILogCase, ILogger
from src.application.banned_log.dtos import BanLogRecord
from src.presentation.ban_log_dispatcher.abcs import IRoute


class BannedLogRoute(IRoute[BanLogRecord]):
    _TS_FORMAT: Final = "%Y/%m/%d_%H:%M:%S"

    def __init__(self, logger: ILogger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self._cases: list[ILogCase[BanLogRecord]] = []
        self._val_types = (
            vals.DateLog,
            vals.TimeLog,
            vals.ActionLog,
            vals.UserIDLog,
            vals.IPAddressLog,
        )

    def add_cases(self, cases: ILogCase[BanLogRecord]) -> None:
        self._cases.append(cases)

    def match(self, line: str) -> BanLogRecord | None:
        vo_map: dict[str, str] = {}
        tokens = line.split()

        for token in tokens:
            for vo_type in self._val_types:
                if vo_type.__name__ in vo_map:
                    continue

                if vo_type.is_valid(token):
                    vo_map[vo_type.__name__] = token
                    break

        if len(vo_map) == len(self._val_types):
            timestamp = vo_map["DateLog"] + "_" + vo_map["TimeLog"]
            return BanLogRecord(
                timestamp=datetime.strptime(timestamp, self._TS_FORMAT),
                action=vo_map["ActionLog"],
                email=vo_map["UserIDLog"],
                client_ip=vo_map["IPAddressLog"],
            )

        return None

    async def run(self, dto: BanLogRecord) -> None:
        for case in self._cases:
            try:
                await case.execute(dto)
            except Exception as exc:
                self._logger.error(exc, exc_info=True)

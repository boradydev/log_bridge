import logging
from datetime import datetime
from typing import Final

from src.application.banned_log import vals
from src.application.banned_log.abcs import ILogCase, ILogger
from src.application.banned_log.dtos import BanLogRecord
from src.presentation.ban_log_dispatcher.abcs import IRoute


class BannedLogRoute(IRoute):
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

    def extract(self, line: str) -> dict[str, str] | None:
        extracted_values: dict[str, str] = {}
        tokens = line.split()

        for token in tokens:
            for vo_type in self._val_types:
                if vo_type.__name__ in extracted_values:
                    continue

                if vo_type.is_valid(token):
                    extracted_values[vo_type.__name__] = token
                    break

        if len(extracted_values) == len(self._val_types):
            return extracted_values

        return None

    async def run(self, data: dict[str, str]) -> None:
        for case in self._cases:
            try:
                timestamp = (
                    data[vals.DateLog.__name__] + "_" + data[vals.TimeLog.__name__]
                )
                dto = BanLogRecord(
                    timestamp=datetime.strptime(timestamp, self._TS_FORMAT),
                    action=data[vals.ActionLog.__name__],
                    email=data[vals.UserIDLog.__name__],
                    client_ip=data[vals.IPAddressLog.__name__],
                )
                await case.execute(dto)
            except Exception as exc:
                self._logger.error(exc, exc_info=True)

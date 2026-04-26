import logging

from src.application.banned_log.abcs import ILogCase, ILogger
from src.application.banned_log.dtos import IBaseDTO
from src.presentation.ban_log_dispatcher.abcs import IRoute


class Route[DTO: IBaseDTO](IRoute):
    def __init__(
        self,
        dto_cls: type[DTO],
        logger: ILogger | None = None,
    ) -> None:
        self._dto_cls = dto_cls
        self._logger = logger or logging.getLogger(__name__)
        self._cases: list[ILogCase[DTO]] = []

    def add_case(self, case: ILogCase[DTO]) -> None:
        self._cases.append(case)

    def extract(self, line: str) -> dict[str, str] | None:
        return self._dto_cls.extract_fields(line)

    async def run(self, data: dict[str, str]) -> None:
        try:
            dto = self._dto_cls(**data)
            for case in self._cases:
                await case.execute(dto)
        except Exception as exc:
            self._logger.error(exc, exc_info=True)

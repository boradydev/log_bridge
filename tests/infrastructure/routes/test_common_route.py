import re
from dataclasses import dataclass
from typing import ClassVar

from src.application.common.dtos import IBaseDTO
from src.infrastructure.routes.common import Route


@dataclass(frozen=True, slots=True, kw_only=True)
class FakeDTO(IBaseDTO):
    value1: str
    value2: str
    value3: str
    value4: str
    value5: str

    _FIELD_PATTERNS: ClassVar[dict[str, re.Pattern[str]]] = {
        "value1": re.compile(r"^value1$"),
        "value2": re.compile(r"^value2$"),
        "value3": re.compile(r"^value3$"),
        "value4": re.compile(r"^value4$"),
        "value5": re.compile(r"^value5$"),
    }

    @classmethod
    def extract_fields(cls, line: str) -> dict[str, str] | None:
        extracted: dict[str, str] = {}
        tokens = line.split(
            maxsplit=len(cls._FIELD_PATTERNS),
            sep="$",
        )
        if len(tokens) < len(cls._FIELD_PATTERNS):
            return None

        field_names = cls._FIELD_PATTERNS.keys()
        for token, field in zip(tokens, field_names, strict=False):
            pattern = cls._FIELD_PATTERNS[field]
            if not pattern.fullmatch(token):
                return None
            extracted[field] = token

        return extracted


async def test_route(
    mock_first_case,
    mock_second_case,
    mock_logger,
) -> None:
    route = Route[FakeDTO](dto_cls=FakeDTO, logger=mock_logger)
    route.add_case(mock_first_case)
    route.add_case(mock_second_case)

    raw_line = "value1$value2$value3$value4$value5"
    data = FakeDTO.extract_fields(raw_line)
    dto = FakeDTO(**data)
    await route.run(data)

    mock_first_case.execute.assert_called_with(dto)
    mock_second_case.execute.assert_called_with(dto)

    invalid_data = {"value1": "value1", "value2": "value2"}
    await route.run(invalid_data)
    mock_logger.error.assert_called_once()

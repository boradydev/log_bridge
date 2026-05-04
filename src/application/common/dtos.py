import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class IBaseDTO(ABC):
    _FIELD_PATTERNS: ClassVar[dict[str, re.Pattern[str]]]

    @classmethod
    @abstractmethod
    def extract_fields(cls, line: str) -> dict[str, str] | None:
        raise NotImplementedError

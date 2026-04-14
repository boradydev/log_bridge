import re
from dataclasses import dataclass
from typing import ClassVar, Final

from src.application.banned_log import excs


@dataclass(frozen=True, slots=True)
class UserIDLog:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^[a-z0-9-]{5,50}$")

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogUserIDException

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls._PATTERN.fullmatch(value))


@dataclass(frozen=True, slots=True)
class DateLog:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^\d{4}/\d{2}/\d{2}$")

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogDateException

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls._PATTERN.fullmatch(value))


@dataclass(frozen=True, slots=True)
class TimeLog:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^\d{2}:\d{2}:\d{2}$")

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogTimeException

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls._PATTERN.fullmatch(value))


@dataclass(frozen=True, slots=True)
class ActionLog:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^BAN|^UNBAN$")

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogActionException

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls._PATTERN.fullmatch(value))


@dataclass(frozen=True, slots=True)
class IPAddressLog:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(
        r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    )

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogIPAddressException

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls._PATTERN.fullmatch(value))


@dataclass(frozen=True, slots=True)
class TagLog:
    value: str
    expected: ClassVar[str] = ""

    def __post_init__(self):
        if self.value != self.expected:
            raise excs.InvalidLogTagException(
                f"Expected {self.expected}, got {self.value}"
            )

    def __str__(self) -> str:
        return self.value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value == cls.expected


@dataclass(frozen=True, slots=True)
class EmailTagLog(TagLog):
    expected: ClassVar[str] = "[Email]"


@dataclass(frozen=True, slots=True)
class IPTagLog(TagLog):
    expected: ClassVar[str] = "[IP]"


@dataclass(frozen=True, slots=True)
class EqualsTagLog(TagLog):
    expected: ClassVar[str] = "="

import re
from dataclasses import dataclass
from typing import ClassVar, Final

from src.application.banned_log import excs


@dataclass(frozen=True, slots=True)
class LogUserID:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^[a-z0-9-]{5,50}$")

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogUserIDException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class LogDate:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^\d{4}/\d{2}/\d{2}$")

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogDateException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class LogTime:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^\d{2}:\d{2}:\d{2}$")

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogTimeException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class LogAction:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^BAN|^UNBAN$")

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogActionException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class LogIPAddress:
    value: str

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(
        r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    )

    def __post_init__(self):
        if not self._PATTERN.match(self.value):
            raise excs.InvalidLogIPAddressException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class LogTag:
    value: str
    expected: ClassVar[str] = ""

    def __post_init__(self):
        if self.value != self.expected:
            raise excs.InvalidLogTagException(
                f"Expected {self.expected}, got {self.value}"
            )


@dataclass(frozen=True, slots=True)
class EmailLogTag(LogTag):
    expected: ClassVar[str] = "[Email]"


@dataclass(frozen=True, slots=True)
class IPLogTag(LogTag):
    expected: ClassVar[str] = "[IP]"


@dataclass(frozen=True, slots=True)
class EqualsLogTag(LogTag):
    expected: ClassVar[str] = "="

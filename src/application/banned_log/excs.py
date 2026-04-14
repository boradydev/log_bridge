from dataclasses import dataclass

from src.core.excs import BaseAppException


@dataclass(frozen=True, slots=True)
class InvalidLogUserIDException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidLogDateException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidLogTimeException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidLogActionException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidLogIPAddressException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidLogTagException(BaseAppException):
    pass

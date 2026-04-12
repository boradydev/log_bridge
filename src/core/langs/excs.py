from dataclasses import dataclass

from src.core.excs import BaseAppException


@dataclass(slots=True, frozen=True)
class FluentBundleNotFound(BaseAppException):
    pass


@dataclass(slots=True, frozen=True)
class MessageToBundleNotFound(BaseAppException):
    pass


@dataclass(slots=True, frozen=True)
class FileFtlNotFound(BaseAppException):
    pass

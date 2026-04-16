import re
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class IFileLog(ABC):
    @abstractmethod
    def get_line(self) -> AsyncIterator[str]:
        raise NotImplementedError


class IRoute(ABC):
    @abstractmethod
    async def run(self, data: dict[str, str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def extract(self, line: str) -> dict[str, str] | None:
        raise NotImplementedError


class IDispatcher(ABC):
    @abstractmethod
    def add_route(self, route: IRoute):
        raise NotImplementedError

    @abstractmethod
    async def run(self) -> None:
        raise NotImplementedError


class INotifier(ABC):
    @abstractmethod
    async def send_message(self, message: str) -> None:
        raise NotImplementedError

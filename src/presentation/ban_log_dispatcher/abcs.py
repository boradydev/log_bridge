import re
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class IFileLog(ABC):
    @abstractmethod
    def get_line(self) -> AsyncIterator[str]:
        raise NotImplementedError


class IRoute[DTO](ABC):
    @abstractmethod
    async def run(self, dto: DTO) -> None:
        raise NotImplementedError

    @abstractmethod
    def match(self, line: str) -> DTO | None:
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

from abc import ABC, abstractmethod


class ILogCase[DTO](ABC):
    @abstractmethod
    async def execute(self, dto: DTO) -> None:
        raise NotImplementedError


class ITelegramLogMessage[DTO](ABC):
    @abstractmethod
    def get(self, dto: DTO) -> str:
        raise NotImplementedError

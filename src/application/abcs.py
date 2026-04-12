from abc import ABC, abstractmethod


class ILogCase[DTO](ABC):
    @abstractmethod
    async def execute(self, dto: DTO) -> None:
        raise NotImplementedError

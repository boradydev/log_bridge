import asyncio
from typing import Any

from src.presentation.ban_log_dispatcher.abcs import IDispatcher, IFileLog, IRoute


class Dispatcher(IDispatcher):
    def __init__(self, logs: IFileLog):
        self.logs = logs
        self.routes: list[IRoute[Any]] = []

    def add_route(self, route: IRoute[Any]):
        self.routes.append(route)

    async def run(self) -> None:
        async for line in self.logs.get_line():
            for route in self.routes:
                dto = route.match(line)
                if dto is not None:
                    asyncio.create_task(route.run(dto))

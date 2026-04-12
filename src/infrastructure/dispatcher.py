import asyncio

from src.presentation.ban_log_dispatcher.abcs import IDispatcher, IFileLog, IRoute


class Dispatcher(IDispatcher):
    def __init__(self, logs: IFileLog):
        self.logs = logs
        self.routes: list[IRoute] = []

    def add_route(self, route: IRoute):
        self.routes.append(route)

    async def run(self) -> None:
        async for line in self.logs.get_line():
            for route in self.routes:
                match = route.match(line)
                if match:
                    asyncio.create_task(route.run(match))

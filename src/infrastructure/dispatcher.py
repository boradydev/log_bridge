import asyncio
import logging
from logging import Logger

from src.presentation.ban_log_dispatcher.abcs import IDispatcher, IFileLog, IRoute


class Dispatcher(IDispatcher):
    def __init__(
        self,
        logs: IFileLog,
        logger: Logger | None = None,
    ):
        self._logger = logger or logging.getLogger(__name__)
        self.logs = logs
        self.routes: list[IRoute] = []

    def add_route(self, route: IRoute):
        self.routes.append(route)

    async def run(self) -> None:
        async for line in self.logs.get_line():
            is_handled = False

            for route in self.routes:
                data = route.extract(line)
                if data is not None:
                    asyncio.create_task(route.run(data))
                    is_handled = True

            if not is_handled:
                self._logger.warning(f"No route found for line: {line=}")

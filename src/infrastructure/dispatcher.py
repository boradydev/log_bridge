import asyncio
import logging
from collections.abc import Callable, Coroutine
from logging import Logger
from typing import Any

from src.presentation.ban_log_dispatcher.abcs import IDispatcher, ILogFile, IRoute


class Dispatcher(IDispatcher):
    _NO_ROUTE_MSG = "No route found for line {line!r} in file://{file_path}"
    _START_MSG = "The dispatcher is started. file://{file_path}"

    def __init__(
        self,
        logs: ILogFile,
        create_task: Callable[[Coroutine[Any, Any, Any]], Any] | None = None,
        logger: Logger | None = None,
    ):
        self.logs = logs
        self._create_task = create_task or asyncio.create_task
        self._logger = logger or logging.getLogger(__name__)
        self.routes: list[IRoute] = []

    def add_route(self, route: IRoute):
        self.routes.append(route)

    async def run(self) -> None:
        self._logger.info(self._START_MSG.format(file_path=self.logs.file_path))
        async for raw_line in self.logs.get_line():
            line = raw_line.strip()
            if not line:
                continue

            is_handled = False
            for route in self.routes:
                data = route.extract(line)
                if data is not None:
                    self._create_task(route.run(data))
                    is_handled = True

            if not is_handled:
                self._logger.warning(
                    self._NO_ROUTE_MSG.format(line=line, file_path=self.logs.file_path)
                )

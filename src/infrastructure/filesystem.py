import asyncio
import logging
import os
from collections.abc import AsyncIterator

import aiofiles

from src.presentation.ban_log_dispatcher.abcs import ILogFile


class LogFile(ILogFile):
    _SKIP_LINE_MSG = (
        "Skipped oversized line in file://{file_path}, "
        "total_skipped_size={total_skipped_size}"
    )
    _SKIP_PATTERN = {"\n", "\r", "\r\n", "\n\r", ""}

    def __init__(
        self,
        file_path: str,
        max_chunk_size: int = 1000,
        logger: logging.Logger | None = None,
    ) -> None:
        self._file_path = file_path
        self._max_chunk_size = max_chunk_size
        self._logger = logger or logging.getLogger(__name__)

    @property
    def file_path(self) -> str:
        return self._file_path

    async def get_line(self) -> AsyncIterator[str]:
        async with aiofiles.open(self._file_path) as file:
            await file.seek(0, os.SEEK_END)

            while True:
                line = await file.readline(self._max_chunk_size)
                if line in self._SKIP_PATTERN:
                    await asyncio.sleep(0.5)
                    continue

                if not line.endswith("\n"):
                    total_skipped_size = len(line)
                    while not line.endswith("\n"):
                        line = await file.readline(self._max_chunk_size)
                        if not line:
                            break

                        total_skipped_size += len(line)

                    self._logger.warning(
                        self._SKIP_LINE_MSG.format(
                            file_path=self._file_path,
                            total_skipped_size=total_skipped_size,
                        )
                    )
                    continue

                yield line

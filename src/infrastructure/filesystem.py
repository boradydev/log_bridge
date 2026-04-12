import asyncio
import os
from collections.abc import AsyncIterator

import aiofiles

from src.presentation.ban_log_dispatcher.abcs import IFileLog


class LogFile(IFileLog):
    def __init__(
        self,
        file_path: str,
    ) -> None:
        self.file_path = file_path

    async def get_line(self) -> AsyncIterator[str]:
        async with aiofiles.open(self.file_path) as file:
            await file.seek(0, os.SEEK_END)

            while True:
                line = await file.readline()
                if not line:
                    await asyncio.sleep(0.5)
                    continue

                yield line

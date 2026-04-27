import asyncio
from pathlib import Path
from typing import Callable, Coroutine, Any

import aiofiles
import pytest


@pytest.fixture
def file_path(tmp_path) -> Path:
    file_path = tmp_path / "test.log"
    file_path.touch()
    return file_path


@pytest.fixture
def writer(file_path) -> Callable[[list[str]], Coroutine[Any, Any, None]]:
    async def _writer(expected_lines: list[str]) -> None:
        async with aiofiles.open(file_path, mode="a") as file:
            for line in expected_lines:
                await file.write(line)
                await file.flush()
                await asyncio.sleep(0.01)

    return _writer

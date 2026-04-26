import asyncio
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import aiofiles
import pytest

from src.presentation.ban_log_dispatcher.abcs import ILogFile, IRoute


@pytest.fixture
def mock_log_file() -> AsyncMock | ILogFile:
    return MagicMock(spec_set=ILogFile)


@pytest.fixture
def mock_first_route() -> AsyncMock | IRoute:
    return MagicMock(spec_set=IRoute)


@pytest.fixture
def mock_second_route() -> AsyncMock | IRoute:
    return MagicMock(spec_set=IRoute)


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

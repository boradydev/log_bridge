import asyncio

import aiofiles
import pytest

from src.infrastructure.filesystem import LogFile  # проверь путь


async def test_log_file_reads_dynamic_lines(tmp_path):
    file_path = tmp_path / "test.log"
    file_path.touch()

    log_reader = LogFile(str(file_path))
    expected_lines: list[str] = [f"line_{i}\n" for i in range(100)]
    received_lines: list[str] = []

    async def writer() -> None:
        async with aiofiles.open(file_path, mode="a") as f:
            for line in expected_lines:
                await f.write(line)
                await f.flush()
                await asyncio.sleep(0.01)

    async def reader() -> None:
        async for line in log_reader.get_line():
            received_lines.append(line)
            if len(received_lines) == len(expected_lines):
                break

    try:
        await asyncio.wait_for(
            asyncio.gather(
                writer(),
                reader(),
            ),
            timeout=5.0,
        )
    except TimeoutError:
        pytest.fail(f"Time out, last: {received_lines[-1]}")

    assert received_lines == expected_lines

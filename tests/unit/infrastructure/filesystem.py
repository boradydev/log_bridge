import asyncio

import pytest

from src.infrastructure.filesystem import LogFile


async def test_log_file_reads_dynamic_lines(
    file_path,
    writer,
) -> None:
    log_reader = LogFile(str(file_path))
    expected_lines: list[str] = [f"line_{i}\n" for i in range(100)]
    received_lines: list[str] = []

    async def reader() -> None:
        async for line in log_reader.get_line():
            received_lines.append(line)
            if len(received_lines) == len(expected_lines):
                break

    try:
        await asyncio.wait_for(
            asyncio.gather(
                writer(expected_lines),
                reader(),
            ),
            timeout=5.0,
        )
    except TimeoutError:
        pytest.fail(f"Time out, last: {received_lines[-1]}")

    assert received_lines == expected_lines


async def test_log_file_manual(
    file_path,
    writer,
    mock_logger,
):
    skip_line = "line_over_max_chunk_size\n"
    expected_lines = [
        "line_1\n",
        skip_line,
        "line_3\n",
        "\n",
        "",
        "line_5\n",
        # "line_6\n",
    ]
    log_file = LogFile(
        str(file_path),
        max_chunk_size=10,
        logger=mock_logger,
    )

    received_lines = {
        "line_1\n",
        "line_3\n",
        "line_5\n",
    }

    async def reader() -> None:
        async for line in log_file.get_line():
            assert line in received_lines
            received_lines.discard(line)
            if not received_lines:
                break

        assert not received_lines
        mock_logger.warning.assert_called_once_with(
            log_file._SKIP_LINE_MSG.format(
                file_path=file_path,
                total_skipped_size=len(skip_line),
            )
        )

    try:
        await asyncio.wait_for(
            asyncio.gather(
                writer(expected_lines),
                reader(),
            ),
            timeout=5.0,
        )
    except TimeoutError:
        pytest.fail(f"Time out, last: {received_lines}")

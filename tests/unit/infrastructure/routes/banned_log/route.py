from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.banned_log.dtos import BanLogRecord
from src.infrastructure.routes import BannedLogRoute


async def test_banned_log_route_success(
    banned_route: BannedLogRoute,
    mock_log_case: AsyncMock,
) -> None:
    line = (
        "2026/04/05 10:36:46   BAN   [Email] = test@test.test  "
        "[IP] = 124.464.463.13 banned for 60 seconds."
    )
    expected_timestamp = datetime.strptime("2026/04/05 10:36:46", "%Y/%m/%d %H:%M:%S")

    match = banned_route.extract(line)
    assert match is not None, f"Failed to parse string: {line}"

    await banned_route.run(match)

    mock_log_case.execute.assert_awaited_once()

    call_args = mock_log_case.execute.call_args.args
    dto: BanLogRecord = call_args[0]

    assert isinstance(dto, BanLogRecord)
    assert dto.timestamp == expected_timestamp
    assert dto.action == "BAN"
    assert dto.email == "test@test.test"
    assert dto.client_ip == "124.464.463.13"


@pytest.mark.parametrize(
    ("log_line", "expected"),
    [
        (
            "2026/04/05 10:36:46   BAN   [Email] = test@test.test  "
            "[IP] = 124.464.463.13 banned for 60 seconds.",
            {
                "timestamp": "2026/04/05 10:36:46",
                "action": "BAN",
                "email": "test@test.test",
                "client_ip": "124.464.463.13",
            },
        ),
        (
            "2026/04/05 10:37:45   UNBAN   [Email] = test@test.test  "
            "[IP] = 124.464.463.13 unbanned.",
            {
                "timestamp": "2026/04/05 10:37:45",
                "action": "UNBAN",
                "email": "test@test.test",
                "client_ip": "124.464.463.13",
            },
        ),
    ],
)
def test_banned_log_route_regex_matching(
    log_line: str,
    expected: dict[str, str],
) -> None:
    route = BannedLogRoute()
    match = route._PATTERN.search(log_line)

    assert match is not None, f"Failed to parse string: {log_line}"

    groups = match.groupdict()

    assert groups["timestamp"] == expected["timestamp"]
    assert groups["action"] == expected["action"]
    assert groups["email"] == expected["email"]
    assert groups["client_ip"] == expected["client_ip"]


def test_banned_log_route_dto_factory() -> None:
    route = BannedLogRoute()

    line = (
        "2026/04/05 10:36:46   BAN   [Email] = test@test.test  "
        "[IP] = 124.464.463.13 banned for 60 seconds."
    )

    match = route.extract(line)
    assert match is not None

    dto = route._dto_factory(match)

    assert dto.timestamp == datetime(2026, 4, 5, 10, 36, 46)
    assert dto.action == "BAN"
    assert dto.email == "test@test.test"
    assert dto.client_ip == "124.464.463.13"


async def test_run_should_be_resilient_to_case_failures(
    banned_route: BannedLogRoute,
    mock_logger: MagicMock,
    mock_log_case_fail: AsyncMock,
    mock_log_case_success: AsyncMock,
) -> None:
    banned_route.add_cases(mock_log_case_fail)
    banned_route.add_cases(mock_log_case_success)

    line = (
        "2026/04/05 10:36:46   BAN   [Email] = test@test.test  "
        "[IP] = 124.464.463.13 banned for 60 seconds."
    )

    match = banned_route.extract(line)
    if match is None:
        raise AssertionError("Failed to match line")

    await banned_route.run(match)

    mock_logger.error.assert_called_once()

    args, kwargs = mock_logger.error.call_args
    error_text = str(args[0])
    assert "Domain logic error" in error_text
    assert kwargs["exc_info"] is True

    mock_log_case_fail.execute.assert_awaited_once()
    mock_log_case_success.execute.assert_awaited_once()

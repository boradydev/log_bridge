from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.abcs import ILogger
from src.infrastructure.routes import BannedLogRoute


@pytest.fixture
def mock_log_case() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_logger() -> MagicMock | ILogger:
    return MagicMock(spec_set=ILogger)


@pytest.fixture
def banned_route(
    mock_logger: MagicMock,
    mock_log_case: AsyncMock,
) -> BannedLogRoute:
    route = BannedLogRoute(logger=mock_logger)
    route.add_cases(mock_log_case)
    return route


@pytest.fixture
def mock_log_case_fail() -> AsyncMock:
    mock = AsyncMock()
    mock.execute.side_effect = Exception("Domain logic error")
    return mock


@pytest.fixture
def mock_log_case_success() -> AsyncMock:
    return AsyncMock()

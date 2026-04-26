from unittest.mock import AsyncMock

import pytest

from src.application.banned_log.abcs import ILogCase


@pytest.fixture
def mock_first_case() -> AsyncMock | ILogCase:
    return AsyncMock(spec_set=ILogCase)


@pytest.fixture
def mock_second_case() -> AsyncMock | ILogCase:
    return AsyncMock(spec_set=ILogCase)

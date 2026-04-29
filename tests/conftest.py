from unittest.mock import MagicMock

import pytest

from src.application.common.abcs import ILogger


@pytest.fixture
def mock_logger() -> MagicMock | ILogger:
    return MagicMock(spec_set=ILogger)

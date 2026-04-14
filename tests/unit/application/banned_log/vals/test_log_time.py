import pytest

from src.application.banned_log import excs
from src.application.banned_log.vals import TimeLog


@pytest.mark.parametrize(
    "valid",
    [
        "10:36:46",
        "10:34:46",
        "11:36:42",
    ],
)
async def test_positive(valid: str) -> None:
    instance = TimeLog(valid)
    assert str(instance) == valid


@pytest.mark.parametrize(
    "invalid",
    [
        "10:36:463",
        "103:36:46",
        "10:362:46",
        "10:36,46",
        "10-34:46",
        "11:36",
    ],
)
async def test_negative(invalid: str) -> None:
    with pytest.raises(excs.InvalidLogTimeException):
        TimeLog(invalid)

import pytest

from src.application.banned_log import excs
from src.application.banned_log.vals import ActionLog


@pytest.mark.parametrize(
    "valid",
    [
        "BAN",
        "UNBAN",
    ],
)
async def test_positive(valid: str) -> None:
    instance = ActionLog(valid)
    assert str(instance) == valid


@pytest.mark.parametrize(
    "invalid",
    [
        "ban",
        "unban",
        "cation",
        "",
    ],
)
async def test_negative(invalid: str) -> None:
    with pytest.raises(excs.InvalidLogActionException):
        ActionLog(invalid)

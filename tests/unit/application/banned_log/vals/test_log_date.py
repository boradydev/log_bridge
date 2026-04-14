import pytest

from src.application.banned_log import excs
from src.application.banned_log.vals import DateLog


@pytest.mark.parametrize(
    "valid",
    [
        "2026/04/04",
        "2026/04/24",
        "2026/02/03",
    ],
)
async def test_positive(valid: str) -> None:
    instance = DateLog(valid)
    assert str(instance) == valid


@pytest.mark.parametrize(
    "invalid",
    [
        "2026/04/043",
        "2026/104/24",
        "20264/02/03",
    ],
)
async def test_negative(invalid: str) -> None:
    with pytest.raises(excs.InvalidLogDateException):
        DateLog(invalid)

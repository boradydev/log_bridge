from dataclasses import dataclass
from typing import ClassVar

import pytest

from src.application.banned_log import excs
from src.application.banned_log.vals import LogTag


@dataclass(frozen=True, slots=True)
class MockLogTag(LogTag):
    expected: ClassVar[str] = "valid"


async def test_positive() -> None:
    assert MockLogTag("valid")


async def test_negative() -> None:
    with pytest.raises(excs.InvalidLogTagException):
        MockLogTag("invalid")

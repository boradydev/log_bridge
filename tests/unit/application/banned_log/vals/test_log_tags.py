from dataclasses import dataclass
from typing import ClassVar

import pytest

from src.application.banned_log import excs
from src.application.banned_log.vals import TagLog


@dataclass(frozen=True, slots=True)
class MockTagLog(TagLog):
    expected: ClassVar[str] = "valid"


async def test_positive() -> None:
    assert MockTagLog("valid")


async def test_negative() -> None:
    with pytest.raises(excs.InvalidLogTagException):
        MockTagLog("invalid")

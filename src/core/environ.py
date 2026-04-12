import os
from collections.abc import Callable
from dataclasses import field
from typing import Any, TypeVar


T = TypeVar("T")


def env_field[T](
    cast_type: Callable[[Any], T],
    key: str,
) -> T:
    return field(default_factory=lambda: cast_type(os.environ[key]))

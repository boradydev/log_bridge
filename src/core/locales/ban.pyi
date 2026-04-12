# mypy: ignore-errors
# This is auto-generated file, do not edit!
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Literal

from aiogram_i18n import LazyProxy

class I18nContext(I18nStub):
    def get(self, key: str, /, **kwargs: Any) -> str: ...
    async def set_locale(self, locale: str, **kwargs: Any) -> None: ...
    @contextmanager
    def use_locale(self, locale: str) -> Generator[I18nContext]: ...
    @contextmanager
    def use_context(self, **kwargs: Any) -> Generator[I18nContext]: ...
    def set_context(self, **kwargs: Any) -> None: ...

class LazyFactory(I18nStub):
    key_separator: str

    def set_separator(self, key_separator: str) -> None: ...
    def __call__(self, key: str, /, **kwargs: dict[str, Any]) -> LazyProxy: ...

L: LazyFactory

class I18nStub:
    @staticmethod
    def BAN(
        *, email: Any, duration: Any, client_ip: Any, **kwargs: Any
    ) -> Literal["🚫 Banned { $email } for {...}. Client IP: { $client_ip }"]: ...
    @staticmethod
    def UNBAN(
        *, email: Any, client_ip: Any, **kwargs: Any
    ) -> Literal["✅ Unbanned { $email }. Client IP: { $client_ip }"]: ...

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
    def auth_failure(
        *, hostname: Any, user: Any, client_ip: Any, **kwargs: Any
    ) -> Literal[
        "🚫 { $hostname }: Auth failure for { $user } from { $client_ip }"
    ]: ...
    @staticmethod
    def disconnect(
        *, hostname: Any, user: Any, client_ip: Any, **kwargs: Any
    ) -> Literal["ℹ️ { $hostname }: { $user } disconnected ({ $client_ip })"]: ...
    @staticmethod
    def invalid_user(
        *, hostname: Any, client_ip: Any, **kwargs: Any
    ) -> Literal["⚠️ { $hostname }: Invalid user login attempt from { $client_ip }"]: ...
    @staticmethod
    def success(
        *, hostname: Any, user: Any, client_ip: Any, **kwargs: Any
    ) -> Literal["✅ { $hostname }: { $user } logged in from { $client_ip }"]: ...

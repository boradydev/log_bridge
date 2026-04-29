from dataclasses import dataclass

from src.core.environ import environ, environ_get


@dataclass(frozen=True, slots=True)
class TelegramSettings:
    BOT_TOKEN: str = environ(str, "BOT_TOKEN")
    CHAT_ID: str = environ(str, "CHAT_ID")
    HTTP_PROXY: str | None = environ_get(str, "HTTP_PROXY")

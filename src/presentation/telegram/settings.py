from dataclasses import dataclass

from src.core.environ import env_field


@dataclass(frozen=True, slots=True)
class TelegramSettings:
    BOT_TOKEN: str = env_field(str, "BOT_TOKEN")
    CHAT_ID: str = env_field(str, "CHAT_ID")
from dataclasses import dataclass

from src.core.environ import environ_get


@dataclass(frozen=True, slots=True)
class AppSettings:
    DEBUG_MODE: str | None = environ_get(str, "DEBUG_MODE")
    BANNED_LOG_PATH: str | None = environ_get(str, "BANNED_LOG_PATH")
    AUTH_LOG_PATH: str | None = environ_get(str, "AUTH_LOG_PATH")

    @property
    def debug(self) -> bool:
        if self.DEBUG_MODE is None:
            return False

        return self.DEBUG_MODE.lower() == "true"

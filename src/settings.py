from dataclasses import dataclass

from src.core.environ import environ


@dataclass(frozen=True, slots=True)
class AppSettings:
    APP_ENV: str = environ(str, "APP_ENV")
    BANNED_LOG_PATH: str = environ(str, "BANNED_LOG_PATH")

    @property
    def debug(self) -> bool:
        return self.APP_ENV == "dev"

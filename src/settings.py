from dataclasses import dataclass

from src.core.environ import environ


@dataclass(frozen=True, slots=True)
class AppSettings:
    APP_ENV: str = environ(str, "APP_ENV")

    @property
    def debug(self) -> bool:
        return self.APP_ENV == "dev"

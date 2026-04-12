from dataclasses import dataclass

from src.core.environ import env_field


@dataclass(slots=True)
class LangSettings:
    lang: str = "en"

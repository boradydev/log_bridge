import re
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from src.application.common.dtos import IBaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class BanLogRecordDTO(IBaseDTO):
    date: str
    time: str
    action: str
    _email_tag: str
    _equal_email: str
    email: str
    _ip_tag: str
    _equal_ip: str
    client_ip: str

    _FIELD_PATTERNS: ClassVar[dict[str, re.Pattern[str]]] = {
        "date": re.compile(r"^\d{4}/\d{2}/\d{2}$"),
        "time": re.compile(r"^\d{2}:\d{2}:\d{2}$"),
        "action": re.compile(r"^BAN|^UNBAN$"),
        "_email_tag": re.compile(r"^\[Email]$"),
        "_equal_email": re.compile(r"^=$"),
        "email": re.compile(r"^[a-z0-9-]{5,50}$"),
        "_ip_tag": re.compile(r"^\[IP]$"),
        "_equal_ip": re.compile(r"^=$"),
        "client_ip": re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    }

    @property
    def timestamp(self) -> datetime:
        return datetime.strptime(
            f"{self.date}_{self.time}",
            "%Y/%m/%d_%H:%M:%S",
        )

    @classmethod
    def extract_fields(cls, line: str) -> dict[str, str] | None:
        extracted: dict[str, str] = {}
        tokens = line.split(maxsplit=len(cls._FIELD_PATTERNS))
        if len(tokens) < len(cls._FIELD_PATTERNS):
            return None

        field_names = cls._FIELD_PATTERNS.keys()
        for token, field in zip(tokens, field_names, strict=False):
            pattern = cls._FIELD_PATTERNS[field]
            if not pattern.fullmatch(token):
                return None
            extracted[field] = token

        return extracted

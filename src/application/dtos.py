from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class BanLogRecord:
    timestamp: datetime
    action: str
    email: str
    client_ip: str

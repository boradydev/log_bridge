import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar

from src.application.auth_log.excs import InvalidLineSSHLogException
from src.application.common.dtos import IBaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class SSHLogRecordDTO(IBaseDTO):
    hostname: str
    action: str
    user: str
    client_ip: str
    timestamp: datetime = field(default_factory=datetime.now, init=False)

    _FIELD_PATTERNS: ClassVar[dict[str, re.Pattern[str]]] = {
        "user": re.compile(r"^\S{1,64}$"),
        "client_ip": re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"),
    }

    _find_actions = [
        "Accepted publickey for",
        "Disconnected from user",
        "Connection closed by invalid user",
        "Connection closed by authenticating user",
    ]

    @classmethod
    def extract_fields(cls, line: str) -> dict[str, str] | None:
        """
        Index content.

        0 "Apr"
        1 "29"
        2 "12:23:37"
        3 "r5645656"
        4 "sshd[139630]:"
        5 "Accepted publickey for root from 24.14.233.31 ..."
          "Disconnected from user root 67.159.244.31 ..."
          "Connection closed by invalid user attacker from 67.159.244.31 ..."
          "Connection closed by authenticating user root 67.159.244.31 ..."
        """
        tokens = line.split(maxsplit=5)
        if len(tokens) < 6 or not tokens[4].startswith("sshd"):
            return None

        content = tokens[5]
        for action in cls._find_actions:
            if action in content:
                content_tokens = content.replace(action, "").split()
                token_iterator = iter(content_tokens)

                extracted: dict[str, str] = {
                    "hostname": tokens[3],
                    "action": action,
                }

                for key, pattern in cls._FIELD_PATTERNS.items():
                    found = False
                    for token in token_iterator:
                        if pattern.fullmatch(token):
                            extracted[key] = token
                            found = True
                            break

                    if not found:
                        raise InvalidLineSSHLogException(line)

                return extracted

        return None

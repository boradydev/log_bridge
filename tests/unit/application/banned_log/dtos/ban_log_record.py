import pytest

from src.application.banned_log.dtos import BanLogRecord


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "2026/04/05 10:36:46   BAN   [Email] = user-123456  "
            "[IP] = 124.464.463.13 banned for 60 seconds.",
            {
                "date": "2026/04/05",
                "time": "10:36:46",
                "action": "BAN",
                "_email_tag": "[Email]",
                "_equal_email": "=",
                "email": "user-123456",
                "_ip_tag": "[IP]",
                "_equal_ip": "=",
                "client_ip": "124.464.463.13",
            },
        ),
        (
            "2026/04/05 10:37:45   UNBAN   [Email] = user-123456  "
            "[IP] = 124.464.463.13 unbanned.",
            {
                "date": "2026/04/05",
                "time": "10:37:45",
                "action": "UNBAN",
                "_email_tag": "[Email]",
                "_equal_email": "=",
                "email": "user-123456",
                "_ip_tag": "[IP]",
                "_equal_ip": "=",
                "client_ip": "124.464.463.13",
            },
        ),
    ],
)
def test_ban_log_record_success(
    line,
    expected,
) -> None:
    fields = BanLogRecord.FIELD_PATTERNS.keys()
    tokens = line.split()
    data = {}
    for token, field in zip(tokens, fields, strict=False):
        if not BanLogRecord.FIELD_PATTERNS[field].fullmatch(token):
            raise ValueError(f"Failed to parse string: {token}")

        data[field] = token

    assert data == expected
    assert BanLogRecord(**data)


def test_fields_unsuccess() -> None:
    assert not BanLogRecord.FIELD_PATTERNS["date"].fullmatch("2026/04/055")
    assert not BanLogRecord.FIELD_PATTERNS["time"].fullmatch("10:36:464")
    assert not BanLogRecord.FIELD_PATTERNS["action"].fullmatch("BANNED")
    assert not BanLogRecord.FIELD_PATTERNS["email"].fullmatch("user-123456%")
    assert not BanLogRecord.FIELD_PATTERNS["client_ip"].fullmatch("1244.464.463.13")
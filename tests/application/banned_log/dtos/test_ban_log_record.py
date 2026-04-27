import pytest

from src.application.banned_log.dtos import BanLogRecordDTO


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
    data = BanLogRecordDTO.extract_fields(line)
    assert data == expected
    assert BanLogRecordDTO(**data)

@pytest.mark.parametrize(
    "line",
    [
        "2026/04/05 10:36:46   BANNED   [Email] = user-123456  "
        "[IP] = 124.464.463.13 banned for 60 seconds.",
        "2026/04/05 10:37:45   UNBANNED   [Email] = user-123456  "
        "[IP] = 124.464.463.13 unbanned.",
        "2026/04/05 10:37:45   UNBAN   [Email] = user-123456#%  "
        "[IP] = 124.464.463.13 unbanned.",
        "2026/504/05 10:37:45   UNBAN   [Email] = user-123456  "
        "[IP] = 124.464.463.13 unbanned.",
        ""
    ],
)
def test_ban_log_record_unsuccess(
    line
) -> None:
    data = BanLogRecordDTO.extract_fields(line)
    assert data is None


def test_fields_unsuccess() -> None:
    assert not BanLogRecordDTO._FIELD_PATTERNS["date"].fullmatch("2026/04/055")
    assert not BanLogRecordDTO._FIELD_PATTERNS["time"].fullmatch("10:36:464")
    assert not BanLogRecordDTO._FIELD_PATTERNS["action"].fullmatch("BANNED")
    assert not BanLogRecordDTO._FIELD_PATTERNS["email"].fullmatch("user-123456%")
    assert not BanLogRecordDTO._FIELD_PATTERNS["client_ip"].fullmatch("1244.464.463.13")

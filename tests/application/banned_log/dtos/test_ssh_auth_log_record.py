import pytest

from src.application.auth_log.dtos import SSHLogRecordDTO
from src.application.auth_log.excs import InvalidLineSSHLogException


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "Apr 30 08:24:58 r5645656 sshd[148704]:"
            " Accepted publickey for root from 24.14.233.31"
            " port 4288 ssh2: ED25519 SHA256:0C5BQ66dSEU5Zh...",
            {
                "hostname": "r5645656",
                "action": "Accepted publickey for",
                "user": "root",
                "client_ip": "24.14.233.31",
            },
        ),
        (
            "Apr 30 08:24:34 r5645656 sshd[148699]:"
            " Connection closed by invalid user attacker 67.159.244.31"
            " port 26565 [preauth]",
            {
                "hostname": "r5645656",
                "action": "Connection closed by invalid user",
                "user": "attacker",
                "client_ip": "67.159.244.31",
            },
        ),
        (
            "Apr 30 08:24:20 r5645656 sshd[148695]:"
            " Connection closed by authenticating user root 67.159.244.31"
            " port 26549 [preauth]",
            {
                "hostname": "r5645656",
                "action": "Connection closed by authenticating user",
                "user": "root",
                "client_ip": "67.159.244.31",
            },
        ),
        (
            "Apr 29 12:57:44 r5645656 sshd[139897]:"
            " Disconnected from user root 24.14.233.31 port 4294",
            {
                "hostname": "r5645656",
                "action": "Disconnected from user",
                "user": "root",
                "client_ip": "24.14.233.31",
            },
        ),
    ],
)
def test_ssh_auth_log_record_success(
    line,
    expected,
) -> None:
    data = SSHLogRecordDTO.extract_fields(line)
    assert data is not None
    assert data == expected
    assert SSHLogRecordDTO(**data)


@pytest.mark.parametrize(
    "line",
    [
        "Apr 30 06:51:06 r5645656 sshd[124875]: Received signal 15; terminating."
        "Apr 30 06:25:02 r5645656 CRON[147403]: pam_unix(cron:session):"
        " session closed for user root",
        "Apr 30 08:24:34 r5645656 sshd[148699]: Invalid data",
    ],
)
def test_ssh_auth_log_record_unsuccess(line) -> None:
    data = SSHLogRecordDTO.extract_fields(line)
    assert data is None


def test_fields_unsuccess() -> None:
    assert not SSHLogRecordDTO._FIELD_PATTERNS["user"].fullmatch("root" * 100)
    assert not SSHLogRecordDTO._FIELD_PATTERNS["client_ip"].fullmatch("1244.464.463.13")


@pytest.mark.parametrize(
    ("line", "exception"),
    [
        (
            "Apr 30 06:51:06 r5645656 sshd[124875]: Accepted publickey for root ...",
            InvalidLineSSHLogException,
        ),
    ],
)
def test_partial_invalid_string(line, exception) -> None:
    pytest.raises(exception, SSHLogRecordDTO.extract_fields, line)

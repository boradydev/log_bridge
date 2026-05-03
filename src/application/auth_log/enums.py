import enum


class SSHAuthEnum(str, enum.Enum):
    SUCCESS = "Accepted publickey for"
    DISCONNECT = "Disconnected from user"
    INVALID_USER = "Connection closed by invalid user"
    AUTH_FAILURE = "Connection closed by authenticating user"

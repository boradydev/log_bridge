import logging

from src.application.auth_log.dtos import SSHLogRecordDTO
from src.application.auth_log.enums import SSHAuthEnum
from src.application.common.abcs import ILogCase
from src.core.locales.stub.auth import I18nContext
from src.presentation.log_dispatchers.abcs import INotifier


class SSHAuthEventCase(ILogCase[SSHLogRecordDTO]):
    def __init__(
        self,
        notifier: INotifier,
        messages: I18nContext,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self._notifier = notifier
        self._messages = messages

    async def execute(self, dto: SSHLogRecordDTO) -> None:
        match dto.action:
            case SSHAuthEnum.SUCCESS:
                message = self._messages.success(
                    hostname=dto.hostname,
                    user=dto.user,
                    client_ip=dto.client_ip,
                )
            case SSHAuthEnum.DISCONNECT:
                message = self._messages.disconnect(
                    hostname=dto.hostname,
                    user=dto.user,
                    client_ip=dto.client_ip,
                )
            case SSHAuthEnum.INVALID_USER:
                message = self._messages.invalid_user(
                    hostname=dto.hostname,
                    client_ip=dto.client_ip,
                )
            case SSHAuthEnum.AUTH_FAILURE:
                message = self._messages.auth_failure(
                    hostname=dto.hostname,
                    user=dto.user,
                    client_ip=dto.client_ip,
                )
            case _:
                self._logger.warning(f"Unknown action: {dto.action}")
                return
        await self._notifier.send_message(message)

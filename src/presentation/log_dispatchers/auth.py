from typing import cast

from aiogram_i18n import I18nContext, I18nMiddleware

from src.application.auth_log.cases import SSHAuthEventCase
from src.application.auth_log.dtos import SSHLogRecordDTO
from src.core.locales.stub.auth import I18nContext as AuthI18nContext
from src.infrastructure.dispatchers.common import Dispatcher
from src.infrastructure.filesystem import LogFile
from src.infrastructure.routes.common import Route
from src.presentation.log_dispatchers.abcs import INotifier


async def auth_log_launcher(
    notifier: INotifier,
    i18n_middleware: I18nMiddleware,
    logfile: LogFile,
) -> None:
    def build_i18n(ctx: I18nContext) -> AuthI18nContext:
        return cast(AuthI18nContext, ctx)

    i18n_ctx = i18n_middleware.new_context(locale="en", data={})
    banned_i18n = build_i18n(i18n_ctx)

    event_case = SSHAuthEventCase(
        notifier=notifier,
        messages=banned_i18n,
    )

    ssh_log_route = Route[SSHLogRecordDTO](SSHLogRecordDTO)
    ssh_log_route.add_case(event_case)

    dispatcher = Dispatcher(logfile)
    dispatcher.add_route(ssh_log_route)
    await dispatcher.run()

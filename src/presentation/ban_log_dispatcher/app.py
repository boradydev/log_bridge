from typing import TYPE_CHECKING

from src.application.banned_log.cases import BannedEventCase
from src.core.paths import PROJECT_DIR
from src.infrastructure.dispatcher import Dispatcher
from src.infrastructure.filesystem import LogFile
from src.infrastructure.routes import BannedLogRoute
from src.presentation.ban_log_dispatcher.abcs import INotifier


if TYPE_CHECKING:
    from src.core.locales.ban import I18nContext as I18n


async def log_dispatcher_app(
    notifier: INotifier,
    i18n: I18n,
) -> None:
    banned_event_case = BannedEventCase(
        notifier=notifier,
        messages=i18n,
    )

    banned_log_route = BannedLogRoute()
    banned_log_route.add_cases(banned_event_case)

    logfile = LogFile(str(PROJECT_DIR / "source/access.log"))

    dispatcher = Dispatcher(logfile)
    dispatcher.add_route(banned_log_route)

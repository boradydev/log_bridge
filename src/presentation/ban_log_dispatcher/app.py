import asyncio
import logging
from typing import cast

from aiogram_i18n import I18nContext, I18nMiddleware

from src.application.banned_log.cases import BannedEventCase
from src.application.banned_log.dtos import BanLogRecordDTO
from src.core.locales.stub.ban import I18nContext as BannedI18nContext
from src.core.paths import PROJECT_DIR
from src.infrastructure.dispatchers.common import Dispatcher
from src.infrastructure.filesystem import LogFile
from src.infrastructure.routes.common import Route
from src.presentation.ban_log_dispatcher.abcs import INotifier


async def log_dispatcher_app(
    notifier: INotifier,
    i18n_middleware: I18nMiddleware,
) -> None:
    logging.getLogger(__name__)

    def build_banned_i18n(ctx: I18nContext) -> BannedI18nContext:
        return cast(BannedI18nContext, ctx)

    i18n_ctx = i18n_middleware.new_context(locale="en", data={})
    banned_i18n = build_banned_i18n(i18n_ctx)

    banned_event_case = BannedEventCase(
        notifier=notifier,
        messages=banned_i18n,
    )

    banned_log_route = Route[BanLogRecordDTO](BanLogRecordDTO)
    banned_log_route.add_case(banned_event_case)

    logfile = LogFile(str(PROJECT_DIR / "source/banned.log"))

    dispatcher = Dispatcher(logfile)
    dispatcher.add_route(banned_log_route)
    try:
        await dispatcher.run()
    except asyncio.CancelledError:
        logging.info("Log dispatcher task was cancelled. Closing resources...")
    finally:
        await logfile.close()
        logging.info("Log dispatcher stopped.")


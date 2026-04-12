import asyncio
from typing import TYPE_CHECKING, cast

from aiogram import Bot
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from src.core.paths import PROJECT_DIR
from src.infrastructure.telegram.notifier import TelegramNotifier
from src.presentation.ban_log_dispatcher.app import log_dispatcher_app
from src.presentation.telegram.app import telegram_app
from src.presentation.telegram.settings import TelegramSettings


async def main() -> None:
    i18n_core = FluentRuntimeCore(
        path=PROJECT_DIR / "src/core/locales/{locale}",
        raise_key_error=True,
    )

    i18n_middleware = I18nMiddleware(
        core=i18n_core,
        default_locale="ru",
    )

    if TYPE_CHECKING:
        from src.core.locales.ban import I18nContext as I18n
    i18n = cast(I18n, i18n_middleware.new_context(locale="ru", data={}))

    telegram_settings = TelegramSettings()
    bot = Bot(token=telegram_settings.BOT_TOKEN)
    chat_ids = [telegram_settings.CHAT_ID]
    notifier = TelegramNotifier(
        bot=bot,
        chat_ids=chat_ids,
    )
    await asyncio.gather(
        log_dispatcher_app(
            i18n=i18n,
            notifier=notifier,
        ),
        telegram_app(
            bot=bot,
            i18n_middleware=i18n_middleware,
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())

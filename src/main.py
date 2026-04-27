import asyncio
import logging

import dotenv
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from src.core.paths import PROJECT_DIR
from src.infrastructure.telegram.notifier import TelegramNotifier
from src.presentation.ban_log_dispatcher.app import log_dispatcher_app
from src.presentation.telegram.app import telegram_app
from src.presentation.telegram.settings import TelegramSettings


async def main() -> None:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Starting application")
    dotenv.load_dotenv()

    i18n_core = FluentRuntimeCore(
        path=PROJECT_DIR / "src/core/locales/source/{locale}",
    )
    await i18n_core.startup()

    i18n_middleware = I18nMiddleware(
        core=i18n_core,
    )

    telegram_settings = TelegramSettings()
    session = AiohttpSession(proxy=telegram_settings.PROXY)
    bot = Bot(token=telegram_settings.BOT_TOKEN, session=session)
    chat_ids = [telegram_settings.CHAT_ID]
    notifier = TelegramNotifier(
        bot=bot,
        chat_ids=chat_ids,
    )
    try:
        await asyncio.gather(
            log_dispatcher_app(
                i18n_middleware=i18n_middleware,
                notifier=notifier,
            ),
            telegram_app(
                bot=bot,
                i18n_middleware=i18n_middleware,
            ),
        )
    except asyncio.CancelledError:
        logger.info("Stopping tasks...")
    finally:
        logger.info("Завершение в main")
        await bot.session.close()
        await i18n_core.shutdown()
        logger.info("Application stopped gracefully")


if __name__ == "__main__":
    asyncio.run(main())

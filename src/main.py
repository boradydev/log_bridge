import asyncio
import logging

import dotenv
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from src.core.paths import PROJECT_DIR
from src.infrastructure.filesystem import LogFile
from src.infrastructure.telegram.notifier import TelegramNotifier
from src.presentation.log_dispatchers.banned import banned_log_launcher
from src.presentation.telegram.dispatcher import dispatcher as telegram_dispatcher
from src.presentation.telegram.settings import TelegramSettings
from src.settings import AppSettings


async def main() -> None:
    dotenv.load_dotenv()
    app_settings = AppSettings()
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG if app_settings.debug else logging.INFO)
    logger.debug("Starting application")

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
    logfile = LogFile(str(PROJECT_DIR / "source/banned.log"))

    async def on_startup():
        asyncio.create_task(
            banned_log_launcher(
                i18n_middleware=i18n_middleware,
                notifier=notifier,
                logfile=logfile,
            )
        )
        logger.debug("Bot started")

    async def on_shutdown():
        await logfile.close()
        await bot.session.close()
        await i18n_core.shutdown()
        logger.debug("Bot stopped")

    telegram_dispatcher.startup.register(on_startup)
    telegram_dispatcher.shutdown.register(on_shutdown)

    i18n_middleware.setup(telegram_dispatcher)
    await telegram_dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

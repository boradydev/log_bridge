import asyncio
import logging

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.backoff import BackoffConfig
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from src.core.paths import PROJECT_DIR
from src.infrastructure.filesystem import LogFile
from src.infrastructure.telegram.notifier import TelegramNotifier
from src.presentation.log_dispatchers.auth import auth_log_launcher
from src.presentation.log_dispatchers.banned import banned_log_launcher
from src.presentation.telegram.dispatcher import (
    dispatcher as telegram_dispatcher,
)
from src.presentation.telegram.settings import TelegramSettings
from src.settings import AppSettings


async def telegram_app(app_settings: AppSettings) -> None:
    logger = logging.getLogger(__name__)
    i18n_core = FluentRuntimeCore(
        path=PROJECT_DIR / "src/core/locales/source/{locale}",
    )
    await i18n_core.startup()

    i18n_middleware = I18nMiddleware(
        core=i18n_core,
    )
    telegram_settings = TelegramSettings()
    session = AiohttpSession(
        proxy=telegram_settings.HTTP_PROXY,
    )
    bot = Bot(
        token=telegram_settings.BOT_TOKEN,
        session=session,
    )
    chat_ids = [telegram_settings.CHAT_ID]
    notifier = TelegramNotifier(
        bot=bot,
        chat_ids=chat_ids,
    )
    banned_logfile = (
        LogFile(app_settings.BANNED_LOG_PATH) if app_settings.BANNED_LOG_PATH else None
    )
    auth_logfile = (
        LogFile(app_settings.AUTH_LOG_PATH) if app_settings.AUTH_LOG_PATH else None
    )

    background_tasks = set()

    if banned_logfile:
        task = asyncio.create_task(
            banned_log_launcher(
                i18n_middleware=i18n_middleware,
                notifier=notifier,
                logfile=banned_logfile,
            )
        )
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    if auth_logfile:
        task = asyncio.create_task(
            auth_log_launcher(
                i18n_middleware=i18n_middleware,
                notifier=notifier,
                logfile=auth_logfile,
            )
        )
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    await notifier.send_message("Bot online")
    logger.info("Bot started and background tasks launched")

    retry_delay = 5
    while True:
        try:
            await telegram_dispatcher.start_polling(
                bot,
                handle_signals=False,
                backoff_config=BackoffConfig(
                    min_delay=1.0,
                    max_delay=60.0,
                    factor=1.5,
                    jitter=0.1,
                ),
            )
            break
        except Exception as exc:
            logger.error(f"Polling error: {exc}. Restarting in {retry_delay}s...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 120)
        finally:
            logger.info("Polling iteration finished")

    logger.info("Shutting down...")
    if banned_logfile:
        await banned_logfile.close()
    if auth_logfile:
        await auth_logfile.close()
    await bot.session.close()
    await i18n_core.shutdown()

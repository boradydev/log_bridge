from aiogram import Bot
from aiogram_i18n import I18nMiddleware

from src.presentation.telegram.dispatcher import dispatcher


async def telegram_app(bot: Bot, i18n_middleware: I18nMiddleware) -> None:
    i18n_middleware.setup(dispatcher)
    await dispatcher.start_polling(bot)

import asyncio
import logging

import dotenv

from src.presentation.telegram.app import telegram_app
from src.settings import AppSettings


async def main() -> None:
    dotenv.load_dotenv()
    app_settings = AppSettings()
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
    )
    logger = logging.getLogger(__name__)

    logger.debug("Starting application")
    await telegram_app()


if __name__ == "__main__":
    asyncio.run(main())

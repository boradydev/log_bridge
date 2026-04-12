from typing import TYPE_CHECKING

from aiogram import types

from src.presentation.telegram.dispatcher import dispatcher


if TYPE_CHECKING:
    from src.core.locales.hello import I18nContext as I18n


@dispatcher.message(commands=["start"])
async def cmd_start(message: types.Message, i18n: I18n):
    await message.answer(i18n.hello.user(name=message.from_user.full_name))

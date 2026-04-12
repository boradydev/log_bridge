import logging
from pathlib import Path

from fluent.runtime import FluentBundle, FluentResourceLoader
from fluent.runtime.types import FluentNone

from src.application.abcs import IMessageRegistry
from src.core.langs import excs


logger = logging.getLogger(__name__)


class MessageRegistry(IMessageRegistry):
    def __init__(
        self,
        path: Path,
        file_ftl: str,
        langs: tuple[str, ...] = ("en", "ru"),
    ) -> None:
        self._path = path
        self._langs = langs
        self._loader = FluentResourceLoader(str(self._path / "{locale}"))
        self._file_ftl = file_ftl
        self._bundles: dict[str, FluentBundle] = {}
        for lang in self._langs:
            ftl_path = self._path / lang / file_ftl
            if not ftl_path.exists():
                raise excs.FileFtlNotFound(str(ftl_path))

            bundle = FluentBundle([lang])
            for resource_list in self._loader.resources(lang, [file_ftl]):
                for resource in resource_list:
                    bundle.add_resource(resource)

            self._bundles[lang] = bundle

    def get_message(self, message_id: str, lang: str, **kwargs) -> str:
        bundle = self._bundles.get(lang)
        if not bundle:
            raise excs.FluentBundleNotFound(str(self._path / lang))

        message = bundle.get_message(message_id)
        if not message or not message.value:
            raise excs.MessageToBundleNotFound(message_id)

        pattern = message.value
        result, errors = bundle.format_pattern(pattern, kwargs)
        if errors:
            logger.error(f"Fluent errors: {errors}")

        if isinstance(result, FluentNone):
            raise excs.MessageToBundleNotFound(f"{message_id}, {result}")

        return result

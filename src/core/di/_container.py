import functools
import itertools
from collections.abc import Iterable

import aioinject
from pydantic_settings import BaseSettings

from core.di._types import Providers
from db.dependencies import create_session
from settings import (
    ApplicationSettings,
    DatabaseSettings,
    S3Settings,
    UploadSettings,
    get_settings,
)

from .modules import files, resume

MODULES: Iterable[Providers] = [
    resume.PROVIDERS,
    files.PROVIDERS,
]


SETTINGS = (
    ApplicationSettings,
    DatabaseSettings,
    S3Settings,
    UploadSettings,
)


def _register_settings(
    container: aioinject.Container,
    *,
    settings_classes: Iterable[type[BaseSettings]],
) -> None:
    for settings_cls in settings_classes:
        factory = functools.partial(get_settings, settings_cls)
        container.register(aioinject.Singleton(factory, type_=settings_cls))


@functools.lru_cache
def create_container() -> aioinject.Container:
    container = aioinject.Container()
    container.register(aioinject.Scoped(create_session))

    for provider in itertools.chain.from_iterable(MODULES):
        container.register(provider)

    _register_settings(container, settings_classes=SETTINGS)

    return container

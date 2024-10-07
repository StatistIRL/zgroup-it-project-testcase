from functools import lru_cache
from typing import Type, TypeVar

import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

TSettings = TypeVar("TSettings", bound=BaseSettings)


@lru_cache
def get_settings(cls: Type[TSettings]) -> TSettings:
    """Фабричная функция для создания экземпляров классов настроек с подгрузкой переменных окружения из .env файла.

    Args:
        cls (Type[TSettings]): класс для создания экземпляра после подгрузки переменных окружения.

    Returns:
        TSettings: экземпляр класса настроек.
    """
    dotenv.load_dotenv()
    return cls()


class ApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="app_")

    host: str
    port: int
    reload: bool = False

    allow_origins: list[str]
    allow_origin_regex: str


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="database_")

    driver: str = "postgresql+asyncpg"
    username: str
    password: str
    host: str
    port: int
    name: str

    echo: bool = False

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


class UploadSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="upload_")

    root_path: str
    resume_attachments_folder: str

    allowed_uploaded_file_size: int = 1024 * 1024 * 100  # 100 Mb
    read_chunk_size: int = 1024 * 1024 * 5  # 5 Mb


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="s3_")

    endpoint_url: str
    bucket: str
    access_key: str
    secret_key: str

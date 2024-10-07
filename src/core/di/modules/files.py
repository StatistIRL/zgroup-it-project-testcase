import contextlib
from collections.abc import AsyncIterator

import aioboto3
import aioinject

from core.di._types import Providers
from core.files.repository import UploadedFileRepository
from core.files.service import FileService
from core.files.storage import S3Storage
from settings import S3Settings


@contextlib.asynccontextmanager
async def create_s3_storage(settings: S3Settings) -> AsyncIterator[S3Storage]:
    session = aioboto3.Session(
        aws_access_key_id=settings.access_key,
        aws_secret_access_key=settings.secret_key,
    )
    async with session.client(
        "s3",
        endpoint_url=settings.endpoint_url,
    ) as client:
        yield S3Storage(client=client, bucket=settings.bucket)


PROVIDERS: Providers = [
    aioinject.Singleton(create_s3_storage),
    aioinject.Scoped(UploadedFileRepository),
    aioinject.Scoped(FileService),
]

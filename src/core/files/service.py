from dataclasses import dataclass
from pathlib import PurePath

from fastapi import UploadFile
from result import Err, Ok, Result

from db.models.file import UploadedFile
from settings import UploadSettings

from .dto import UploadedFileDTO
from .exceptions import (
    ContentTypeIsNoneError,
    FilenameIsNoneError,
    InvalidFileSizeError,
)
from .repository import UploadedFileRepository
from .storage import S3Storage, build_random_filename


@dataclass
class ValidatedParams:
    filename: str
    content_type: str
    size: int


class FileService:
    def __init__(
        self,
        s3_storage: S3Storage,
        repository: UploadedFileRepository,
        settings: UploadSettings,
    ) -> None:
        self._s3_storage = s3_storage
        self._settings = settings
        self._repository = repository

    @staticmethod
    def validate_file(
        file: UploadFile,
        max_file_size: int,
    ) -> Result[
        ValidatedParams,
        FilenameIsNoneError | ContentTypeIsNoneError | InvalidFileSizeError,
    ]:
        if file.filename is None:
            return Err(FilenameIsNoneError())

        if file.content_type is None:
            return Err(ContentTypeIsNoneError())

        if file.size is None or file.size > max_file_size:
            return Err(
                InvalidFileSizeError(file_size=file.size, max_file_size=max_file_size)
            )

        return Ok(
            ValidatedParams(
                filename=file.filename,
                content_type=file.content_type,
                size=file.size,
            ),
        )

    async def upload_file(
        self,
        *,
        directory: PurePath,
        file: UploadFile,
    ) -> Result[
        UploadedFileDTO,
        FilenameIsNoneError | ContentTypeIsNoneError | InvalidFileSizeError,
    ]:
        validated_params_result = self.validate_file(
            file,
            max_file_size=self._settings.allowed_uploaded_file_size,
        )
        if isinstance(validated_params_result, Err):
            return validated_params_result

        params = validated_params_result.ok_value

        filename = build_random_filename(params.filename)

        async with self._s3_storage.multipart_upload(
            filename=filename,
            file_path=directory,
        ) as upload:
            while chunk := await file.read(
                self._settings.read_chunk_size,
            ):
                await upload.upload_part(chunk)

            return Ok(
                UploadedFileDTO(
                    bucket=self._s3_storage.bucket,
                    full_path=upload.full_path,
                    size=params.size,
                    filename=params.filename,
                    content_type=params.content_type,
                ),
            )

    async def upload_and_save(
        self,
        *,
        directory: PurePath,
        file: UploadFile,
    ) -> Result[
        UploadedFile,
        FilenameIsNoneError | ContentTypeIsNoneError | InvalidFileSizeError,
    ]:
        result = await self.upload_file(directory=directory, file=file)
        if isinstance(result, Err):
            return result
        return Ok(await self._repository.create(dto=result.ok_value))

    async def delete_file(self, path: str) -> None:
        await self._s3_storage.delete_object(path)

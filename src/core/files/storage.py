from __future__ import annotations

import uuid
from functools import cached_property
from os import PathLike
from pathlib import PurePath
from types import TracebackType
from typing import TYPE_CHECKING, Final, Self
from urllib import parse

from .dto import FilePartDTO

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


class S3Storage:
    def __init__(self, client: S3Client, bucket: str) -> None:
        self._s3_client: Final = client
        self.bucket: Final = bucket

    async def delete_object(self, path: str) -> None:
        await self._s3_client.delete_object(Bucket=self.bucket, Key=path)

    async def generate_presigned_url(
        self,
        key: str,
        bucket: str,
        filename: str,
        expires_in: int = 3_600,
    ) -> str:
        filename = parse.quote(filename)
        return await self._s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket,
                "Key": key,
                "ResponseContentDisposition": f"attachment;filename={filename}",
                "ResponseContentType": "application/octet-stream",
            },
            ExpiresIn=expires_in,
        )

    def multipart_upload(
        self,
        filename: PurePath,
        file_path: PurePath,
    ) -> S3MultipartUpload:
        return S3MultipartUpload(
            client=self._s3_client,
            filename=filename,
            file_path=file_path,
            bucket=self.bucket,
        )


class S3MultipartUpload:
    def __init__(
        self,
        client: S3Client,
        filename: PurePath,
        file_path: PurePath,
        bucket: str,
    ) -> None:
        self._s3_client = client
        self._bucket = bucket
        self._filename = filename
        self.file_size = 0
        self._file_path = file_path
        self._upload_id = ""
        self._e_tags: list[tuple[int, str]] = []
        self._part_number = 0

    @cached_property
    def full_path(self) -> str:
        return PurePath(self._file_path, self._filename).as_posix()

    async def __aenter__(self) -> Self:
        self._upload_id = await self._create_multipart_upload()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_val is not None:
            await self._abort_multipart_upload()

        await self._complete_multipart_upload()

    async def upload_part(self, chunk: bytes) -> None:
        self._part_number += 1
        self.file_size += len(chunk)
        dto = FilePartDTO(
            filename=self._filename,
            file_path=self._file_path,
            chunk=chunk,
            part_number=self._part_number,
        )
        e_tag = await self._upload_part(dto)
        self._e_tags.append((self._part_number, e_tag))

    async def _upload_part(
        self,
        dto: FilePartDTO,
    ) -> str:
        response = await self._s3_client.upload_part(
            Bucket=self._bucket,
            Key=self.full_path,
            Body=dto.chunk,
            PartNumber=dto.part_number,
            UploadId=self._upload_id,
        )
        return response["ETag"].replace('"', "")

    async def _create_multipart_upload(self) -> str:
        response = await self._s3_client.create_multipart_upload(
            Bucket=self._bucket,
            Key=self.full_path,
        )
        return response["UploadId"]

    async def _complete_multipart_upload(self) -> int:
        response = await self._s3_client.complete_multipart_upload(
            Bucket=self._bucket,
            Key=self.full_path,
            UploadId=self._upload_id,
            MultipartUpload={
                "Parts": [
                    {"PartNumber": part_number, "ETag": e_tag}
                    for part_number, e_tag in self._e_tags
                ],
            },
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]

    async def _abort_multipart_upload(self) -> int:
        response = await self._s3_client.abort_multipart_upload(
            Bucket=self._bucket,
            Key=self.full_path,
            UploadId=self._upload_id,
        )
        return response["ResponseMetadata"]["HTTPStatusCode"]


def build_random_filename(filepath: PathLike[str] | str) -> PurePath:
    if not isinstance(filepath, PurePath):
        filepath = PurePath(filepath)

    return filepath.with_stem(str(uuid.uuid4()))

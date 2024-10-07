from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from core.files.dto import UploadedFileDTO
from db.models import UploadedFile


class UploadedFileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, dto: UploadedFileDTO) -> UploadedFile:
        model = UploadedFile(
            bucket=dto.bucket,
            name=dto.filename,
            path=dto.full_path,
            file_size=dto.size,
            content_type=dto.content_type,
        )
        self._session.add(model)
        await self._session.flush()
        return model

    async def get(self, id_: UUID) -> UploadedFile | None:
        return await self._session.get(UploadedFile, id_)

    async def delete(self, model: UploadedFile) -> None:
        await self._session.delete(model)
        await self._session.flush()

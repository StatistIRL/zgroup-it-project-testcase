from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.resume import Resume

from .dto import ResumeCreateDTO


class ResumeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_resume_list(self) -> Sequence[Resume]:
        query = select(Resume).order_by(Resume.created_at, Resume.rating)
        return (await self._session.scalars(query)).all()

    async def get(self, id_: UUID) -> Resume | None:
        return await self._session.get(Resume, id_)

    async def delete(self, model: Resume) -> None:
        await self._session.delete(model)
        await self._session.flush()

    async def create_resume(self, dto: ResumeCreateDTO):
        model = Resume(
            pretender_name=dto.pretender_name,
            rating=dto.rating,
            file_id=dto.file_id,
        )
        self._session.add(model)
        await self._session.flush()
        return model

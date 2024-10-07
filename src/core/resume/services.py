import uuid
from collections.abc import Sequence
from pathlib import PurePath

from fastapi import UploadFile
from result import Err, Ok, Result

from core.exceptions import ObjectNotFoundError
from core.files.exceptions import (
    ContentTypeIsNoneError,
    FilenameIsNoneError,
    InvalidFileSizeError,
)
from core.files.repository import UploadedFileRepository
from core.files.service import FileService
from db.models.resume import Resume
from settings import UploadSettings

from .dto import ResumeCreateDTO
from .repositories import ResumeRepository


class ResumeService:
    def __init__(
        self,
        file_service: FileService,
        resume_repository: ResumeRepository,
        file_repository: UploadedFileRepository,
        settings: UploadSettings,
    ) -> None:
        self._file_service = file_service
        self._resume_repository = resume_repository
        self._file_repository = file_repository
        self._settings = settings

    async def read_resume_list(self) -> Sequence[Resume]:
        resume_list = await self._resume_repository.get_resume_list()
        return resume_list

    async def upload_pretender_resume(
        self,
        file: UploadFile,
        dto: ResumeCreateDTO,
    ) -> Result[
        Resume, FilenameIsNoneError | ContentTypeIsNoneError | InvalidFileSizeError
    ]:
        resume_file_id = uuid.uuid4()
        file_upload = await self._file_service.upload_and_save(
            file=file,
            directory=PurePath(
                self._settings.root_path,
                self._settings.resume_attachments_folder,
                str(resume_file_id),
            ),
        )
        if isinstance(file_upload, Err):
            return file_upload

        dto.file_id = file_upload.ok_value.id
        resume = await self._resume_repository.create_resume(dto=dto)
        return Ok(resume)

    async def delete_resume(self, id_: uuid.UUID) -> Result[None, ObjectNotFoundError]:
        resume = await self._resume_repository.get(id_=id_)
        if resume is None:
            return Err(ObjectNotFoundError(id_=id_, entity_name="Resume"))

        uploaded_file = await self._file_repository.get(id_=resume.file_id)
        if uploaded_file is None:
            return Err(
                ObjectNotFoundError(id_=str(resume.file_id), entity_name="UploadedFile")
            )

        await self._resume_repository.delete(model=resume)
        await self._file_service.delete_file(path=uploaded_file.path)
        await self._file_repository.delete(model=uploaded_file)

        return Ok(None)

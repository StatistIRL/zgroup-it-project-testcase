from typing import Annotated, assert_never
from uuid import UUID

from aioinject import Inject
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, Form, Path, UploadFile
from fastapi_pagination import Page, paginate
from result import Err
from starlette import status

from api.exceptions import (
    FileContentTypeIsNoneHTTPError,
    FilenameIsNoneHTTPError,
    InvalidFileSizeHTTPError,
    ObjectNotFoundHTTPError,
)
from core.exceptions import ObjectNotFoundError
from core.files.exceptions import (
    ContentTypeIsNoneError,
    FilenameIsNoneError,
    InvalidFileSizeError,
)
from core.resume.dto import ResumeCreateDTO
from core.resume.services import ResumeService

from .schemas import ResumeSchema

router = APIRouter(
    prefix="/resume",
    tags=["resume"],
)


@router.get(
    "/list",
    responses={
        status.HTTP_200_OK: {"model": Page[ResumeSchema]},
    },
)
@inject
async def read_resume_list(
    service: Annotated[ResumeService, Inject],
) -> Page[ResumeSchema]:
    result = await service.read_resume_list()
    return paginate(ResumeSchema.model_validate_list(result))


@router.post(
    "/upload",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def upload_resume(
    pretender_name: Annotated[str, Form(alias="pretender_name")],
    rating: Annotated[float, Form(alias="rating")],
    upload_file: UploadFile,
    service: Annotated[ResumeService, Inject],
) -> None:
    dto = ResumeCreateDTO(
        pretender_name=pretender_name,
        rating=rating,
    )
    result = await service.upload_pretender_resume(file=upload_file, dto=dto)
    if isinstance(result, Err):
        match err := result.err_value:
            case FilenameIsNoneError():
                raise FilenameIsNoneHTTPError
            case ContentTypeIsNoneError():
                raise FileContentTypeIsNoneHTTPError
            case InvalidFileSizeError():
                raise InvalidFileSizeHTTPError(
                    max_file_size=err.max_file_size,
                )
            case _ as never:
                assert_never(never)


@router.delete(
    "/delete/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Resume not found"},
    },
)
@inject
async def delete_resume(
    resume_id: Annotated[UUID, Path()],
    service: Annotated[ResumeService, Inject],
) -> None:
    result = await service.delete_resume(id_=resume_id)
    if isinstance(result, Err):
        match err := result.err_value:
            case ObjectNotFoundError():
                raise ObjectNotFoundHTTPError(
                    identifier=str(err.id), entity_name=err.entity_name
                )
            case _ as never:
                assert_never(never)

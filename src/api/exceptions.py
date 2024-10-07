from typing import Protocol

from starlette import status

from core.schema import BaseSchema


class APIErrorSchema(BaseSchema):
    code: str
    message: str


class HasIdentifierAPIErrorSchema(APIErrorSchema):
    identifier: str
    entity_name: str


class BaseHTTPErrorProtocol(Protocol):
    status_code: int
    error_schema: APIErrorSchema
    code: str


class BaseHTTPError(BaseHTTPErrorProtocol, Exception):
    pass


class FilenameIsNoneHTTPError(BaseHTTPError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "filename_is_none"
    error_schema = APIErrorSchema(
        code=code,
        message="Filename must be not None",
    )


class FileContentTypeIsNoneHTTPError(BaseHTTPError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "file_content_type_is_none"
    error_schema = APIErrorSchema(
        code=code,
        message="File content-type is None",
    )


class InvalidFileSizeHTTPError(BaseHTTPError):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    code = "invalid_file_size"

    def __init__(self, max_file_size: int) -> None:
        self.error_schema = APIErrorSchema(
            code=self.code,
            message=f"The file must not be larger than {max_file_size} bytes",
        )


class ObjectNotFoundHTTPError(BaseHTTPError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "object_not_found"

    def __init__(self, identifier: str, entity_name: str) -> None:
        self.error_schema = HasIdentifierAPIErrorSchema(
            code=self.code,
            message="Object not found",
            identifier=identifier,
            entity_name=entity_name,
        )

class FileUploadValidationError(Exception):
    pass


class FilenameIsNoneError(FileUploadValidationError):
    pass


class ContentTypeIsNoneError(FileUploadValidationError):
    pass


class InvalidFileSizeError(FileUploadValidationError):
    def __init__(
        self,
        file_size: int | None,
        max_file_size: int,
    ) -> None:
        self.file_size = file_size
        self.max_file_size = max_file_size

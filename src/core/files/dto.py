from dataclasses import dataclass
from pathlib import PurePath


@dataclass(frozen=True, slots=True)
class UploadedFileDTO:
    size: int
    bucket: str
    filename: str
    full_path: str
    content_type: str


@dataclass(frozen=True, slots=True)
class FilePartDTO:
    chunk: bytes
    part_number: int
    filename: PurePath
    file_path: PurePath

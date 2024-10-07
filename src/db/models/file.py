import datetime

from sqlalchemy.orm import Mapped, mapped_column

from core.utils import utc_now
from db.base import Base, str_64, str_128, uuid_pk


class UploadedFile(Base):
    __tablename__ = "uploaded_file"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        comment="Название загружаемого файла с расширением"
    )
    path: Mapped[str] = mapped_column(comment="Полный путь до файла в S3")
    content_type: Mapped[str_64]
    file_size: Mapped[int]
    bucket: Mapped[str_128] = mapped_column(comment="Название бакета в S3")
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=utc_now, comment="Дата создания записи информации о файле"
    )

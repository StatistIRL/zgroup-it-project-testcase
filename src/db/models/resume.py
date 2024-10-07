import datetime
import uuid

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.utils import utc_now
from db.base import Base, uuid_pk
from db.models import UploadedFile


class Resume(Base):
    __tablename__ = "resume"
    __table_args__ = (
        CheckConstraint("rating BETWEEN 0.0 AND 5.0", "rating_between_0_5_range"),
    )

    id: Mapped[uuid_pk]
    pretender_name: Mapped[str] = mapped_column(nullable=False, comment="Имя кандидата")
    rating: Mapped[float] = mapped_column(comment="Оценочный рейтниг резюме")

    file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("uploaded_file.id"), comment="Загруженный файл резюме"
    )
    file: Mapped[UploadedFile] = relationship()

    created_at: Mapped[datetime.datetime] = mapped_column(
        default=utc_now, comment="Дата создания записи резюме"
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=utc_now, onupdate=utc_now, comment="Дата редактирования записи резюме"
    )

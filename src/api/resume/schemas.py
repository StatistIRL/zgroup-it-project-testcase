from datetime import datetime
from typing import Any, Iterable, Self
from uuid import UUID

from core.schema import BaseSchema


class ResumeSchema(BaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
    pretender_name: str
    rating: float
    file_id: UUID

    @classmethod
    def model_validate_list(cls, models: Iterable[Any]) -> list[Self]:
        return [cls.model_validate(model) for model in models]

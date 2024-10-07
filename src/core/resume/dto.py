from dataclasses import dataclass
from uuid import UUID


@dataclass
class ResumeCreateDTO:
    pretender_name: str
    rating: float
    file_id: UUID | None = None

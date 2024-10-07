import aioinject

from core.di._types import Providers
from core.resume.repositories import ResumeRepository
from core.resume.services import ResumeService

PROVIDERS: Providers = [
    aioinject.Scoped(ResumeRepository),
    aioinject.Scoped(ResumeService),
]

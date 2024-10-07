import contextlib
from typing import AsyncIterator

from aioinject.ext.fastapi import AioInjectMiddleware
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from starlette.middleware.cors import CORSMiddleware

from api.exceptions import BaseHTTPError
from api.resume import resume_router
from core.di import create_container
from settings import ApplicationSettings, get_settings

routers = [
    resume_router,
]


@contextlib.asynccontextmanager
async def _lifespan(
    app: FastAPI,  # noqa: ARG001 - required by lifespan protocol
) -> AsyncIterator[None]:
    async with contextlib.aclosing(create_container()):
        yield


async def http_exception_handler(
    request: Request,  # noqa: ARG001
    exc: BaseHTTPError,
) -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder(exc.error_schema.model_dump(by_alias=True)),
        status_code=exc.status_code,
    )


def create_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    add_pagination(app)

    for router in routers:
        app.include_router(router)

    app.exception_handlers[BaseHTTPError] = http_exception_handler

    settings: ApplicationSettings = get_settings(ApplicationSettings)
    app.add_middleware(AioInjectMiddleware, container=create_container())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_origin_regex=settings.allow_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    disable_installed_extensions_check()
    return app

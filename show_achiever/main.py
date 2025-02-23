from typing import TYPE_CHECKING

try:
    from mysite.asgi import django_app
except ImportError:
    from show_achiever.mysite.asgi import django_app

from achiever_app.endpoints.internal.router import achiever_app_internal_router
from achiever_app.endpoints.router import achiever_app_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mysite.config import settings
from mysite.errors.handlers import error_handler_pairs
from mysite.middleware import add_middlewares
from telegram_bot_app.endpoints.router import telegram_bot_router

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


async def lifecycle(_: FastAPI) -> "AsyncGenerator[None]":
    """Add your lifecycle events here."""
    yield


# app is a wrapper, while `achiever_app` is the actual FastAPI instance.
# `app` should only contain `/healthz` endpoint for it to be:
#   - accessible by health checks
#   - not be accessible by users
#   - be in the true root of the path
app = FastAPI(
    lifespan=lifecycle,
)

achiever_app = FastAPI(
    debug=settings.debug,
    title=settings.title,
    version=settings.version,
    root_path=settings.root_path,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

for handler in error_handler_pairs:
    achiever_app.add_exception_handler(handler[0], handler[1])

app.include_router(achiever_app_internal_router)
achiever_app.include_router(achiever_app_router)
achiever_app.include_router(telegram_bot_router)


achiever_app.mount("/django", django_app)

achiever_app.mount(
    "/static",
    StaticFiles(
        directory="static",
    ),
    name="static",
)
achiever_app.mount(
    "/media",
    StaticFiles(
        directory="media",
    ),
    name="media",
)

app.mount("", achiever_app)


add_middlewares(achiever_app)

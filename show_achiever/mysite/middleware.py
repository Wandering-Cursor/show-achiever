from typing import TYPE_CHECKING

from asgiref.sync import sync_to_async
from django.db import connections
from fastapi.middleware.cors import CORSMiddleware
from mysite.config import security_settings

if TYPE_CHECKING:
    from fastapi import FastAPI


def add_cors_middleware(app: "FastAPI") -> "FastAPI":
    """
    Adds a CORS middleware with settings from Security Settings.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=security_settings.allow_credentials,
        allow_methods=security_settings.allow_methods,
        allow_headers=security_settings.cors_headers,
        allow_origin_regex="|".join(security_settings.cors_allow_origin_regex),
    )

    return app


def close_old_connections(**kwargs: object) -> None:  # noqa: ARG001
    for conn in connections.all(initialized_only=True):
        conn.close_if_unusable_or_obsolete()


class CloseOldConnectionsMiddleware:
    """
    This connection closes old connections before each request.

    Used because Django doesn't close old connections automatically when using
    ASGI.
    """

    def __init__(self, app: "FastAPI") -> None:
        self.app = app
        self.ignore_endpoints = ("/healthz",)

    async def __call__(self, scope, receive, send) -> None:  # noqa: ANN001
        if scope["type"] == "http":
            path = scope["path"]
            if path not in self.ignore_endpoints:
                # Wrapped in `sync_to_async` because Django ORM is synchronous
                # at least in some parts when they close the connection
                await sync_to_async(close_old_connections)()
        await self.app(scope, receive, send)


def add_middlewares(app: "FastAPI") -> "FastAPI":
    app.add_middleware(CloseOldConnectionsMiddleware)

    return app

"""
The router for `achiever_app` endpoints.
Add all routers for the `achiever_app` here.
"""

from achiever_app.endpoints.task.router import task_router
from fastapi import APIRouter
from mysite.errors.responses import responses

achiever_app_router = APIRouter(
    responses=responses,
)

achiever_app_router.include_router(
    task_router,
)

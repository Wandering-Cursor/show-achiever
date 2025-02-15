"""
The router for `achiever_app` endpoints.
Add all routers for the `achiever_app` here.
"""

from fastapi import APIRouter
from mysite.errors.responses import responses

achiever_app_router = APIRouter(
    responses=responses,
)

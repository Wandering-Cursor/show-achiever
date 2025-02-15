"""
Router for the Telegram Bot.
"""

from fastapi import APIRouter
from mysite.errors.responses import responses

telegram_bot_router = APIRouter(
    responses=responses,
)

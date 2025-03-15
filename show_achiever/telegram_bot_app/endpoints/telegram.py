from typing import Annotated

from fastapi import Body
from mysite.errors.http_errors import NotFoundError
from telegram_bot_app.endpoints.router import telegram_bot_router
from telegram_bot_app.models.enums import BotPlatforms
from telegram_bot_app.operations.webhook.process import process_webhook
from telegram_bot_app.operations.webhook.read import find_bot


@telegram_bot_router.post(
    "/{platform}/{secret_token}/{bot_token}",
)
async def telegram_webhook(
    secret_token: str,
    bot_token: str,
    webhook_data: Annotated[dict, Body()],
    platform: BotPlatforms = BotPlatforms.TELEGRAM,
) -> dict:
    """
    Telegram Webhook endpoint
    """
    bot = await find_bot(
        platform=platform,
        secret=secret_token,
        token=bot_token,
    )

    if not bot:
        raise NotFoundError(
            log_message={
                "msg": "Received a webhook request for an unknown bot",
                "platform": platform,
                "secret": secret_token,
                "token": bot_token,
            }
        )

    await process_webhook(
        bot=bot,
        webhook_data=webhook_data,
    )

    return {"status": "ok"}

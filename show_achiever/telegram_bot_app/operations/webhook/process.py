from typing import TYPE_CHECKING

from telegram_bot_app.operations.telegram.integration import make_bot

if TYPE_CHECKING:
    from telegram_bot_app.models.bot import Bot


async def process_webhook(
    bot: "Bot",
    webhook_data: dict,
) -> None:
    """
    Process the webhook data
    """
    handler = make_bot(bot)

    await handler.process_update(update=webhook_data)

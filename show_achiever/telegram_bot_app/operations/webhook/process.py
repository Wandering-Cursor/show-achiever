from typing import TYPE_CHECKING

from telegram_bot_app.operations.telegram.integration import MyApp, convert_data_to_update

if TYPE_CHECKING:
    from telegram_bot_app.models.bot import Bot


async def process_webhook(
    bot: "Bot",
    webhook_data: dict,
) -> None:
    """
    Process the webhook data
    """
    handler = await MyApp.get_bot(bot=bot)

    # Consider storing the update data in the DB, perhaps

    update = await convert_data_to_update(data=webhook_data, bot=handler)

    await handler.process_update(
        update=update,
    )

    await MyApp.finish(bot=bot)

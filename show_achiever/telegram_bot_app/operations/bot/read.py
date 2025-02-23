from telegram_bot_app.models.bot import Bot


async def get_bot_by_token(token: str) -> Bot:
    return await Bot.objects.aget(
        bot_token=token,
    )

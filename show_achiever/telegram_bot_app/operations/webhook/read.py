from telegram_bot_app.models.bot import Bot
from telegram_bot_app.models.enums import BotPlatforms


async def find_bot(
    platform: BotPlatforms,
    secret: str,
    token: str,
) -> Bot | None:
    try:
        return await Bot.objects.aget(
            platform=platform,
            webhook_secret=secret,
            bot_token=token,
        )
    except Bot.DoesNotExist:
        return None


async def find_all_bots(
    platform: BotPlatforms,
) -> list[Bot]:
    qs = Bot.objects.filter(platform=platform)

    return [bot async for bot in qs]

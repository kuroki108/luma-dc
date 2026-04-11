import discord
import datetime
from discord.ext import tasks
from zoneinfo import ZoneInfo

WEEKLY_CHANNEL_ID = 1492532959662833786

TIMEZONE = ZoneInfo("Europe/Berlin")
TIME01 = datetime.time(hour=18, minute=0, tzinfo=TIMEZONE)
TIME02 = datetime.time(hour=17, minute=45, tzinfo=TIMEZONE)

def build_weekly_embed() -> discord.Embed:
    return discord.Embed(
        title="Wöchendliche Besprechung",
        description=(
            "Einmal bitte eintragen wer am Dienstag um 18:00 Uhr kann."
        ),
        color=discord.Color.purple()
    )

async def get_channel(bot: discord.Client):
    try:
        return bot.get_channel(WEEKLY_CHANNEL_ID) or await bot.fetch_channel(WEEKLY_CHANNEL_ID)
    except discord.NotFound:
        print(f"[Weekly] Channel {WEEKLY_CHANNEL_ID} nicht gefunden!")
    except discord.Forbidden:
        print(f"[Weekly] Kein Zugriff auf Channel {WEEKLY_CHANNEL_ID}!")
    return None

async def send_weekly_notification(bot: discord.Client):
    channel = await get_channel(bot)
    if channel is None:
        return

    msg = await channel.send(
        "||@Team||",
        embed=build_weekly_embed(),
        allowed_mentions=discord.AllowedMentions(everyone=True)
    )
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

async def send_weekly_reminder(bot: discord.Client):
    channel = await get_channel(bot)
    if channel is None:
        return

    await channel.send(
        "||@Team||\n"
        "Wir haben gleich Weekly, bitte eintragen falls noch nicht geschehen!",
        allowed_mentions=discord.AllowedMentions(everyone=True)
    )

@tasks.loop(time=[TIME01, TIME02])
async def weekly_task():
    bot = weekly_task._bot
    now = datetime.datetime.now(TIMEZONE)

    if now.weekday() == 0 and now.hour == TIME01.hour and now.minute == TIME01.minute:  # Montag
        await send_weekly_notification(bot)
    elif now.weekday() == 1 and now.hour == TIME02.hour and now.minute == TIME02.minute:  # Dienstag
        await send_weekly_reminder(bot)

@weekly_task.before_loop
async def before_weekly():
    await weekly_task._bot.wait_until_ready()
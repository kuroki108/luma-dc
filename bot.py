import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from modules.selfroles import RoleView01, RoleView02, color_booster
from modules.weekly import weekly_task
from modules.welcome_msg import on_member_join

# -------------------------------------------------------

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment ERROR")

# -------------------------------------------------------
# Selfroles Embed
EMBED_IMAGE_URL = "attachment://banner.png"
EMBED_COLOR     = discord.Color.purple()
EMBED_TITLE     = "Selfroles"
EMBED_DESC      = (
    "Zeig der Community wer du bist!\n"
    "Du kannst Rollen jederzeit wechseln oder entfernen."
)

# Color Embed
COLOR_IMAGE_URL = "attachment://banner_color.png"
COLOR_COLOR     = discord.Color.purple()
COLOR_TITLE     = "🎨 Wähl deine Farbe"
COLOR_DESC      = (
    "Als Booster hast du Zugang zu exklusiven Farbrollen!\n"
    "Such dir eine Farbe aus und mach deinen Namen zum Hingucker."
)

# Berechtigte Rollen-IDs
ADMIN_ROLES = (1490723942946705558, 1490723470483521706, 1490678382713638962)

BOOSTER_ROLE_ID = 1490690920222556364

# -------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.invites = True 
intents.manage


bot = commands.Bot(command_prefix='!', intents=intents)
bot.add_listener(on_member_join)


# -------------------------------------------------------
# Events
# -------------------------------------------------------

@bot.event
async def on_ready():
    print(f"Der Discord Bot [{bot.user}] ist online!")


    if not bot.persistent_views:
        bot.add_view(RoleView01())
        bot.add_view(RoleView02())
        bot.add_view(color_booster(BOOSTER_ROLE_ID))

    # Weekly Task starten
    if not weekly_task.is_running():
        weekly_task._bot = bot
        weekly_task.start()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        await ctx.send("Du hast keine Berechtigung diesen Befehl auszuführen.", delete_after=3)
    else:
        raise error

# -------------------------------------------------------
# Embed Builder
# -------------------------------------------------------

def build_selfroles_embed() -> discord.Embed:
    embed = discord.Embed(
        title=EMBED_TITLE,
        description=EMBED_DESC,
        color=EMBED_COLOR,
    )
    embed.set_image(url=EMBED_IMAGE_URL)
    return embed


def build_color_embed() -> discord.Embed:
    embed = discord.Embed(
        title=COLOR_TITLE,
        description=COLOR_DESC,
        color=COLOR_COLOR,
    )
    embed.set_image(url=COLOR_IMAGE_URL)
    return embed

# -------------------------------------------------------
# Commands
# -------------------------------------------------------


@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")


@bot.command()
@commands.has_any_role(*ADMIN_ROLES)
async def selfroles(ctx):
    file = discord.File("assets/banner.png", filename="banner.png")

    selfroles_ids = {"select_gender", "select_age", "select_state", "select_dm_status", "select_games", "select_ping"}
    async for message in ctx.channel.history(limit=50):
        if message.author == bot.user:
            component_ids = {
                component.custom_id
                for row in message.components
                for component in row.children
                if hasattr(component, "custom_id")
            }
            if component_ids & selfroles_ids:
                try:
                    await message.delete()
                except discord.HTTPException:
                    pass

    try:
        await ctx.message.delete()
    except discord.HTTPException:
        pass

    await ctx.send(file=file, embed=build_selfroles_embed(), view=RoleView01())
    await ctx.send(view=RoleView02())


@bot.command()
@commands.has_any_role(*ADMIN_ROLES)
async def color(ctx):
    file = discord.File("assets/banner_color.png", filename="banner_color.png")

    async for message in ctx.channel.history(limit=50):
        if message.author == bot.user and (message.components or message.embeds):
            try:
                await message.delete()
            except discord.HTTPException:
                pass

    try:
        await ctx.message.delete()
    except discord.HTTPException:
        pass

    await ctx.send(file=file, embed=build_color_embed(), view=color_booster(BOOSTER_ROLE_ID))


# -------------------------------------------------------

if __name__ == "__main__":
    bot.run(TOKEN)
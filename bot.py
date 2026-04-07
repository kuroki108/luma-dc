import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# ------------------------------------------------------

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment ERROR")

# -------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


# -------------------------------------------------------
# Events
# -------------------------------------------------------

@bot.event
async def on_ready():
    print(f"Der Discord Bot [{bot.user}] ist online!")


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send("Pong!")

# -------------------------------------------------------

if __name__ == "__main__":
    bot.run(TOKEN)
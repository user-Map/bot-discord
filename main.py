import discord
from discord.ext import commands
import os

PREFIX = ".."
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"🔥 Bot online: {bot.user}")

@bot.event
async def setup_hook():
    for file in os.listdir("./cmds"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"cmds.{file[:-3]}")
                print(f"Loaded {file}")
            except Exception as e:
                print(f"Error {file}: {e}")

if not TOKEN:
    print("TOKEN MISSING")
else:
    bot.run(TOKEN)

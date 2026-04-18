import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix=">", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot đã online: {bot.user}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def usermap(ctx, amount: int):
    guild = ctx.guild

    # Giới hạn tránh spam quá
    if amount > 20:
        return await ctx.send("❌ Tối đa 20 kênh thôi!")

    created = 0

    for i in range(amount):
        try:
            channel = await guild.create_text_channel(f"user-{i+1}")
            created += 1
            await asyncio.sleep(0.5)  # tránh rate limit
        except:
            break

    await ctx.send(f"✅ Đã tạo {created} kênh!")

bot.run("TOKEN_CUA_BAN")

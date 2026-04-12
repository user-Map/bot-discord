from discord.ext import commands

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def menu(self, ctx):
        await ctx.send("🔥 BOT OK - MENU WORKING")

async def setup(bot):
    await bot.add_cog(Menu(bot))

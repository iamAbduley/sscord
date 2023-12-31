from discord import Embed
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name = "help")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def help_command(self, ctx):

        embed = Embed(description="Type **`??ss`** while replying a message", color = 0xfffff)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        await ctx.send(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
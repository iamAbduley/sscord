import asyncio
import discord
from io import BytesIO
from discord.ext import commands
from utils.sscord import SSCORD
from typing import Optional
from utils.functions import check_permission
from utils.log import log

class Screenshot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(name = "ss", aliases = ["bang", "catch", "shot", "shoot"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.bot_has_permissions(attach_files=True, send_messages=True, read_message_history= True)
    async def screenshot(self, ctx, channel: Optional[discord.TextChannel]):
        # send to specified channel
        if channel is not None and isinstance(channel, discord.TextChannel):
            if await check_permission(ctx) is False:
                return
        else:
            channel = ctx.channel

        replied_message_id = ctx.message.reference.message_id if ctx.message.reference else None

        if replied_message_id:
            replied_message = await ctx.channel.fetch_message(replied_message_id)

            if replied_message:
                if replied_message.content == "":
                    await ctx.send("Not supported images now", delete_after = 6)
                    return

                sscord = SSCORD(replied_message.author, replied_message)
                img = await sscord.draw()
            else:
                ctx.command.reset_cooldown(ctx)
                await ctx.send("Not found replied message.", delete_after = 6)
                return
        else:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("Use this command while replying a message.", delete_after = 6)
            return

        with BytesIO() as a:
            img.save(a, "PNG")
            a.seek(0)
            first_message = await ctx.send(content = ":camera_with_flash: Screenshootting..")
            last_message = await channel.send(content= None, file = discord.File(a, "sscord.png"))
            await first_message.delete()
        await log(self.bot, ctx, last_message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Screenshot(bot))
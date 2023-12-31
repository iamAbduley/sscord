from discord.ext import commands
from typing import Optional

async def check_permission(ctx):
    if ctx.author.guild_permissions.manage_messages: 
        return True
    await ctx.send("You need **Manage Messages** permission for use this command", delete_after = 6)
    return False
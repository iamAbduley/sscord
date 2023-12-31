from discord.ext import commands
from discord import Embed, Message
from zoneinfo import ZoneInfo

LOG_CHANNEL = 1190951263026811000

async def log(bot, ctx, message: Message):
    TURKIYE_ISTANBUL = ZoneInfo("Europe/Istanbul")

    channel = bot.get_channel(LOG_CHANNEL)
    created_at = message.created_at.astimezone(tz = TURKIYE_ISTANBUL).strftime('%d %B %Y - %H:%M')

    author = ctx.author
    guild = ctx.guild

    embed = Embed(
        description = f":camera_with_flash: Screenshotted by {author.name} in {guild.name} at {created_at}",
        color = 0xffffff
        )
    embed.set_image(url = message.attachments[0].url)
    embed.add_field(
        name = "IDs & URL", value = f"""**`Server ID:`** {guild.id}
        **`Author ID:`** {author.id}
        **`Message URL:`** [Click Here]({message.jump_url})""")
    
    await channel.send(embed = embed)
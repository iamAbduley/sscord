import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

prefixes = ("<@1190016167826440293>", "??")

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = prefixes,
            intents = discord.Intents.all(),
            activity = discord.Streaming(
                name="??ss | Take A Screenshot",
                url="https://www.twitch.tv/iamabduley"),
            application_id = 1190016167826440293)
        
        self.initial_extensions = ["utils.error_handler"]
        self.prefix = prefixes

    async def setup_hook(self):
        cogs_folder = os.listdir("./cogs/")

        for file in cogs_folder:
            if file != "__pycache__":
                try:
                    self.initial_extensions.append(f"cogs.{file[:-3]}")
                except FileNotFoundError:
                    print("Cogs files was failed!")

        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync()
        
    async def on_ready(self):
       print(f"{self.user} is connected to Discord")


bot = MyBot()
bot.remove_command("help")

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

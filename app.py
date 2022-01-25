import discord
import logging
import os

from dotenv import load_dotenv

# Set up the environment from `.env`
load_dotenv()
if "DISCORD_BOT_TOKEN" not in os.environ:
    raise RuntimeError("DISCORD_BOT_TOKEN must be defined in the environment.")


class Discordle(discord.Client):
    def __init__(self):
        intents = discord.Intents.none()
        intents.guilds = True
        intents.members = True
        intents.guild_messages = True
        super().__init__(intents=intents)
        
    # Event handlers
    async def on_ready(self):
        logging.info("Discordle ready!")
        
    async def on_message(self, message: discord.Message):
        print(message.content)


if __name__ == "__main__":
    bot = Discordle()
    bot.run(os.environ["DISCORD_BOT_TOKEN"])

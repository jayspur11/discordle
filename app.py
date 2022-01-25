import discord
import logging
import management
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

        self.checked_guilds = False

    # Event handlers
    async def on_ready(self):
        logging.info("Discordle ready!")

        if self.checked_guilds:
            # We've already been through this setup.
            return
        self.checked_guilds = True

        for guild in self.guilds:
            wordler_role = await management.get_wordler_role(guild)
            await management.configure_wordler_channel(guild, wordler_role)

    async def on_message(self, message: discord.Message):
        print(message.content)


if __name__ == "__main__":
    bot = Discordle()
    bot.run(os.environ["DISCORD_BOT_TOKEN"])

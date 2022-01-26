import discord
import logging
import management
import message_util
import os

from datetime import datetime
from dateutil import tz
from dotenv import load_dotenv

# Set up the environment from `.env`
load_dotenv()

if "DISCORD_BOT_TOKEN" not in os.environ:
    raise RuntimeError("DISCORD_BOT_TOKEN must be defined in the environment.")

# Using Eastern time here because that's the most-forward TZ of the group I'm
# building this for
_US_EASTERN = tz.gettz("US/Eastern")
_WORDLE_DAY_ZERO = datetime(2021, 6, 19, tzinfo=_US_EASTERN)


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
        message_wordle_number = message_util.get_wordle_number(message.content)
        if message_wordle_number is None:
            return

        current_wordle_number = (datetime.now(tz=_US_EASTERN) -
                                 _WORDLE_DAY_ZERO).days
        if message_wordle_number == current_wordle_number:
            # TODO grant access
            print("Great success!")


if __name__ == "__main__":
    bot = Discordle()
    bot.run(os.environ["DISCORD_BOT_TOKEN"])

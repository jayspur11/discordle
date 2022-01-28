import discord
import logging
import management
import message_util
import os

from asyncio import run_coroutine_threadsafe
from datetime import datetime, time, timedelta
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
        intents.guild_messages = True
        intents.members = True
        super().__init__(intents=intents)

        self.checked_guilds = False

    async def revoke(self):
        await management.revoke_wordler_roles(self.guilds)
        self.schedule_revocation()

    def schedule_revocation(self):
        tomorrow = datetime.now(tz=_US_EASTERN).date() + timedelta(days=1)
        midnight = time(0, 0, tzinfo=_US_EASTERN)
        tomorrow_midnight = datetime.combine(tomorrow,
                                             midnight,
                                             tzinfo=_US_EASTERN)
        self.loop.call_at(tomorrow_midnight.timestamp(),
                          run_coroutine_threadsafe, self.revoke(), self.loop)

    # Event handlers
    async def on_ready(self):
        logging.info("Discordle ready!")

        if self.checked_guilds:
            # We've already been through this setup.
            return
        self.checked_guilds = True

        self.schedule_revocation()
        for guild in self.guilds:
            await management.configure_guild(guild)

    async def on_message(self, message: discord.Message):
        message_wordle_number = message_util.get_wordle_number(message.content)
        if message_wordle_number is None:
            return

        current_wordle_number = (datetime.now(tz=_US_EASTERN) -
                                 _WORDLE_DAY_ZERO).days
        if message_wordle_number == current_wordle_number:
            await management.grant_wordler_role(message)

    async def on_guild_join(self, guild):
        await management.configure_guild(guild)


if __name__ == "__main__":
    bot = Discordle()
    bot.run(os.environ["DISCORD_BOT_TOKEN"])

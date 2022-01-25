import discord
import logging
import os

from dotenv import load_dotenv

# Set up the environment from `.env`
load_dotenv()

if "DISCORD_BOT_TOKEN" not in os.environ:
    raise RuntimeError("DISCORD_BOT_TOKEN must be defined in the environment.")

# Add a non-printing space to the end as a human-namespace-collision-avoider.
_WORDLER_ROLE = "wordler\u200B"


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
            wordler_role = None
            for role in guild.roles:
                if role.name == _WORDLER_ROLE:
                    wordler_role = role
                    break

            if not wordler_role:
                wordler_role = await guild.create_role(
                    name=_WORDLER_ROLE, colour=discord.Colour.green())

            wordler_channel = None
            for channel in guild.text_channels:
                if channel.name == "wordle-spoilers":
                    wordler_channel = channel
                    break

            if wordler_channel:
                if wordler_channel.overwrites_for(
                        guild.default_role).read_messages != False:
                    await wordler_channel.set_permissions(guild.default_role,
                                                          read_messages=False)
                if wordler_channel.overwrites_for(
                        wordler_role).read_messages != True:
                    await wordler_channel.set_permissions(wordler_role,
                                                          read_messages=True)
            else:
                await guild.create_text_channel(
                    name="wordle-spoilers",
                    overwrites={
                        wordler_role:
                            discord.PermissionOverwrite(read_messages=True),
                        guild.default_role:
                            discord.PermissionOverwrite(read_messages=False),
                    })

    async def on_message(self, message: discord.Message):
        print(message.content)


if __name__ == "__main__":
    bot = Discordle()
    bot.run(os.environ["DISCORD_BOT_TOKEN"])

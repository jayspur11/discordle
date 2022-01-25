import discord

# Add a non-printing space to the end as a human-namespace-collision-avoider.
_WORDLER_ROLE = "wordler\u200B"


async def get_wordler_role(guild):
    wordler_role = None
    for role in guild.roles:
        if role.name == _WORDLER_ROLE:
            wordler_role = role
            break

    if not wordler_role:
        wordler_role = await guild.create_role(name=_WORDLER_ROLE,
                                               colour=discord.Colour.green())

    return wordler_role


async def configure_wordler_channel(guild, role):
    wordler_channel = None
    for channel in guild.text_channels:
        if channel.name == "wordle-spoilers":
            wordler_channel = channel
            break

    if wordler_channel:
        _configure_visibility(wordler_channel, guild.default_role, False)
        _configure_visibility(wordler_channel, role, True)
    else:
        await guild.create_text_channel(
            name="wordle-spoilers",
            overwrites={
                role:
                    discord.PermissionOverwrite(read_messages=True),
                guild.default_role:
                    discord.PermissionOverwrite(read_messages=False),
            })

    return wordler_channel


async def _configure_visibility(channel, role, read_messages):
    if channel.overwrites_for(role).read_messages != read_messages:
        await channel.set_permissions(role, read_messages=read_messages)

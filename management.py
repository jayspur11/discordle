import discord

_WORDLER_ROLE = "Wordled today"


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
        await _configure_visibility(wordler_channel, guild.default_role, False)
        await _configure_visibility(wordler_channel, role, True)
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


async def grant_wordler_role(message: discord.Message):
    wordler_role = await get_wordler_role(message.guild)
    await message.author.add_roles(wordler_role)


async def _configure_visibility(channel, role, read_messages):
    if channel.overwrites_for(role).read_messages != read_messages:
        await channel.set_permissions(role, read_messages=read_messages)

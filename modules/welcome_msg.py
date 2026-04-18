import discord

WELCOME_CHANNEL_ID = 1490653912707895432

ROLE_IDS = [
    1490823807290704063,
    1490823333577494568,
    1490823379866095626,
    1490823613929230446,
    1490823544056189000,
    1490823436602179747
]


async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)

    if channel is None:
        try:
            channel = await member.guild.fetch_channel(WELCOME_CHANNEL_ID)
        except (discord.NotFound, discord.Forbidden):
            print("Channel nicht gefunden oder kein Zugriff!")
            return

    try:
        await channel.send(f"👋 Willkommen auf dem Server, {member.mention}! Viel Spaß!")
    except discord.HTTPException as e:
        print(f"[Welcome] Nachricht konnte nicht gesendet werden: {e}")

    roles = []
    for role_id in ROLE_IDS:
        role = member.guild.get_role(role_id)
        if role:
            roles.append(role)

    if roles:
        try:
            await member.add_roles(*roles)
        except discord.HTTPException as e:
            print(f"[Welcome] Rollen konnten nicht vergeben werden: {e}")
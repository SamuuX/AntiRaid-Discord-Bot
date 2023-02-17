import discord
import requests
from discord.ext import commands
from AntiSpam import AntiSpamHandler
import os

TOKEN = os.getenv('TOKEN')

with open("bannedwords.txt", "r") as file:
    banned_words = file.read().strip().lower().split()
intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)
warn_embed_dict = {
    "title": "**Dear $USERNAME**",
    "description": "Stop spamming!",
    "timestamp": True,
    "color": 0xFF0000,
    "footer": {
        "text": "$BOTNAME Make sure to wait 60 seconds to avoid this warning",
        "icon_url": "$BOTAVATAR",
    },
    "author": {"name": "$GUILDNAME", "icon_url": "$GUILDICON"},
    "fields": [
        {"name": "Current warns:", "value": "$WARNCOUNT", "inline": False},
    ],
}
client.handler = AntiSpamHandler(
    client,
    ignore_roles=[1067139423352930365, 1067139050328301638],
    warn_only=True,
    message_duplicate_count=8,
    guild_warn_message=warn_embed_dict,
)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord")


# Use this if you want a specific person to not be tagged at all


@client.event
async def on_message(message):
    if "@UserName" in message.clean_content and message.author.bot is False:
        return
    else:
        print("I did it")
        await message.delete()
        bch = client.get_channel(1072034594485960715)
        embed = discord.Embed(title="Insert User Mentioned")
        embed.add_field(
            name=f"{message.author.name}:{message.author.id}",
            value=f"{message.content}",
        )
        await bch.send(embed=embed)
        wmessage = await message.channel.send(
            f"{message.author.mention} ¡No haga ping los nombre de usuario!"
        )
        await wmessage.delete(delay=10)
    if any(banned_word in message.content.strip().lower() for banned_word in banned_words):
        if message.author.bot == True:
            return
        else:
            bch = client.get_channel(1072034594485960715)
            embed = discord.Embed(title="Banned Word Detected")
            embed.add_field(
                name=f"{message.author.name}:{message.author.id}",
                value=f"{message.content}",
            )
            await bch.send(embed=embed)
            await message.delete()
            bmessage = await message.channel.send(
                f"{message.author.mention} That word is NOT permitted in this server! Proceed to use it and you will be banned!"
            )
            await bmessage.delete(delay=10)

    # This is to stop discord server links being posted in the server, if you do not wish to have it just put a # in front of "if" below
    if "discord.gg" in message.content.strip().lower():
        if message.author.bot == True:
            return
        elif message.channel == client.get_channel(1072034594485960715):
            return
        elif message.author.guild_permissions.administrator == True:
            return
        elif message.channel == client.get_channel(1072034594485960715):
            return
        else:
            bch = client.get_channel(1072034594485960715)
            embed = discord.Embed(title="Invite Deleted")
            embed.add_field(
                name=f"{message.author.name}:{message.author.id}",
                value=f"{message.content}",
            )
            await bch.send(embed=embed)
            await message.delete()
            bmessage = await message.channel.send(
                f"{message.author.mention} Sending another link will have you banned!"
            )
            await bmessage.delete(delay=10)
        await client.handler.propagate(message)
        await client.process_commands(message)

# Do NOT insert the token in the quotes below!
client.run(TOKEN)

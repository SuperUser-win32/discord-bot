from dotenv import load_dotenv
from discord.ext import commands
from discord import Embed, Member, Intents, Client, Color
from contextlib import suppress
import os
import logging

Bot_logger = logging.Logger("discord.bot")
Formatter = logging.Formatter("%(asctime)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("logs.log")
stream_handler = logging.StreamHandler()
file_handler.setFormatter(Formatter)
stream_handler.setFormatter(Formatter)
Bot_logger.addHandler(file_handler)
Bot_logger.addHandler(stream_handler)

load_dotenv()

client = Client(intents=Intents.all())
bot_user_id = int(os.getenv("BOT_USER_ID"))
welcoming_channel_id = int(os.getenv("WELCOMING_CHANNEL_ID"))

bot = commands.Bot("!", intents=Intents.all())


async def send_to_channel(channel_id: int, *args, **kwargs) -> None:
    channel = client.get_channel(channel_id)
    await channel.send(*args, **kwargs)


@client.event
async def on_ready():
    Bot_logger.info("The bot has started")


@client.event
async def on_member_remove(member: Member):
    embed_sent = Embed(
        title=f"Bye {member.name}",
        description="We wish you the best",
        color=Color.dark_red(),
    )
    with suppress(AttributeError):
        embed_sent.set_thumbnail(url=member.avatar.url)
    await send_to_channel(welcoming_channel_id, embed=embed_sent)


@client.event
async def on_member_join(member: Member):
    embed_sent = Embed(
        title=f"Welcome {member.name}",
        description="We welcome you into the server",
        color=Color.dark_blue(),
    )
    with suppress(AttributeError):
        embed_sent.set_thumbnail(url=member.avatar.url)
    await send_to_channel(welcoming_channel_id, embed=embed_sent)


client.run(os.getenv("DISCORD_API_KEY"), log_formatter=Formatter)

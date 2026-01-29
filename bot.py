from dotenv import load_dotenv
from discord.ext import commands
from discord import Embed, Member, Intents, Color
from contextlib import suppress
from functools import lru_cache
import random
import json
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


bot_user_id = int(os.getenv("BOT_USER_ID"))
welcoming_channel_id = int(os.getenv("WELCOMING_CHANNEL_ID"))

bot = commands.Bot("!", intents=Intents.all())


@lru_cache
def get_joke(id: int, source_file: str = "data.json") -> str:
    try:
        with open(source_file, "r", encoding="utf-8") as f:
            return json.load(f)["jokes"][id]
    except OSError:
        return "There is no jokes available at the moment"


@lru_cache
def get_meme(id: int, source_file: str = "data.json") -> str:
    try:
        with open(source_file, "r", encoding="utf-8") as f:
            return json.load(f)["memes"][id]
    except OSError:
        return "There is no memes available at the moment"


async def send_to_channel(channel_id: int, *args, **kwargs) -> None:
    channel = bot.get_channel(channel_id)
    await channel.send(*args, **kwargs)


@bot.event
async def on_ready():
    Bot_logger.info("The bot has started")


@bot.event
async def on_member_remove(member: Member) -> None:
    embed_sent = Embed(
        title=f"Bye {member.name}",
        description="We wish you the best",
        color=Color.dark_red(),
    )
    with suppress(AttributeError):
        embed_sent.set_thumbnail(url=member.avatar.url)
    await send_to_channel(welcoming_channel_id, embed=embed_sent)


@bot.event
async def on_member_join(member: Member) -> None:
    embed_sent = Embed(
        title=f"Welcome {member.name}",
        description="We welcome you into the server",
        color=Color.dark_blue(),
    )
    with suppress(AttributeError):
        embed_sent.set_thumbnail(url=member.avatar.url)
    await send_to_channel(welcoming_channel_id, embed=embed_sent)


@bot.event
async def on_error(event, *args, **kwargs) -> None:
    Bot_logger.info(f"error at {event} && {args} && {kwargs}")


@bot.command(description="bans a list of users from the server")
@commands.has_permissions(administrator=True)
async def mass_ban(ctx: commands.context.Context, *users: Member) -> None:
    for user in users:
        await user.ban()
        await user.send(f">> You got banned by {ctx.author.name}")


@bot.command(description="bans a user from the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.context.Context, user: Member) -> None:
    await user.ban()
    await user.send(f">> You got banned by {ctx.author.name}")


@bot.command(description="kicks a user from the server")
@commands.has_permissions(administrator=True)
async def kick(ctx: commands.context.Context, user: Member) -> None:
    await user.kick()
    await user.send(f">> You got kicked by {ctx.author.name}")


@bot.command(description="mute a user from the server")
@commands.has_permissions(administrator=True)
async def mute(ctx: commands.context.Context, user: Member) -> None:
    await user.edit(mute=True)
    await ctx.send(f">> You got muted by {ctx.author.name}", ephemeral=True)


@bot.command(description="unmute a user from the server")
@commands.has_permissions(administrator=True)
async def unmute(ctx: commands.context.Context, user: Member) -> None:
    await user.edit(mute=False)
    await ctx.send(f">> You got unmuted by {ctx.author.name}", ephemeral=True)


@bot.command(description="gets you the bots lentency")
async def ping(ctx: commands.context.Context) -> None:
    if ctx.channel.id == 1465016548908601446:
        await ctx.send(f">> bot's lentency : {bot.latency * 1000}ms", ephemeral=True)


@bot.command(description="sends a joke")
async def joke(ctx: commands.context.Context) -> None:
    if ctx.channel.id == 1465016548908601446:
        await ctx.send(get_joke(random.randrange(0, 20)))


@bot.command(description="sends a meme")
async def meme(ctx: commands.context.Context) -> None:
    if ctx.channel.id == 1465016548908601446:
        await ctx.send(get_meme(random.randrange(0, 13)))


@bot.command()
async def serverinfo(ctx: commands.context.Context) -> None:
    if ctx.channel.id == 1465016548908601446:
        embed = Embed(
            title="Serverinfo",
            color=Color.dark_blue(),
        )
        embed.add_field(name="server name", value=ctx.guild.name)
        embed.add_field(name="member count", value=ctx.guild.member_count)
        embed.add_field(
            name="roles", value=" - ".join(map(str, ctx.guild.roles)), inline=False
        )
        await ctx.send(embed=embed, ephemeral=True)


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_API_KEY"), log_formatter=Formatter)
    Bot_logger.info("The bot has shutdowned")

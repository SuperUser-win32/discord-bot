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


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.guild is not None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mass_ban(self, ctx: commands.context.Context, *users: Member) -> None:
        for user in users:
            await user.ban()
            await user.send(f">> You got banned by {ctx.author.name}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.context.Context, user: Member) -> None:
        await user.ban()
        await user.send(f">> You got banned by {ctx.author.name}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx: commands.context.Context, user: Member) -> None:
        await user.kick()
        await user.send(f">> You got kicked by {ctx.author.name}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx: commands.context.Context, user: Member) -> None:
        await user.edit(mute=True)
        await ctx.send(f">> You got muted by {ctx.author.name}", ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx: commands.context.Context, user: Member) -> None:
        await user.edit(mute=False)
        await ctx.send(f">> You got unmuted by {ctx.author.name}", ephemeral=True)


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.guild is not None

    @commands.command()
    async def joke(self, ctx: commands.context.Context) -> None:
        if ctx.channel.id == 1465016548908601446:
            await ctx.send(get_joke(random.randrange(0, 20)))

    @commands.command()
    async def meme(self, ctx: commands.context.Context) -> None:
        if ctx.channel.id == 1465016548908601446:
            await ctx.send(get_meme(random.randrange(0, 13)))


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.guild is not None

    @commands.command()
    async def serverinfo(self, ctx: commands.context.Context) -> None:
        if ctx.channel.id == 1465016548908601446:
            embed = Embed(
                title="Serverinfo",
                color=Color.dark_blue(),
            )
            with suppress(AttributeError):
                embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.add_field(name="server name", value=ctx.guild.name)
            embed.add_field(name="member count", value=ctx.guild.member_count)
            embed.add_field(
                name="roles", value=" - ".join(map(str, ctx.guild.roles)), inline=False
            )
            await ctx.send(embed=embed, ephemeral=True)

    @commands.command()
    async def userinfo(self, ctx: commands.context.Context, member: Member) -> None:
        if ctx.channel.id == 1465016548908601446:
            embed = Embed(
                title="Userinfo",
                color=Color.dark_blue(),
            )
            with suppress(AttributeError):
                embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="name", value=member.name)
            embed.add_field(
                name="roles",
                value=" - ".join(map(str, member.roles)),
                inline=False,
            )
            await ctx.send(embed=embed, ephemeral=True)


class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.guild is not None

    @commands.command()
    async def ping(self, ctx: commands.context.Context) -> None:
        if ctx.channel.id == 1465016548908601446:
            await ctx.send(
                f">> bot's lentency : {bot.latency * 1000}ms", ephemeral=True
            )


@bot.event
async def on_ready():
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(Utility(bot))
    await bot.add_cog(Fun(bot))
    await bot.add_cog(General(bot))
    Bot_logger.info("The bot has started")


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_API_KEY"), log_formatter=Formatter)
    Bot_logger.info("The bot has shutdowned")

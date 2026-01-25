from dotenv import load_dotenv
import os
import discord
import logging

Bot_logger = logging.Logger("DISCORD-BOT")
Formatter = logging.Formatter("%(asctime)s | %(name)s | %(message)s")
file_handler = logging.FileHandler("logs.log")
stream_handler = logging.StreamHandler()
file_handler.setFormatter(Formatter)
stream_handler.setFormatter(Formatter)
Bot_logger.addHandler(file_handler)
Bot_logger.addHandler(stream_handler)

load_dotenv()

client = discord.Client(discord.Intents.all())


@client.event
async def on_ready():
    Bot_logger.info("The bot has started")


client.run(os.getenv("DISCORD_API_KEY"))

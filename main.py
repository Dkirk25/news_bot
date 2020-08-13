import os
import discord
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()


@client.event
async def on_ready():
    channel = client.get_channel(os.getenv("CHANNEL_ID"))
    # Call stock news and return list of stock info

    # Read history of discord chat and save the last 10 messages

    # check last article published_at by the bot

    # if any of the published_at in stock info list is newer than the last message in discord chat, then post stock info in chat

    # Send stock news to discord channel
    await channel.send('hello')


client.run(os.getenv("TOKEN"))

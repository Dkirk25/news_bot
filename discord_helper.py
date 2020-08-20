import discord
from datetime import datetime
import os

BOT_NAME = os.getenv("BOT_NAME")


def create_embed(new_stock_info):
    embed = discord.Embed(
        title=new_stock_info.title,
        description=new_stock_info.text,
        url=new_stock_info.url
    )
    embed.set_author(name=new_stock_info.author +
                     ", " + new_stock_info.stock_name)
    return embed


async def get_bot_messages(channel):
    # Read history of discord chat and save the last 10 messages
    messages = await channel.history(limit=100).flatten()

    # Get only news-bot messages
    news_bot_messages = []
    if(len(messages) > 0):
        [news_bot_messages.append(
            message) for message in messages if message.author.name == BOT_NAME]
    return remove_empty_embed_messages(news_bot_messages)


def remove_empty_embed_messages(dirty_messages):
    clean_discord_messages = []
    [clean_discord_messages.append(message) for message in dirty_messages if len(
        message.embeds) > 0 and message.embeds[0] is not None]
    return clean_discord_messages


def get_clean_date(dirty_date):
    clean_date = dirty_date.replace(
        "-", "/").replace("T", " ").replace("Z", "")
    print(clean_date)
    stock_date = datetime.strptime(
        clean_date, '%Y/%m/%d %H:%M:%S')
    return stock_date

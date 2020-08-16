import discord
from pyrh import Robinhood
from datetime import datetime
from model.news import StockInfo
import sys
import numpy as np
import tulipy as ti
import schedule
import time
import pyotp
import os
import asyncio
from dotenv import load_dotenv
load_dotenv(override=True)

client = discord.Client()

MFA = os.getenv("MFA")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

totp = pyotp.TOTP(MFA).now()
rh = Robinhood()
rh.login(username=USERNAME,
         password=PASSWORD,
         qr_code=MFA)

# Add scheduler to discord bot to run every hour???
# https://www.youtube.com/watch?v=rWAnKvI2ePI


def get_channel(channels, channel_name):
    for channel in client.get_all_channels():
        # print(channel)
        if channel.name == channel_name:
            return channel
    return None


def fetch_news():
    print("Getting news\n")

    news = rh.get_news("WKHS")
    info_results = news["results"]
    clean_stock_list = []
    for i in info_results:
        stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                               i["preview_text"].replace("\n\n", ""), i["url"])
        print(str(stock_info))
        clean_stock_list.append(stock_info)
    return clean_stock_list


@client.event
async def on_ready():
    print("Bot is ready")
    await client.wait_until_ready()

    channel = get_channel(client.get_all_channels(), 'general')

    # Call stock news and return list of stock info
    stock_info_list = fetch_news()

    # Read history of discord chat and save the last 10 messages
    messages = await channel.history(limit=5).flatten()

    news_bot_messages = []
    for message in messages:
        if(message.author.name == "news-bot"):
            news_bot_messages.append(message)

    # check last article published_at by the bot
    latest_discord_message = news_bot_messages[0]
    print(latest_discord_message)

    # latest discord message is older than stock
    latest_stock = stock_info_list[0]
    clean_date = latest_stock.published_at.replace(
        "-", "/").replace("T", " ").replace("Z", "")
    print(clean_date)
    stock_date = datetime.strptime(
        clean_date, '%Y/%m/%d %H:%M:%S')

    if(stock_date > latest_discord_message.created_at):
        # if any of the published_at in stock info list is newer than the last message in discord chat, then post stock info in chat

        # Create embed then post stock info
        embed = discord.Embed(
            title=latest_stock.title,
            description=latest_stock.text,
            url=latest_stock.url
        )
        embed.set_author(name=latest_stock.author)
        # Send stock news to discord channel
        await channel.send(embed=embed)


client.run(os.getenv("TOKEN"))

# schedule.every(1).minutes.do(fetch_news)
# schedule.every().minute.at("1:00").do(fetch_news)

# while True:
#     schedule.run_all()
# time.sleep(1)

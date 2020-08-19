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

BOT_NAME = os.getenv("BOT_NAME")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

totp = pyotp.TOTP(MFA).now()
rh = Robinhood()
rh.login(username=USERNAME,
         password=PASSWORD,
         qr_code=MFA)

# Bot commands to add and remove stocks to get news.

# PREFIX = "$"
# bot = commands.Bot(command_prefix=PREFIX, self_bot=True)


async def get_channel(channels, channel_name):
    for channel in client.get_all_channels():
        if channel.name == channel_name:
            return channel
    return None


async def fetch_news(stock):
    print("Getting news\n")

    stock_to_search = stock
    news = rh.get_news(stock_to_search)
    info_results = news["results"]
    clean_stock_list = []
    for i in info_results:
        stock_info = StockInfo(i["uuid"], i["title"], i["source"], i["published_at"],
                               i["preview_text"].replace("\n\n", ""), i["url"], stock_to_search)
        print(str(stock_info))
        clean_stock_list.append(stock_info)
    return clean_stock_list


def get_clean_date(dirty_date):
    clean_date = dirty_date.replace(
        "-", "/").replace("T", " ").replace("Z", "")
    print(clean_date)
    stock_date = datetime.strptime(
        clean_date, '%Y/%m/%d %H:%M:%S')
    return stock_date


def list_of_news_bot_messages(messages):
    news_bot_messages = []
    return list(news_bot_messages.append(
        message) for message in messages if message.author.name == BOT_NAME)


def create_embed(new_stock_info):
    embed = discord.Embed(
        title=new_stock_info.title,
        description=new_stock_info.text,
        url=new_stock_info.url
    )
    embed.set_author(name=new_stock_info.author)
    return embed


async def post_news_info():
    await client.wait_until_ready()
    while(True):
        channel = await get_channel(client.get_all_channels(), CHANNEL_NAME)

        # Read history of discord chat and save the last 10 messages
        messages = await channel.history(limit=10).flatten()

        # Get only news-bot messages
        news_bot_messages = []
        clean_date = ""
        if(len(messages) > 0):
            [news_bot_messages.append(
                message) for message in messages if message.author.name == BOT_NAME]

            list_of_searched_stocks = ["WKHS", "AYRO", "GLUU"]
            for stock in list_of_searched_stocks:
                # Call stock news and return list of stock info
                stock_info_list = await fetch_news(stock)

                # check last article published_at by the bot
                if(len(news_bot_messages) > 0 and len(stock_info_list) > 0):
                    # Check through list of stocks and see if stock_name == stock
                    for discord_message in news_bot_messages:
                        # if equals stock name, then compare....
                        if(stock_info_list[0].stock_name == discord_message.stock_name):
                            # latest discord message is older than stock
                            latest_stock = stock_info_list[0]
                            clean_date = get_clean_date(
                                latest_stock.published_at)
                            # if any of the published_at in stock info list is newer than the last message in discord chat, then post stock info in chat
                            if(clean_date > discord_message.created_at):
                                # Send stock news to discord channel
                                await channel.send(embed=create_embed(latest_stock))
            # Play every 10min of seconds
            await asyncio.sleep(600)

# @bot.command(pass_context=True, aliases=['a'])
# async def add_stock(ctx, *args):


# @bot.command(pass_context=True, aliases=['r'])
# async def remove_stock(ctx, *args):


@client.event
async def on_ready():
    print("Bot is ready")


client.loop.create_task(post_news_info())
client.run(os.getenv("TOKEN"))

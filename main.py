import discord
from discord.ext import commands
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

list_of_searched_stocks = ["GEVO", "F", "WKHS", "AYRO", "GLUU"]


async def get_channel(channels, channel_name):
    for channel in client.get_all_channels():
        if channel.name == channel_name:
            return channel
    return None


async def fetch_news(stock):
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
    return news_bot_messages


def remove_empty_embed_messages(dirty_messages):
    clean_discord_messages = []
    [clean_discord_messages.append(message) for message in dirty_messages if len(
        message.embeds) > 0 and message.embeds[0] is not None]
    return clean_discord_messages


async def post_news_info():
    await client.wait_until_ready()
    while(True):
        print(list_of_searched_stocks)
        for stock in list_of_searched_stocks:
            # Call stock news and return list of stock info
            stock_info_list = await fetch_news(stock)
            # If there is no news, go to next stock
            if(len(stock_info_list) > 0):
                stock_info = stock_info_list[0]
                channel = await get_channel(client.get_all_channels(), "test")
                dirty_list = await get_bot_messages(channel)
                news_bot_messages = remove_empty_embed_messages(dirty_list)

                if(stock_info is not None):
                    if(len(news_bot_messages) == 0):
                        await channel.send(embed=create_embed(stock_info))
                    elif(len(news_bot_messages) > 0):
                        # Check through list of stocks and see if stock_name == stock
                        count = 0
                        for discord_message in news_bot_messages:
                            # if equals stock name, then compare....
                            embed_from_message = discord_message.embeds[0]
                            if(stock_info.stock_name in embed_from_message.author.name):
                                if(get_clean_date(stock_info.published_at) > discord_message.created_at):
                                    await channel.send(embed=create_embed(stock_info))
                            else:
                                count = count + 1
                        if(count == len(news_bot_messages)):
                            await channel.send(embed=create_embed(stock_info))
        # Play every 10min of seconds
        await asyncio.sleep(20)


@ client.event
async def on_message(message):
    await client.wait_until_ready()
    channel = await get_channel(client.get_all_channels(), "test")
    # do some extra stuff here
    print("I'm here")
    if(message.content.startswith(".add")):
        msg = message.content.split()
        if(msg[1] not in list_of_searched_stocks):
            list_of_searched_stocks.append(msg[1])
            await channel.send(msg[1] + " was added to watch list!")
        else:
            await channel.send(msg[1] + " is already in watch list!")
    elif(message.content.startswith(".remove")):
        msg = message.content.split()
        list_of_searched_stocks.remove(msg[1])
        await channel.send(msg[1] + " was removed to watch list!")
    elif(message.content.startswith(".list")):
        output = ''
        for stock in list_of_searched_stocks:
            output += stock
            output += "\n"
        await channel.send("Stocks that are being watched:\n" + output)


client.loop.create_task(post_news_info())
client.run(os.getenv("TOKEN"))

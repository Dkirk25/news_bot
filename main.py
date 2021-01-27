from discord.ext import commands
import discord
from pyrh import Robinhood
from datetime import datetime
from model.news import StockInfo
from stock_helper import StockHelper
import database
from discord_helper import DiscordHelper
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
discord_helper = DiscordHelper()
stock_helper = StockHelper()


def get_channel():
    channel_id = int(os.getenv("CHANNEL_ID"))
    return client.get_channel(channel_id)


async def validate_stock(channel, stock_info, list_discord_messages):
    if discord_helper.is_stock_info_already_posted(stock_info, list_discord_messages):
        await channel.send(embed=discord_helper.create_embed(stock_info))


async def post_news_info():
    try:
        await client.wait_until_ready()
        while(True):
            list_of_searched_stocks = database.get_stocks()
            for stock in list_of_searched_stocks:
                # Call stock news and return list of stock info
                stock_info_list = await stock_helper.fetch_news(stock)
                # If there is no news, go to next stock
                if(len(stock_info_list) > 0):
                    stock_info = stock_info_list[0]
                    channel = get_channel()
                    news_bot_messages = await discord_helper.get_bot_messages(channel)

                    if(stock_info is not None):
                        await validate_stock(channel, stock_info, news_bot_messages)
            # Play every 10min of seconds
            await asyncio.sleep(int(os.getenv("POLL_INTERVAL", "600")))
    except Exception as ex:
        print(ex)


@client.event
async def on_message(message):
    await client.wait_until_ready()

    if (message.author.bot):
        return
    channel = get_channel()
    if(message.content.startswith(".add")):
        msg = message.content.split()
        database.add_stock(msg[1].upper())
        await channel.send(msg[1].upper() + " was added to watch list!")
    elif(message.content.startswith(".remove")):
        msg = message.content.split()
        database.remove_stock(msg[1].upper())
        await channel.send(msg[1].upper() + " was removed from the watch list!")
    elif(message.content.startswith(".list")):
        output = ''
        list_of_searched_stocks = database.get_stocks()
        for stock in list_of_searched_stocks:
            output += stock
            output += "\n"
        await channel.send("Stocks that are being watched:\n" + output)
    elif(message.content.startswith(".help")):
        output = ''
        list_of_commands = [".add <stock>", ".remove <stock>", ".list"]
        for stock in list_of_commands:
            output += stock
            output += "\n"
        await channel.send("Here are the commands:\n" + output)
    elif(message.content.startswith(".purge")):
        non_bot_messages = await discord_helper.get_non_bot_messages(channel)
        await discord_helper.delete_messages_channel(message.channel, non_bot_messages)


client.loop.create_task(post_news_info())
client.run(os.getenv("TOKEN"))

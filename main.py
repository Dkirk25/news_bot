from discord.ext import commands
import discord
from pyrh import Robinhood
from datetime import datetime
from model.news import StockInfo
import stock_helper
import discord_helper
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

list_of_searched_stocks = ["GEVO", "Tesla", "WKHS", "AYRO", "GLUU"]


def get_channel():
    channel_id = int(os.getenv("CHANNEL_ID"))
    return client.get_channel(channel_id)


async def post_news_info():
    await client.wait_until_ready()
    while(True):
        print(list_of_searched_stocks)
        for stock in list_of_searched_stocks:
            # Call stock news and return list of stock info
            stock_info_list = await stock_helper.fetch_news(stock)
            # If there is no news, go to next stock
            if(len(stock_info_list) > 0):
                stock_info = stock_info_list[0]
                channel = get_channel()
                news_bot_messages = await discord_helper.get_bot_messages(channel)

                if(stock_info is not None):
                    if(len(news_bot_messages) == 0):
                        await channel.send(embed=discord_helper.create_embed(stock_info))
                    elif(len(news_bot_messages) > 0):
                        # Check through list of stocks and see if stock_name == stock
                        count = 0
                        for discord_message in news_bot_messages:
                            # if equals stock name, then compare....
                            embed_from_message = discord_message.embeds[0]
                            if(stock_info.stock_name in embed_from_message.author.name):
                                if(discord_helper.get_clean_date(stock_info.published_at) > discord_message.created_at):
                                    await channel.send(embed=discord_helper.create_embed(stock_info))
                            else:
                                count = count + 1
                        if(count == len(news_bot_messages)):
                            await channel.send(embed=discord_helper.create_embed(stock_info))
        # Play every 10min of seconds
        await asyncio.sleep(20)


@ client.event
async def on_message(message):
    await client.wait_until_ready()

    if (message.author.bot):
        return
    channel = get_channel()
    # do some extra stuff here
    print("I'm here")
    if(message.content.startswith(".add")):
        msg = message.content.split()
        if(msg[1] not in list_of_searched_stocks):
            list_of_searched_stocks.append(msg[1].upper())
            await channel.send(msg[1].upper() + " was added to watch list!")
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
    elif(message.content.startswith(".help")):
        output = ''
        list_of_commands = [".add <stock>", ".remove <stock>", ".list"]
        for stock in list_of_commands:
            output += stock
            output += "\n"
        await channel.send("Here are the commands:\n" + output)

client.loop.create_task(post_news_info())
client.run(os.getenv("TOKEN"))

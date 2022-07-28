import asyncio
import os
import time

import discord
from dotenv import load_dotenv

from database_builder import DatabaseBuilder
from discord_helper import DiscordHelper
from news_builder import NewsBuilder

load_dotenv(override=True)

database = DatabaseBuilder().get_db()
discord_helper = DiscordHelper()
client = discord.Client()
factory = NewsBuilder().get_news_helper()


def get_channel():
    channel_id = int(os.getenv("CHANNEL_ID"))
    return client.get_channel(channel_id)


async def post_news_info():
    try:
        await client.wait_until_ready()
        while True:
            list_of_searched_stocks = database.get_stocks()
            for stock in list_of_searched_stocks:
                # Call stock news and return list of stock info
                stock_info_list = factory.fetch_news(stock)
                # If there is no news, go to next stock
                if len(stock_info_list) > 0:
                    stock_info = stock_info_list[0]
                    channel = get_channel()
                    news_bot_messages = await discord_helper.get_bot_messages(channel)

                    if (stock_info is not None and
                            discord_helper.is_stock_info_already_posted(stock_info, news_bot_messages) and
                            discord_helper.is_newer_date(discord_helper.get_clean_date(stock_info.published_at))):
                        await channel.send(embed=discord_helper.create_embed(stock_info))
            # Play every 10min of seconds
            await asyncio.sleep(int(os.getenv("POLL_INTERVAL", "600")))
    except Exception as ex:
        print("Error happened while fetching stock info: ", ex)


@client.event
async def on_message(message):
    await client.wait_until_ready()

    if message.author.bot:
        return
    channel = get_channel()
    if message.content.startswith(".add"):
        msg = message.content.split()
        database.add_stock(msg[1].upper())
        await channel.send(msg[1].upper() + " was added to watch list!")
    elif message.content.startswith(".remove"):
        msg = message.content.split()
        database.remove_stock(msg[1].upper())
        await channel.send(msg[1].upper() + " was removed from the watch list!")
    elif message.content.startswith(".list"):
        output = ''
        list_of_searched_stocks = database.get_stocks()
        for stock in list_of_searched_stocks:
            output += stock
            output += "\n"
        await channel.send("Stocks that are being watched:\n" + output)
    elif message.content.startswith(".help"):
        output = ''
        list_of_commands = [".add <stock>", ".remove <stock>", ".list"]
        for stock in list_of_commands:
            output += stock
            output += "\n"
        await channel.send("Here are the commands:\n" + output)
    elif message.content.startswith(".purge"):
        non_bot_messages = await discord_helper.get_non_bot_messages(channel)
        old_bot_messages = await discord_helper.get_old_messages(channel)
        # remove news messages that are more than 7 days old
        await discord_helper.delete_messages_channel(message.channel, non_bot_messages)
        await discord_helper.delete_messages_channel(message.channel, old_bot_messages)
        print("done with all")


def start_script():
    try:
        client.loop.create_task(post_news_info())
        client.run(os.getenv("TOKEN"))
    except Exception as e:
        print("Error in script, trying to restart:", e)
        handle_crash()


def handle_crash():
    time.sleep(10)
    start_script()


while True:
    start_script()

import asyncio
import os
import time

import discord
from discord import app_commands
from dotenv import load_dotenv

from database_builder import DatabaseBuilder
from discord_helper import DiscordHelper
from my_client import MyClient
from news_builder import NewsBuilder

load_dotenv(override=True)

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

database = DatabaseBuilder().get_db()
discord_helper = DiscordHelper()
factory = NewsBuilder().get_news_helper()
channel_id = int(os.getenv("CHANNEL_ID"))


def get_channel():
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


# @client.event
# async def on_message(message):
#     await client.wait_until_ready()
#
#     if message.author.bot:
#         return
# channel = get_channel()
# if message.content.startswith(".add"):
#     msg = message.content.split()
#     database.add_stock(msg[1].upper())
#     await channel.send(msg[1].upper() + " was added to watch list!")
# elif message.content.startswith(".remove"):
#     msg = message.content.split()
#     database.remove_stock(msg[1].upper())
#     await channel.send(msg[1].upper() + " was removed from the watch list!")
# elif message.content.startswith(".list"):
#     output = ''
#     list_of_searched_stocks = database.get_stocks()
#     for stock in list_of_searched_stocks:
#         output += stock
#         output += "\n"
#     await channel.send("Stocks that are being watched:\n" + output)
# elif message.content.startswith(".help"):
#     output = ''
#     list_of_commands = [".add <stock>", ".remove <stock>", ".list"]
#     for stock in list_of_commands:
#         output += stock
#         output += "\n"
#     await channel.send("Here are the commands:\n" + output)
# elif message.content.startswith(".purge"):
#     non_bot_messages = await discord_helper.get_non_bot_messages(channel)
#     old_bot_messages = await discord_helper.get_old_messages(channel)
#     # remove news messages that are more than 7 days old
#     await discord_helper.delete_messages_channel(message.channel, non_bot_messages)
#     await discord_helper.delete_messages_channel(message.channel, old_bot_messages)
#     print("done with all")


# @client.command()
@tree.command(name="add", description="Add a stock by it's ticker value")
async def add(interaction: discord.Interaction, message: discord.Message):
    msg = message.content.split()
    database.add_stock(msg[1].upper())
    await interaction.response.send_message(msg[1].upper() + " was added to watch list!")


@tree.command(name="remove", description="Add a stock by it's ticker value")
async def remove(interaction: discord.Interaction, message: discord.Message):
    msg = message.content.split()
    database.remove_stock(msg[1].upper())
    await interaction.response.send_message(msg[1].upper() + " was removed from the watch list!")


# This context menu command only works on messages
@tree.command(name="help", description="Add a stock by it's ticker value")
async def new_help(interaction: discord.Interaction):
    embed = discord.Embed(title='Help Menu', description="Here are a list of commands to use",
                          color=discord.Color.random())

    embed.set_field_at(name="add <stock>", value="Add a stock by it's ticker value")
    embed.set_field_at(name="remove <stock>", value="deletes a stock by it's ticker value")
    embed.set_field_at(name="list", value="view the list of tickers that are being watched")

    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="purge", description="Add a stock by it's ticker value")
async def purge(message: discord.Message):
    non_bot_messages = await discord_helper.get_non_bot_messages(channel_id)
    old_bot_messages = await discord_helper.get_old_messages(channel_id)
    # remove news messages that are more than 7 days old
    await discord_helper.delete_messages_channel(message.channel, non_bot_messages)
    await discord_helper.delete_messages_channel(message.channel, old_bot_messages)
    print("done with all")


@tree.command(name="list", description="view the list of tickers that are being watched")
async def list_of_tickers(interaction: discord.Interaction):
    output = ''
    list_of_searched_stocks = database.get_stocks()
    for stock in list_of_searched_stocks:
        output += stock
        output += "\n"
    await interaction.response.send_message("Stocks that are being watched:\n" + output)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


async def start_script():
    async with client:
        try:
            client.loop.create_task(post_news_info())
            await client.start(os.getenv("TEST_TOKEN_ID"))
        except Exception as e:
            print("Error in script, trying to restart:", e)
            handle_crash()


def handle_crash():
    time.sleep(10)
    start_script()


while True:
    asyncio.run(start_script())

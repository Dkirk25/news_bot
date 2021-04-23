import discord
from datetime import datetime
from pytz import timezone
import os


class DiscordHelper:
    def __init__(self):
        self._bot_name = os.getenv("BOT_NAME")

    def create_embed(self, new_stock_info):
        embed = discord.Embed(
            title=new_stock_info.title,
            description=new_stock_info.text,
            url=new_stock_info.url,
            timestamp=self.get_clean_date(new_stock_info.published_at)
        )
        embed.set_author(name=new_stock_info.author +
                         ", " + new_stock_info.stock_name+" (" + new_stock_info.stock_price + ")")
        return embed

    async def delete_messages_channel(self, channel, list_of_messages):
        try:
            await channel.delete_messages(list_of_messages)
        except Exception as e:
            print("Error: ", e, "Occurred.")
            print("Deleting one by one...")
            print(len(list_of_messages))
            for msg in list_of_messages:
                try:
                    await msg.delete()
                except Exception as e:
                    pass
            print("done")

    async def get_non_bot_messages(self, channel):
        messages = await channel.history(limit=100).flatten()
        non_bot_messages = []
        [non_bot_messages.append(message)
         for message in messages if message.author.name != self._bot_name]
        return non_bot_messages

    async def get_bot_messages(self, channel):
        messages = await channel.history(limit=100).flatten()

        # Get only news-bot messages
        news_bot_messages = []
        if(len(messages) > 0):
            [news_bot_messages.append(
                message) for message in messages if message.author.name == self._bot_name]
        return await self.remove_empty_embed_messages(news_bot_messages)

    async def remove_empty_embed_messages(self, dirty_messages):
        clean_discord_messages = []
        [clean_discord_messages.append(message) for message in dirty_messages if len(
            message.embeds) > 0 and message.embeds[0] is not None]
        return clean_discord_messages

    def get_clean_date(self, dirty_date):
        clean_date = dirty_date.replace(
            "-", "/").replace("T", " ").replace("Z", "")

        stock_date = ""

        if("/" in clean_date):
            stock_date = datetime.strptime(clean_date, '%Y/%m/%d %H:%M:%S')
        else:
            stock_date = datetime.strptime(clean_date, '%B %d, %Y, %H:%M %p')

        CT = timezone('America/Chicago')

        return CT.localize(stock_date, is_dst=None)

    def is_stock_info_already_posted(self, stock_info, list_of_messages):
        list_of_embed_messages = []
        [list_of_embed_messages.append(message.embeds[0]) for message in list_of_messages if len(
            message.embeds) > 0 and message.embeds[0] is not None]

        filtered_stock_list = list(filter(
            lambda x: stock_info.stock_name in x.author.name, list_of_embed_messages))

        filtered_even_more = list(filter(
            lambda x: stock_info.title in x.title, filtered_stock_list))

        if(len(filtered_even_more) == 0):
            return True
        return False

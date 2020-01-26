from django.core.management.base import BaseCommand, CommandError

import os

import discord
import time
from discord_bot.custom_search_engine import google_search
from discord_bot.search_result_formatter import google_search_result_formatter
from discord_bot.search_history import UserSearchHistory
# from discord_bot.search_history import save_user_search, get_data_from_history

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.author, client.user)
    welcome_msg_conf = {
        'hi': 'hey'
    }
    query = message.content.lower()
    if query in welcome_msg_conf:
        await message.channel.send(welcome_msg_conf.get(query))
        return

    search_history_service = UserSearchHistory(message.author)
    if query.startswith('!google '):
        query = query[8:]
        search_history_service.save_user_search(search_term=query)
        search_response = google_search(search_term=query, num=5)
        if not search_response:
            await message.channel.send("Something went wrong..Please try again")
            return
        response = google_search_result_formatter(search_response)
        await message.channel.send(response)
    elif query.startswith('!recent '):
        query = query[8:]
        result = search_history_service.get_data_from_history(key=query)
        if not result:
            await message.channel.send("No recent data found for it.")
            return
        response = '\n'.join(result)
        await message.channel.send(response)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('jsr')
        while True:
            try:
                client.run(TOKEN)
            except Exception as e:
                print(f"Error: {str(e)}")
                time.sleep(3)

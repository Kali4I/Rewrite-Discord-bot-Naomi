import os
import sys
import time
import asyncio
import traceback

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='n!')
bot.remove_command('help')

_cogs = ['cogs.member',
         'cogs.admin',
         'cogs.owner',
         'cogs.music',
         'cogs.logger']

if __name__ == '__main__':
    for extension in _cogs:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'[{time.ctime()}] Не удалось загрузить модуль {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    log(f'[{time.ctime()}] Подключение успешно осуществлено!\nВ сети: {bot.user}')

    async def __presence():
        _sleeping = 12
        while not bot.is_closed():
            await client.change_presence(activity=discord.Streaming(name=f'{len(bot.guilds)} серверов!', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(_sleeping)
            await client.change_presence(activity=discord.Streaming(name=f'{len(bot.users)} пользователей!', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(_sleeping)
            await client.change_presence(activity=discord.Streaming(name=f'{len(bot.emojis)} эмодзи!', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(_sleeping)
            await client.change_presence(activity=discord.Streaming(name=f'{len(bot.all_commands)} команд!', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(_sleeping)
            await client.change_presence(activity=discord.Streaming(name=f'n!help', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(_sleeping)
    bot.loop.create_task(__presence())

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)
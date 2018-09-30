import os
import sys
import time
import asyncio
import traceback
import aiohttp

import discord
from discord.ext import commands

prefix = os.getenv("PREFIX")

bot = commands.Bot(command_prefix=prefix)

async def start_session():
    bot.session = aiohttp.ClientSession()

bot.remove_command('help')

extensions = ['cogs.member.fun',
              'cogs.member.info',
              'cogs.member.music',
              'cogs.member.utils',
              'cogs.system.error_handler',
              'cogs.system.logger',
              'cogs.admin',
              'cogs.owner']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'[{time.ctime()}] Не удалось загрузить модуль {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print(f'[{time.ctime()}] Подключение успешно осуществлено!\nВ сети: {bot.user}')

    await start_session()

    async def presence():
        sleeping = 12
        while not bot.is_closed():
            await bot.change_presence(activity=discord.Streaming(name=f'{len(bot.guilds)} серверов!', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(sleeping)
            await bot.change_presence(activity=discord.Streaming(name=f'{len(bot.users)} участников!', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(sleeping)
            await bot.change_presence(activity=discord.Streaming(name=f'{len(bot.emojis)} эмодзи!', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(sleeping)
            await bot.change_presence(activity=discord.Streaming(name=f'{len([x.name for x in bot.commands if not x.hidden])} команд!', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(sleeping)
            await bot.change_presence(activity=discord.Streaming(name=f'{prefix}help', url='https://www.twitch.tv/%none%'))
            await asyncio.sleep(sleeping)
    bot.loop.create_task(presence())

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)
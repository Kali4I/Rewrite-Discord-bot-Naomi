# python3.6
# coding: utf-8

import os
import sys
import time
import asyncio
import aiohttp
import traceback
import aiohttp

import discord
from discord.ext import commands

prefix = os.getenv('PREFIX')
game_activity = os.getenv('ACTIVITY')

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')
async def start_session():
    bot.session = aiohttp.ClientSession(loop=bot.loop)

extensions = ['cogs.member.fun',
              'cogs.member.info',
              'cogs.member.music',
              'cogs.member.utils',
              'cogs.member.owo',
              'cogs.system.error_handler',
              'cogs.system.logger',
              'cogs.admin.management',
              'cogs.owner']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'[!] Не удалось загрузить модуль {extension}.', file=sys.stderr)
            print('------------------------')
            traceback.print_exc()
            print('------------------------')
        else:
            print(f'[!] Модуль {extension} успешно загружен.')

@bot.event
async def on_connect():
    await bot.change_presence(activity=discord.Game(name='загружаюсь :з'), status=discord.Status.idle)

@bot.event
async def on_ready():
    print(f'[#] Подключение успешно осуществлено!\n[#] В сети: {bot.user}')

    async def presence():
        await start_session()
        while not bot.is_closed():
            awaiting = 10

            messages = [f'{len(bot.guilds)} серверов!',
                        f'{len(bot.users)} участников!',
                        f'{len(bot.emojis)} эмодзи!',
                        f'{len([x.name for x in bot.commands if not x.hidden])} команд!',
                        f'{prefix}help',
                         'https://discord.io/naomi']
            for msg in messages:
                if game_activity == 'streaming':
                    await bot.change_presence(activity=discord.Streaming(name=msg, url='https://www.twitch.tv/%none%'))
                    await asyncio.sleep(awaiting)
                if game_activity == 'playing':
                    await bot.change_presence(activity=discord.Game(name=msg))
                    await asyncio.sleep(awaiting)
    await bot.loop.create_task(presence())

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)

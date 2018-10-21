# python3.6
# coding: utf-8

import os
import sys
import time
import asyncio
import traceback
import aiohttp

import discord
from discord.ext import commands

prefix = os.getenv('PREFIX')
game_activity = os.getenv('ACTIVITY')

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

extensions = ['cogs.member.fun',
              'cogs.member.info',
              'cogs.member.music',
              'cogs.member.utils',
              'cogs.system.error_handler',
              'cogs.system.logger',
              'cogs.admin.management',
              'cogs.owner']

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Не удалось загрузить модуль {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print(f'[{time.ctime()}] Подключение успешно осуществлено!\nВ сети: {bot.user}')
    
    async def presence():
        while not bot.is_closed():
            awaiting = 10
            messages = [f'{len(bot.guilds)} серверов!',
                        f'{len(bot.users)} участников!',
                        f'{len(bot.emojis)} эмодзи!',
                        f'{len([x.name for x in bot.commands if not x.hidden])} команд!',
                        f'{prefix}help']
            for msg in messages:
                if game_activity == 'streaming':
                    await bot.change_presence(activity=discord.Streaming(name=msg, url='https://www.twitch.tv/%none%'))
                    await asyncio.sleep(awaiting)
                if game_activity == 'playing':
                    await bot.change_presence(activity=discord.Game(name=msg))
                    await asyncio.sleep(awaiting)

    await bot.loop.create_task(presence())

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)

# python3.6
# -*- coding: utf-8 -*-

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

game_activity = os.getenv("ACTIVITY")

async def start_session():
    bot.session = aiohttp.ClientSession()

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
            print(f'[{time.ctime()}] Не удалось загрузить модуль {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    print(f'[{time.ctime()}] Подключение успешно осуществлено!\nВ сети: {bot.user}')

    await start_session()

    async def presence():
        sleeping = 10
        messages = [f'{len(bot.guilds)} серверов!',
                    f'{len(bot.users)} участников!',
                    f'{len(bot.emojis)} эмодзи!',
                    f'{len([x.name for x in bot.commands if not x.hidden])} команд!',
                    f'{prefix}help']
        while not bot.is_closed():
            for msg in messages:
                if self.game_activity == 'streaming':
                    await self.change_presence(activity=discord.Streaming(name=msg, url='https://www.twitch.tv/%none%'))
                    await asyncio.sleep(10)
                if self.game_activity == 'playing':
                    await self.change_presence(activity=discord.Game(name=msg))
                    await asyncio.sleep(10)
    
    def run(self):
        self.remove_command('help')
        for extension in self.extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'[{time.ctime()}] Не удалось загрузить модуль {extension}.', file=sys.stderr)
                traceback.print_exc()
        super().run(os.getenv('TOKEN'), reconnect=True)
        
    async def on_ready(self):
        print(f'[{time.ctime()}] Подключение успешно осуществлено!\nВ сети: {self.user}')
        self.loop.create_task(presence())

if __name__ == '__main__':
    Naomi(**{"BOTPREFIX": os.getenv('PREFIX'), "CINS": True, "FOM": False}).run()

import os
import sys
import time
import asyncio
import traceback
import aiohttp

import discord
from discord.ext import commands

class Naomi(commands.AutoShardedBot):
    def __init__(self):
        
        super().__init__(command_prefix=commands.when_mentioned_or(os.getenv("PREFIX")), case_insensitive=True, fetch_offline_members=False)
        
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.game_activity = 'playing'
        self.extensions = ['cogs.member.fun',
                           'cogs.member.info',
                           'cogs.member.music',
                           'cogs.member.utils',
                           'cogs.system.error_handler',
                           'cogs.system.logger',
                           'cogs.admin',
                           'cogs.owner']

        self.messages = [f'{len(self.guilds)} серверов!',
                         f'{len(self.users)} участников!',
                         f'{len(self.emojis)} эмодзи!',
                         f'{len([x.name for x in self.commands if not x.hidden])} команд!',
                         f'{self.prefix}help']
                         
    def __repr__(self):
        return "Я - Бот Наоми :)"

    async def presence(self):
        while not self.is_closed():
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
    Naomi().run()

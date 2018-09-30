import discord
from discord.ext import commands
import time

class Logger(object):
    """Набор эвентов для логирования событий."""

    def __init__(self, bot):
        self.bot = bot

    async def on_member_ban(self, g, u):
        print(f'[{time.ctime()}] {u.name} ({u.id}) забанен на {g.name} ({g.id})')

    async def on_member_unban(self, g, u):
        print(f'[{time.ctime()}] {u.name} ({u.id}) разбанен на {g.name} ({g.id})')

    async def on_member_join(self, m):
        print(f'[{time.ctime()}] {m} присоединился к гильдии {m.guild.name}')

    async def on_member_remove(self, m):
        print(f'[{time.ctime()}] {m} вышел с гильдии {m.guild.name}')

    async def on_guild_join(self, g):
        print(f'[{time.ctime()}] Меня пригласили на {g.name}, еее!')

    async def on_guild_remove(self, g):
        print(f'[{time.ctime()}] Меня отключили от {g.name}, обидка :с')


def setup(bot):
    bot.add_cog(Logger(bot))
    print('[logger.py] Логгер загружен.')
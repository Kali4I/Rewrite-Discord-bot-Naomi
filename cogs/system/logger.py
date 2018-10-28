import discord
from discord.ext import commands
import time


class Logger(object):
    """Набор эвентов для логирования событий."""

    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, g):
        print(f'[?] Меня пригласили на {g.name}, еее! :з')

    async def on_guild_remove(self, g):
        print(f'[?] Меня отключили от {g.name}, обидка :с')

    # Да, здесь ОЧЕНЬ много эвентов xD

def setup(bot):
    bot.add_cog(Logger(bot))

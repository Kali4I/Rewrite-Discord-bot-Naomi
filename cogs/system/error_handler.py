import discord
from discord.ext import commands
import sys
import time
import traceback

"""
Error handler by EvieePy
    (https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612)

Edited by AkiraSumato-01 for Rewrite-Discord-Bot-Naomi
    (https://github.com/AkiraSumato-01/Rewrite-Discord-Bot-Naomi)
"""


class ErrorHandler:
    """Модуль обработки и оповещения об исключениях."""

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.NotOwner, discord.NotFound)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return
        
        # Нет прав
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(color=0xFF0000).set_author(
                    name='У вас нет прав.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)

        # Не указаны ключевые аргументы
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Указаны не все ключевые аргументы для {ctx.prefix}{ctx.command}.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)

        # Команда отключена
        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Команда {ctx.prefix}{ctx.command} отключена.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)

        # Ошибка прав со стороны бота
        elif isinstance(error, discord.errors.Forbidden):
            embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'У меня недостаточно прав.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)

        # Ошибка проверки (прав / NSFW-канала)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Эту команду нельзя выполнить здесь. (Может быть, попробуете в NSFW канале?)',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)

        # Серверная команда использована в ЛС
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Команда {ctx.prefix}{ctx.command} не может быть выполнена в ЛС.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
                return await ctx.send(embed=embed)
            except:
                pass

        # Неверный аргумент
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Получен неверный аргумент для {ctx.prefix}{ctx.command}.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)


        # Если ничего не подходит
        rep_guild = discord.utils.get(self.bot.guilds, id=457092470472179712)
        rep_channel = discord.utils.get(rep_guild.channels, id=503340681058713621)
        
        embed = discord.Embed(
                    color=0xF56415,
                    timestamp=ctx.message.created_at,
                    title='ErrorHandler обнаружил ошибку!',
                    description=f'Вызвано участником: {ctx.author}\nКоманда: {ctx.prefix}{ctx.command}\nПодробности ошибки: ```python\n{type(error).__name__}: {error}```\n```python\n{type(error).__name__}:\n{type(error).__doc__}```'
                    )
        embed.set_author(
                    name='Обработка исключения.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
        await rep_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    print('[error_handler.py] ErrorHandler загружен.')

import discord
import io
import os
import sys
import traceback
import textwrap
import platform
import psutil

from discord.ext import commands
from contextlib import redirect_stdout

class Owner(object):
    """Набор команд для отладки и тестирования."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='sysinfo', pass_context=True)
    @commands.is_owner()
    async def sysinfo(self, ctx):
        """Системная информация.
        """

        pid = os.getpid()
        py = psutil.Process(pid)

        mem_percent_usage = py.memory_percent()
        cpu_percent_usage = py.cpu_percent()
        process_sys_name = py.name()
        process_sys_username = py.username()

        ram_load = psutil.virtual_memory().percent
        cpu_load = ', '.join([f'{x}%' for x in psutil.cpu_percent(interval=None, percpu=True)])

        main = f"""
Загрузка ЦПУ (всего):
- `{''.join(cpu_load)}`
Загрузка ОЗУ (всего): `{ram_load}`
Имя процесса: `{process_sys_name}`
Имя пользователя: `{process_sys_username}`

Потребление ОЗУ: `{round(mem_percent_usage)}%`
Потребление ресурсов ЦПУ: `{round(cpu_percent_usage)}%`
"""

        await ctx.send(embed=discord.Embed(
            title=f'Системная информация | {ctx.prefix}{ctx.command}',
            description=main))

    @commands.command(name='quit', aliases=['quitserver'], hidden=True)
    @commands.is_owner()
    async def quit_guild(self, ctx, guild: discord.Guild):
        """Отключить меня от сервера.

        Аргументы:
        `:guild` - имя сервера
        __                                            __
        Например:
        ```
        n!quit MyLittleGroup
        ```
        """
        try:
            await guild.leave()

        except:
            ctx.send(f'Возникла ошибка:\n{traceback.format_exc()}')

    @commands.command(name='ping', hidden=True)
    @commands.is_owner()
    async def ping(self, ctx):
        """Измерение задержки API, клиента.
        """

        resp = await ctx.send('Тестируем...')
        diff = resp.created_at - ctx.message.created_at
        await resp.edit(content=f':ping_pong: Pong!\nЗадержка API: {1000 * diff.total_seconds():.1f}мс.\nЗадержка {self.bot.user.name}: {round(self.bot.latency * 1000)}мс')

    @commands.command(hidden=True, aliases=['r'])
    @commands.is_owner()
    async def restart(self, ctx):
        """Перезагрузка.
        """

        await ctx.send(embed=discord.Embed(color=0x13CFEB).set_footer(text="Перезагружаемся..."))
        os.execl(sys.executable, sys.executable, * sys.argv)

    @commands.command(name='#exception', hidden=True)
    @commands.is_owner()
    async def exception(self, ctx):
        """Выдать исключение.
        """

        raise RuntimeError('Вызвано разработчиком.')

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Загрузить модуль.

        Аргументы:
        `:cog` - имя модуля (включая директорию)
        __                                            __
        Например:
        ```
        n!load cogs.member.utils
        ```
        """

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при загрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно загружен`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Выгрузить модуль.

        Аргументы:
        `:cog` - имя модуля (включая директорию)
        __                                            __
        Например:
        ```
        n!unload cogs.admin
        ```
        """

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при выгрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно выгружен`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Перезагрузка модуля.

        Аргументы:
        `:cogs` - имя модуля (включая директорию)
        __                                            __
        Например:
        ```
        n!reload cogs.member.fun
        ```
        """

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при перезагрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно перезагружен`**')

    @commands.command(name='execute', aliases=['exec', 'eval'], hidden=True)
    @commands.is_owner()
    async def execute(self, ctx, *, code: str):
        """Интерпретатор Python кода.

        Аргументы:
        `:code` - код (Python 3)
        __                                            __
        Например:
        ```
        n!exec print('Hello World')
        ```
        """

        async def v_execution():
            async with ctx.channel.typing():
                owner = (await self.bot.application_info()).owner

                env = {
                    'channel': ctx.channel,
                    'author': ctx.author,
                    'guild': ctx.guild,
                    'message': ctx.message,
                    'client': self.bot,
                    'bot': self.bot,
                    'discord': discord,
                    'ctx': ctx,
                    'owner': owner
                }

                env.update(globals())
                _code = ''.join(code).replace('```python', '').replace('```', '')
                try:
                    stdout = io.StringIO()
                    interpretate = f'async def virtexec():\n{textwrap.indent(_code, "  ")}'
                    exec(interpretate, env)
                    virtexec = env['virtexec']
                    with redirect_stdout(stdout):
                        function = await virtexec()

                except:
                    stdout = io.StringIO()
                    value = stdout.getvalue()

                    msg = discord.Embed(color=0xff0000, description=f"\n:inbox_tray: Входные данные:\n```python\n{''.join(code).replace('```python', '').replace('```', '')}\n```\n:outbox_tray: Выходные данные:\n```python\n{value}{traceback.format_exc()}```".replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                    msg.set_author(name='Интерпретатор Python кода.')
                    msg.set_footer(text=f'Интерпретация не удалась - Python {platform.python_version()} | {platform.system()}')
                    return await ctx.send(f'{owner.mention}, смотри сюда!', embed=msg)
                else:
                    value = stdout.getvalue()
                    if function is None:
                        if not value:
                            value = 'None'
                        success_msg = discord.Embed(color=0x00ff00, description=f":inbox_tray: Входные данные:\n```python\n{''.join(code).replace('```python', '').replace('```', '')}```\n\n:outbox_tray: Выходные данные:\n```python\n{value}```".replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                        success_msg.set_author(name='Интерпретатор Python кода.')
                        success_msg.set_footer(text=f'Интерпретация успешно завершена - Python {platform.python_version()} | {platform.system()}')
                        return await ctx.send(f'{owner.mention}, смотри сюда!', embed=success_msg)
                    else:
                        success_msg = discord.Embed(color=0x00ff00, description=f":inbox_tray: Входные данные:\n```python\n{''.join(code).replace('```python', '').replace('```', '')}```\n\n:outbox_tray: Выходные данные:\n```python\n{value}{function}```".replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                        success_msg.set_author(name='Интерпретатор Python кода.')
                        success_msg.set_footer(text=f'Интерпретация успешно завершена - Python {platform.python_version()} | {platform.system()}')
                        return await ctx.send(f'{owner.mention}, смотри сюда!', embed=success_msg)

        self.bot.loop.create_task(v_execution())

        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass

def setup(bot):
    bot.add_cog(Owner(bot))
    print('[owner.py] Модуль всея владельца загружен.')

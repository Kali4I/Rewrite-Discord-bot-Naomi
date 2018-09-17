import discord
import io
import os
import sys
import traceback
import textwrap
import platform

from utils.HelpPaginator import HelpPaginator, CannotPaginate

from discord.ext import commands
from contextlib import redirect_stdout

class Owner(object):

    def __init__(self, bot):
        self.bot = bot






    @commands.command(name='thelp', description='Тестовое меню справки.')
    @commands.is_owner()
    async def thelp(self, ctx, *, command:str=None):
        try:
            if command is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = self.bot.get_cog(command) or self.bot.get_command(command)

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Команда или категория "{clean}" не найдена.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
            await ctx.send(e)

    """
    async def thelp(self, ctx, command:str=None):
        if command:
            return await ctx.send('Справка по конкретным командам не готова.')

        temp = []
        cmd_list = []
        command_pages = {}
        for cmd in [x for x in self.bot.commands if not x.hidden]:
            if len(temp) != 10:
                temp.append(cmd)
            else:
                cmd_list.append(temp)
                temp = []
        for row in cmd_list:
            for i in range(len(cmd_list)):
                command_pages[i] = [f'{x.name} | {x.description}' for x in row if not x.hidden]

        current = await ctx.send('Кликните реакцию.')

        async def react_control():
            reactions = {'⬅':'<', '➡':'>'}
            for react in reactions:
                await current.add_reaction(react)

            def check(r, u):
                if not current:
                    return False
                elif str(r) not in reactions.keys():
                    return False
                elif u.id != ctx.author.id or r.message.id != current.id:
                    return False
                return True

            while current:
                react, user = await self.bot.wait_for('reaction_add', check=check)
                try:
                    control = reactions.get(str(react))
                except:
                    control = None

                curpage = 0

                if control == '<':
                    try:
                        await current.edit(embed=command_pages[curpage - 1])
                    except KeyError as e:
                        print(e)

                if control == '>':
                    try:
                        await current.edit(embed=command_pages[curpage + 1])
                    except KeyError as e:
                        print(e)

                try:
                    await current.remove_reaction(react, user)
                except discord.HTTPException:
                    pass
                    
        self.bot.loop.create_task(react_control())


"""



    @commands.command(name='ping', description='Проверка скорости ответа.')
    @commands.is_owner()
    async def ping(self, ctx):
        resp = await ctx.send('Тестируем...')
        diff = resp.created_at - ctx.message.created_at
        await resp.edit(content=f'Задержка API: {1000*diff.total_seconds():.1f}ms.\nЗадержка {self.bot.user.name}: {round(self.bot.latency * 1000)}ms')






    @commands.command(hidden=True, description='Перезагрузка.', aliases=['r'])
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.send(embed=discord.Embed(color=0x13CFEB).set_footer(text="Перезагружаемся..."))
        os.execl(sys.executable, sys.executable, * sys.argv)






    @commands.command(name='load', description='Загрузка модуля.', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при загрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно загружен`**')






    @commands.command(name='unload', description='Выгрузка модуля.', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при выгрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно выгружен`**')


    @commands.command(name='reload', description='Перезагрузка модуля.', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`Ошибка при перезагрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно перезагружен`**')


    @commands.command(name='execute', description=f'Интерпретатор Python {platform.python_version()}.', aliases=['exec', 'eval'], hidden=True)
    @commands.is_owner()
    async def execute(self, ctx, *, code: str):

        async def _execution():
            async with ctx.channel.typing():
                env = {
                    'channel': ctx.channel,
                    'author': ctx.author,
                    'guild': ctx.guild,
                    'message': ctx.message,
                    'client': self.bot,
                    'discord': discord
                }

                owner = (await self.bot.application_info()).owner

                env.update(globals())
                _code = ''.join(code).replace('```python', '').replace('```', '')
                try:
                    stdout = io.StringIO()
                    interpretate = f'async def virtexec():\n{textwrap.indent(_code, "  ")}'
                    exec(interpretate, env)
                    virtexec = env['virtexec']
                    with redirect_stdout(stdout):
                        function = await virtexec()

                except Exception as e:
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

        self.bot.loop.create_task(_execution())

        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            pass



def setup(bot):
    bot.add_cog(Owner(bot))
    print('[owner.py] Модуль всея владельца загружен.')
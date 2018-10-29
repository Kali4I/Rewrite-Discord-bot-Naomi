# python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
from random import randint
import discord
import whois
import time

from utils.HastebinPoster import post

class Utils(object):
    """Команды пользователей - Utils"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='unicodemoji', aliases=['uemoji'])
    async def uemoji(self, ctx, emoji: commands.clean_content):
        """Получить Unicode-эмодзи.

        Аргументы:
        `:emoji` - эмодзи
        __                                            __
        Например:
        ```
        n!uemoji :thinking:
        ```
        """
        await ctx.send(f'**`{emoji}`**')
    
    @commands.command(name='randint', aliases=['rval'])
    async def random_(self, ctx, from_: int = 0, to: int = 100):
        """Сгенерировать случайное число.

        Аргументы:
        `:from_` - от...
        `:to` - до...
        __                                            __
        Например:
        ```
        n!rval 5 100
        n!randint 500 2931
        ```
        """
        await ctx.send(f'Рандомное число: **`{randint(from_, to)}`**')

    @commands.command(name='hostinfo', aliases=['host', 'whois'])
    async def hostinfo(self, ctx, domain: commands.clean_content):
        """WHOIS-информация о домене.

        Аргументы:
        `:domain` - домен / ip
        __                                            __
        Например:
        ```
        n!host google.com
        ```
        """

        try:
            whois_info = whois.whois(domain)
        except whois.gaierror:
            return await ctx.send(f':x: У меня не получилось найти "{domain}"! :c')

        hostinfo = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000, title=f'WHOIS-информация для {domain}')

        crtdate = whois_info["creation_date"]
        expdate = whois_info["expiration_date"]
        domain = whois_info["domain_name"]

        if type(expdate).__name__ == 'list':
            expdate = whois_info["expiration_date"][0]
        
        if type(crtdate).__name__ == 'list':
            crtdate = whois_info["creation_date"][0]

        if type(domain).__name__ == 'list':
            domain = whois_info["domain_name"][0]

        hostinfo.add_field(name="Домен:", value=domain, inline=True)
        hostinfo.add_field(name="Регистратор:", value=whois_info["registrar"], inline=True)
        hostinfo.add_field(name="Whois-сервер:", value=whois_info["whois_server"], inline=True)
        hostinfo.add_field(name="Дата окончания:", value=expdate, inline=True)
        hostinfo.add_field(name="Дата создания:", value=crtdate, inline=True)
        hostinfo.add_field(name="Регион:", value=whois_info["country"], inline=True)
        hostinfo.set_footer(text=ctx.prefix + 'hostinfo [домен]')
        await ctx.send(embed=hostinfo)

    @commands.command(name='hastebin', pass_context=True)
    async def hastebin_post(self, ctx, *, code: str):
        """Отправка текста на Hastebin.com

        Аргументы:
        `:code` - текст
        __                                            __
        Например:
        ```
        n!hastebin print('Hello World')
        ```
        """

        link = await post(code)
        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, title='Ваш код был загружен на Hastebin:',
                                        description=f'```{link}```'))

    @commands.command(name='calc', aliases=['calculator', 'math', 'calculate'])
    async def calc(self, ctx, *, expression: str):
        """Калькулятор.

        Аргументы:
        `:expression` - математическое выражение
        __                                            __
        Например:
        ```
        n!calc 5 + 5
        n!calculate 10 ^ 2
        n!calculator (10 + 2) * 6
        ```
        """
        from math import pi
        from re import sub

        try:
            a = expression.replace(':', '/').replace('^', '**').replace(',', '.')
            b = sub('[ йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮQWERTYUIOPASDFGHJKLZXCVBNMqwertyuoasdfghjklzxcvbnm;!@#$=\'\"]', '', a)
        except:
            return False

        if len(b) >= 9 and b.count('**') == 1 or b.count('**') >= 2 and len(b) >= 6:
            return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xfA0000).set_footer(text='Недопустимо по причине снижения производительности.'))

        else:

            embed = discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302,
                                description=f'```css\n\{expression}```')
            embed.set_footer(text=f'{ctx.prefix}{ctx.command} <expression>')
            embed.set_author(name=ctx.message.author.name,
                             icon_url=ctx.message.author.avatar_url)

            try:
                eval_ = str(eval(b))

            except ZeroDivisionError:
                eval_ = '∞'

            except:
                embed.add_field(name='Выражение имеет ошибку.',
                                value='Исправьте его.')

            if len(eval_) > 12 and not eval_.isnumeric():
                embed.add_field(name='Ответ:',
                                value=f'{eval_[:12]}..')
                embed.add_field(name='Округленное значение:',
                                value=f'{round(float(eval_))}')

            elif len(eval_) > 12 and eval_.isnumeric():
                embed.add_field(name='Ответ:',
                                value=f'{eval_[:26]}..')

            else:
                embed.add_field(name='Ответ:',
                                value=f'{eval_}')
            
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utils(bot))
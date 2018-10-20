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
    
    @commands.command(name='randint', aliases=['rval'])
    async def random_(self, ctx, from_: int = None, to: int = None):
        """Сгенерировать случайное число.

        Аргументы:
        `:from_` - от...
        `:to` - до...
        \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
        Например:
        ```
        n!rval 5 100
        n!randint 500 2931
        ```
        """

        if not from_ or not from_.isnumeric():
            from_ = 0
        if not to or not to.isnumeric():
            to = 100
        
        try:
            int_ = randint(from_, to)
        except:
            int_ = randint(0, 100)

        await ctx.send(f'Рандомное число: **`{int_}`**')

    @commands.command(name='hostinfo', aliases=['host', 'whois'])
    async def hostinfo(self, ctx, domain:str):
        """WHOIS-информация о домене.

        Аргументы:
        `:domain` - домен / ip
        \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
        Например:
        ```
        n!host google.com
        ```
        """

        whois_info = whois.whois(domain)

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
    async def hastebin_post(self, ctx, *, code:str):
        """Отправка текста на Hastebin.com

        Аргументы:
        `:code` - текст
        \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
        Например:
        ```
        n!hastebin print('Hello World')
        ```
        """

        link = await post(code)
        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, title='Ваш код был загружен на Hastebin:',
                                        description=f'```{link}```'))

    @commands.command(name='calc', aliases=['calculator', 'calculate'], pass_context=True)
    async def calc(self, ctx, *, expression:str):
        """Калькулятор.

        Аргументы:
        `:expression` - математическое выражение
        \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
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
        
        if len(b) >= 16 and b.count('**') == 1 or b.count('**') >= 2 and len(b) >= 8:
            return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xfA0000).set_footer(text=ctx.prefix + 'Недопустимо по причине снижения производительности.'))

        else:
            try:
                eval_ = str(eval(b))

            except ZeroDivisionError:
                eval_ = '∞'

            except:
                return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302).set_footer(text=ctx.prefix + 'Выражение имеет ошибку.\nИсправьте его.'))

            if len(eval_) > 12 and not eval_.isnumeric():
                await ctx.send(embed=discord.Embed(
                    timestamp=ctx.message.created_at,
                    color=0xf0a302,
                    description=f'```css\n{expression}\n({b})\
                    \n```(Указаны первые 12 цифр)\
                    \n{eval_[:12]}\
                    \n\nОкругленный:\
                    \n{round(float(eval_))}').set_footer(text=ctx.prefix + ctx.command + ' [матем.выражение]'))

            elif len(eval_) > 12 and eval_.isnumeric():
                await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,
                    color=0xf0a302,
                    description=f'```css\n\{expression}\n({b})\
                    \n```(Указаны первые 12 цифр)\
                    \n{eval_[:12]}').set_footer(text=ctx.prefix + ctx.command + ' [матем.выражение]'))

            else:
                await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,
                    color=0xf0a302,
                    description=f'```css\n{expression}\n({b})\
                    \n```{eval_}').set_footer(text=ctx.prefix + ctx.command + ' [матем.выражение]'))

def setup(bot):
    bot.add_cog(Utils(bot))
    print('[utils.py] Модуль "Member/Utils" загружен.')

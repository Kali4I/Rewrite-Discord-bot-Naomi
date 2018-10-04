from discord.ext import commands
from random import randint
import discord
import whois
import time

from utils.HastebinPoster import post

class Utils(object):
    """Команды пользователей // Utils"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='randint', aliases=['rval', 'rvalue'])
    async def random_(self, ctx, from_: int = None, to: int = None):
        """Сгенерировать случайное число.

        Подробности:
        --------------
        <from_> - от...
        <to> - до...
        """

        if not from_:
            from_ = 0
        if not to:
            to = 100
        
        await ctx.send(f'Рандомное число: **`{randint(from_, to)}`**')

    @commands.command(name='hostinfo', aliases=['host', 'whois'])
    async def hostinfo(self, ctx, domain:str):
        """WHOIS-информация о домене.

        Подробности:
        --------------
        <domain> - домен (например google.com).
        """

        whois_info = whois.whois(domain)

        hostinfo = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000, title=f'WHOIS-информация для {domain}')

        crtdate = whois_info["creation_date"]
        expdate = whois_info["expiration_date"]
        domain = whois_info["domain_name"]

        if type(expdate).__name__ == 'list':
             expdata = whois_info["expiration_date"][0]
        
        if type(crtdate).__name__ == 'list':
            whois_info["creation_date"][0]

        if type(domain).__name__ == 'list':
            domain = whois_info["domain_name"][0]

        hostinfo.add_field(name="Домен:", value=domain, inline=True)
        hostinfo.add_field(name="Регистратор:", value=whois_info["registrar"], inline=True)
        hostinfo.add_field(name="Whois-сервер:", value=whois_info["whois_server"], inline=True)
        hostinfo.add_field(name="Дата окончания:", value=expdata, inline=True)
        hostinfo.add_field(name="Дата создания:", value=crtdata, inline=True)
        hostinfo.add_field(name="Регион:", value=whois_info["country"], inline=True)
        hostinfo.set_footer(text='hostinfo [домен]')
        await ctx.send(embed=hostinfo)

    @commands.command(name='hastebin')
    async def hastebin_post(self, ctx, *, code:str):
        """Отправить код на Hastebin.com.

        Подробности:
        --------------
        <code> - код для отправки на hastebin.com (без ```)
        """

        link = await post(code)
        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, title='Ваш код был загружен на Hastebin:',
                                        description=f'```{link}```'))

    @commands.command(name='calc', aliases=['calculator', 'calculate'])
    async def calc(self, ctx, *, numbers:str):
        """Калькулятор.

        Подробности:
        --------------
        <numbers> - математическое выражение.
        """
        from math import pi
        from re import sub

        try:
            a = numbers.replace(':', '/').replace('^', '**').replace(',', '.')
            b = sub('[ йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮQWERTYUIOPASDFGHJKLZXCVBNMqwertyuoasdfghjklzxcvbnm;!@#$=\'\"]', '', a)
        except:
            return False
        
        if len(b) >= 8 and b.count('**') != 0:
            return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xfA0000).set_footer(text='Недопустимо по причине снижения производительности.'))

        else:
            try:
                __eval = str(eval(b))

            except ZeroDivisionError:
                __eval = '∞'

            except:
                return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302).set_footer(text='Выражение имеет ошибку.\nИсправьте его.'))

            if len(__eval) > 12 and not __eval.isnumeric():
                await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302, description=f'```css\n{numbers}\n({b})\n```(Указаны первые 12 цифр)\n{__eval[:12]}\n\nОкругленный:\n{round(float(__eval))}').set_footer(text='calc [матем.выражение]'))

            elif len(__eval) > 12 and __eval.isnumeric():
                await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302, description=f'```css\n{numbers}\n({b})\n```(Указаны первые 12 цифр)\n{__eval[:12]}').set_footer(text='calc [матем.выражение]'))

            else:
                await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302, description=f'```css\n{numbers}\n({b})\n```{__eval}').set_footer(text='calc [матем.выражение]'))

def setup(bot):
    bot.add_cog(Utils(bot))
    print('[utils.py] Модуль "Member/Utils" загружен.')

from discord.ext import commands
import discord
import whois
import time

from utils.HastebinPoster import post

blocked = [437883431897268224]

class Utils(object):
    """Команды пользователей // Utils"""
    def __init__(self, bot):
        self.bot = bot







    @commands.command(name='hostinfo', aliases=['host', 'whois'])
    async def hostinfo(self, ctx, domain:str):
        """WHOIS-информация о домене.

        Подробности:
        --------------
        <domain> - домен (например google.com).
        """

        whois_info = whois.whois(domain)

        hostinfo = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000, title=f'WHOIS-информация для {domain}')

        try:
            expdata = str(whois_info["expiration_date"][0])
        except:
            expdata = str(whois_info["expiration_date"])

        try:
            crtdata = str(whois_info["creation_date"][0])
        except:
            crtdata = str(whois_info["creation_date"])

        try:
            domain = whois_info["domain_name"][0]
        except:
            domain = whois_info["domain_name"]

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







    @commands.command(name='idea', aliases=['myidea', 'my-idea'])
    async def idea(self, ctx, *, message:str):
        """Поделиться Вашей идеей для меня.

        Подробности:
        --------------
        <message> - описание вашей идеи.
        """

        if ctx.author.id in blocked:
            return await ctx.send('Нельзя.')

        try:
            ideas_guild = discord.utils.get(self.bot.guilds, id=457092470472179712)
            ideas_channel = discord.utils.get(ideas_guild.channels, id=483662616921767956)

            await ctx.send('Ваша идея отправлена на наш Discord-сервер;\n Спасибо за помощь.')
            await ideas_channel.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xF56415, 
                                title='Идея от пользователя.',
                                description='Отправил: %s\nОписание:```markup\n%s```\n\n%s' % (ctx.author, message, time.ctime())))
        except Exception as e:
            await ctx.send('Не удалось отправить.\n%s' % e)






    @commands.command(name='bug', aliases=['bugreport', 'bug-report', 'report-bug'])
    async def bugreport(self, ctx, *, message:str):
        """Сообщить о проблеме / баге.

        Подробности:
        --------------
        <message> - подробное описание проблемы.
        """

        if ctx.author.id in blocked:
            return await ctx.send('Нельзя.')

        try:
            rep_guild = discord.utils.get(self.bot.guilds, id=457092470472179712)
            rep_channel = discord.utils.get(rep_guild.channels, id=483662931377127424)

            await ctx.send('Ваш баг-репорт отправлен на наш Discord-сервер;\n Спасибо за помощь.')
            await rep_channel.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xF56415, 
                                title='Новый баг-репорт!',
                                description='Отправил: %s\nОписание:```markup\n%s```\n\n%s' % (ctx.author, message, time.ctime())))
        except Exception as e:
            await ctx.send('Не удалось отправить репорт.\n%s' % e)






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
            try: __eval = str(eval(b))
            except ZeroDivisionError: __eval = '∞'
            except Exception as e:
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
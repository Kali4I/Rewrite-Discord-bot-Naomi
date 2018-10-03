from discord.ext import commands
from random import randint, choice
import discord
import apiai
import nekos
import json
import os

from utils.NekosWrapper import (get_neko, 
                                NekoNotInTags,
                                tags)

class Fun(object):
    """Команды пользователей // Fun"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='random', aliases=['randuser', 'randomuser', 'rand-user'])
    async def randomuser(self, ctx, *, message:str):
        """Выбрать рандомного участника сервера.

        Подробности:
        --------------
        <message> - Ваше сообщение.
        """
        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=randint(0x000000, 0xFFFFFF),
            description=f'{choice([x.mention for x in ctx.guild.members])} {message}'))

    @commands.command(name='myname', aliases=['my-name'])
    @commands.guild_only()
    async def myname(self, ctx, *, nickname:str=None):
        """Сменить Ваш никнейм.

        Подробности:
        --------------
        [nickname] - новый никнейм (ничего для сброса).
        """

        try:
            await ctx.author.edit(nick=nickname, reason='Запрошено пользователем.')
        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'))

    @commands.command(name='talk', aliases=['t'])
    async def talk(self, ctx, *, message:str):
        """Общение с ботом.

        Подробности:
        --------------
        <message> - ваше сообщение боту.
        """
        
        ai = apiai.ApiAI(os.getenv('TALK_SERVICE_TOKEN'))

        request = ai.text_request()
        request.lang = 'ru'
        request.session_id = os.getenv('TALK_SERVICE_SESSION_ID')
        request.query = message
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']

        if response:
            await ctx.send(response)

        else:
            no_answer = choice(['Не знаю, как ответить...',
                                'Полагаю, у меня нет ответа.',
                                '~~Как же ответить, как же ответить...~~',
                                'Извиняюсь, но я не знаю, как ответить...'])
            await ctx.send(no_answer)

    @commands.command(name='helloworld', aliases=['hw'])
    async def helloworld(self, ctx):
        await ctx.send('Hello, %s' % ctx.author.mention)

    @commands.command(name='say', aliases=['repeat', 'msg'])
    async def say(self, ctx, *, msg:str):
        """Повторить сообщение пользователя.

        Подробности:
        --------------
        <msg> - ваше сообщение.
        """
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(msg)

    @commands.command(name='neko', aliases=['catgirl', 'nekogirl'])
    async def catgirl(self, ctx, tag:str=None):
        """Отправляет аниме изображение [Только в NSFW-каналах]

        Подробности:
        --------------
        [tag] - тег (если не указан, выбирается рандомно).

        Список тегов:
            feet, yuri, trap, futanari, hololewd, lewdkemo, solog,
            feetg, cum, erokemo, les, lewdk, ngif, tickle, lewd,
            feed, eroyuri, eron, cum_jpg, bj, nsfw_neko_gif, solo,
            kemonomimi, nsfw_avatar, poke, anal, slap, hentai, avatar,
            erofeet, holo, keta, blowjob, pussy, tits, holoero,
            pussy_jpg, pwankg, classic, kuni, pat, kiss, femdom, neko,
            cuddle, erok, fox_girl, boobs, smallboobs, hug, ero, wallpaper
        """

        try:
            if not ctx.channel.is_nsfw():
                return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='Вы не в NSFW канале!'))
        except:
            pass

        nekoframe = discord.Embed(timestamp=ctx.message.created_at, color=0xF13875)

        if tag not in tags:
            nekoframe.add_field(name='Доступные теги:', value=', '.join(tags))

        else:
            nekoframe.set_image(url=get_neko(tag))

        await ctx.send(embed=nekoframe)

    @commands.command(name='avatar', aliases=['useravatar'])
    async def avatar(self, ctx, member:discord.Member=None):
        """Выдает аватарку пользователя.

        Подробности:
        --------------
        [member] - участник.
            (если не указан, выдается аватарка автора команды)
        """

        if not member:
            member = ctx.author

        if member.avatar_url is None:
            a = discord.Embed(timestamp=ctx.message.created_at, color=0xfA0000, title=f'Аватарка {member}')
            a.set_image(url=member.default_avatar_url)
            a.set_footer(text='avatar [@пользователь]')
            await ctx.send(embed=a)

        else:
            a = discord.Embed(timestamp=ctx.message.created_at, color=0xfA0000, title=f'Аватарка {member}')
            a.set_image(url=member.avatar_url_as(static_format='png', size=1024))
            a.set_footer(text='avatar [@пользователь]')
            await ctx.send(embed=a)

def setup(bot):
    bot.add_cog(Fun(bot))
    print('[fun.py] Модуль "Member/Fun" загружен.')

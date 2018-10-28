# python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
from random import randint, choice
import requests
import discord
import apiai
import nekos
import json
import os

import pokebase as pb
import asyncio

from utils.NekosWrapper import (get_neko, 
                                NekoNotInTags,
                                nekos_tags)

class Fun(object):
    """Команды пользователей - Fun"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='voteyn')
    async def voteyn(self, ctx, msg: commands.clean_content):

        reactions = ['👍', '👎']

        embed = discord.Embed(title='Голосование',
                              description=msg)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        m = await ctx.send('Голосуем!', embed=embed)

        self.voted_down = 0
        self.voted_up = 0
        self.checked = []

        async def checking():
            for x in reactions:
                await m.add_reaction(x)

            def check(r, u):
                if not m \
                    or r.message.id != m.id \
                    or u.id in self.checked \
                    or u.bot:
                    return False
                return True

            while True:
                r, u = await self.bot.wait_for('reaction_add', check=check)
                if str(r) == '👍':
                    self.voted_up += 1
                if str(r) == '👎':
                    self.voted_down += 1

                self.checked.append(u.id)
        checkloop = self.bot.loop.create_task(checking())
        await asyncio.sleep(8)
        checkloop.cancel()

        embed = discord.Embed(title='Голосование окончено!',
                              description=f'```{msg}```\n\nРезультаты:\n👍: {self.voted_up}\n👎: {self.voted_down}')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='pokemon')
    async def pokemon_game(self, ctx):
        """Игра “Угадай покемона„.

        Суть игры проста - нужно написать в чат имя покемона,
            изображенного в сообщении.
        """

        def message_check(m):
            return m.author.id == ctx.author.id
        
        resp = requests.get('https://pokeapi.co/api/v2/pokemon/')
        pokemons = [x['name'] for x in resp.json()['results']]

        pokemon_name = choice(pokemons)
        pokemon = pb.pokemon(pokemon_name)

        embed = discord.Embed(color=0x42f453, title='Игра “Угадай покемона„',
                    description='У вас есть 30 секунд, чтобы отгадать этого покемона.\nПишите имя латиницей.')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.set_image(url=f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon.id}.png')
        await ctx.send(embed=embed)

        msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        
        if msg.content.lower() == pokemon_name:
            await ctx.send('Вы ответили верно! :cake:')
        else:
            await ctx.send('Ответ неверный. Ничего, повезет в следующий раз!')

    @commands.command(name='prediction', aliases=['predict'])
    async def prediction(self, ctx, *, message: str):
        """Могущественное предсказание.

        Аргументы:
        `:message` - ваш вопрос
        __                                            __
        Например:
        ```
        n!predict Я выиграю миллион?
        ```
        """
        possible = [
            'Вероятно, нет.', 'Вряд ли...', 'Очень сомневаюсь.', 'Может быть.',
            'Невозможно!', 'Мой ответ: Нет.', 'Вообще понятия не имею.',
            'Возможно, но шансы очень малы.', 'Думаю, это возможно.', 'Не отрицаю :thinking:',
            'Мой ответ: Да.', 'Полагаю, это так.', 'Несомненно.', 'Разумеется, да.']

        if len(message) <= 1:
            i_choice_it = randint(0, 5)
            return await ctx.send('{0}, {1}'.format(ctx.author.mention, possible[i_choice_it]))

        if len(message) >= 15:
            i_choice_it = randint(0, 8)
            return await ctx.send('{0}, {1}'.format(ctx.author.mention, possible[i_choice_it]))

        if len(message) >= 2 and len(message) <= 14:
            i_choice_it = randint(0, 13)
            return await ctx.send('{0}, {1}'.format(ctx.author.mention, possible[i_choice_it]))

    @commands.command(name='random', aliases=['randuser', 'randomuser', 'rand-user'])
    async def randomuser(self, ctx, *, message: str):
        """Выбрать рандомного участника сервера.

        Аргументы:
        `:message` - сообщение.
        __                                            __
        Например:
        ```
        n!randuser проиграл 5к рублей!
        n!random не покушал кашу
        ```
        """
        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at,
            color=randint(0x000000, 0xFFFFFF),
            description=f'{choice([x.mention for x in ctx.guild.members])} {message}'))

    @commands.command(name='myname', aliases=['my-name'])
    @commands.guild_only()
    async def myname(self, ctx, *, nickname: str = None):
        """Сменить ваш никнейм

        Аргументы:
        `:nickname` - новый никнейм (оставьте пустым для сброса)
        __                                            __
        Например:
        ```
        n!myname Рамочка
        n!myname
        ```
        """

        await ctx.author.edit(nick=nickname, reason='Запрошено пользователем.')

    @commands.command(name='talk', aliases=['t'])
    async def talk(self, ctx, *, message: commands.clean_content):
        """Общение с ботом (используя Google DialogFlow).

        Аргументы:
        `:message` - ваше сообщение
        __                                            __
        Например:
        ```
        n!talk Привет, что делаешь?
        ```
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
    async def say(self, ctx, *, message: commands.clean_content):
        """Повторить ваше сообщение.

        Аргументы:
        `:message` - сообщение.
        __                                            __
        Например:
        ```
        n!say Я - могущественный бот, мне нет равных. Но это не точно.
        ```
        """
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(message)

    @commands.command(name='neko', aliases=['catgirl', 'nekogirl'])
    @commands.is_nsfw()
    async def catgirl(self, ctx, tag: str = None):
        """Отправка аниме изображений.

        Аргументы:
        `:tag` - тег (или "help" для списка тегов)
        __                                            __
        Например:
        ```
        n!neko help
        n!neko avatar
        ```
        """
        nekoframe = discord.Embed(timestamp=ctx.message.created_at, color=0xF13875)

        if tag not in nekos_tags:
            nekoframe.add_field(name='Доступные теги:',
                                value=', '.join(nekos_tags))

        else:
            nekoframe.set_image(url=get_neko(tag))

        await ctx.send(embed=nekoframe)

    @commands.command(name='avatar', aliases=['useravatar'])
    async def avatar(self, ctx, member: discord.Member = None):
        """Получить аватарку участника.

        Аргументы:
        `:member` - участник
        __                                            __
        Например:
        ```
        n!avatar Username
        n!avatar @Username#123
        ```
        """

        if not member:
            member = ctx.author

        if not member.avatar_url:
            a = discord.Embed(timestamp=ctx.message.created_at, color=0xfA0000, title=f'Аватарка {member}')
            a.set_image(url=member.default_avatar_url)
            a.set_footer(text=ctx.prefix + 'avatar [@пользователь]')
            await ctx.send(embed=a)

        else:
            a = discord.Embed(timestamp=ctx.message.created_at, color=0xfA0000, title=f'Аватарка {member}')
            a.set_image(url=member.avatar_url_as(static_format='png', size=1024))
            a.set_footer(text=ctx.prefix + 'avatar [@пользователь]')
            await ctx.send(embed=a)

def setup(bot):
    bot.add_cog(Fun(bot))
    print('[fun.py] Модуль "Member/Fun" загружен.')

# python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
from random import randint, choice
import requests
import discord
import apiai
import json
import os

import pokebase as pb
import asyncio

from utils.MemeGenerator import make_meme
from utils.NekosWrapper import (get_neko,
                                NekoNotInTags,
                                nekos_tags)

class Fun(object):
    """Команды пользователей - Fun"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='emote', aliases=['emotes'])
    async def emotes(self, ctx):
        """Эмоции и анимешные картинки <3"""
        if not ctx.invoked_subcommand:
            await ctx.send(f'{ctx.prefix}{ctx.command} -\nlove\nsad\njoy\nangry\nlonely')

    @emotes.command(name='love')
    async def love(self, ctx):
        """Влюбленность"""
        image = 'http://images.vfl.ru/ii/1540905231/0cf06cf3/24000410.jpg'
        author = ctx.message.author.name
        messages = [f'{author} полон любви и заботы <3']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @emotes.command(name='sad')
    async def sad(self, ctx):
        """Грусть"""
        image = 'http://images.vfl.ru/ii/1540905169/1859d59c/24000401.jpg'
        author = ctx.message.author.name
        messages = [f'{author} чувствует грусть :c',
                    f'Так печально, когда {author} грустит...']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @emotes.command(name='joy')
    async def joy(self, ctx):
        """Радость"""
        image = 'http://images.vfl.ru/ii/1540905081/27bd14ca/24000379.jpg'
        author = ctx.message.author.name
        messages = [f'Я рада, {author} счастлив!',
                    f'Счастья полон {author}, это так прекрасно! :з',
                    f'{author} счастлив! Меня это радует <3']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @emotes.command(name='angry')
    async def angry(self, ctx):
        """Злость"""
        image = 'http://images.vfl.ru/ii/1540904890/5fce2341/24000340.jpg'
        author = ctx.message.author.name
        messages = [f'{author} испытывает злость... Не стоит беспокоить его!',
                    f'Мне так грустно видеть, что {author} испытывает злость...',
                    f'{author} зол... Это наполняет меня грустью :c']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @emotes.command(name='lonely')
    async def lonely(self, ctx):
        """Одиночество"""
        image = 'http://images.vfl.ru/ii/1540905345/1bab6eb8/24000432.jpg'
        author = ctx.message.author.name
        messages = [f'Мне жаль {author}. Он чувствует одиночество :c',
                    f'Ах, как жаль... Чувство одинокости наполнило {author}...',
                    f'{author} чувствует одиночество...']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command(name='memegen')
    @commands.cooldown(1, 8, commands.BucketType.guild)
    async def memegen(self, ctx, *, text: commands.clean_content = 'Вот такие пироги'):
        """Генератор мемов. *Сооруди свой топовый мем!*

        [!] Команда может быть выполнена лишь раз в 8 секунд.

        Аргументы:
        `:text` - текст (% - перенос вниз)
        __                                            __
        Например:
        ```
        n!memegen Вот такие пироги
        ```
        """
        string_list = text.split('%')

        templates = [f'templates/{x}' for x in os.listdir('templates/')]

        if len(string_list) == 1:
            make_meme(topString='',
                    bottomString=string_list[0],
                    outputFilename=ctx.guild.id,
                    filename=choice(templates))
        elif len(string_list) >= 2:
            make_meme(topString=string_list[0],
                    bottomString=string_list[1],
                    outputFilename=ctx.guild.id,
                    filename=choice(templates))
        await ctx.send(file=discord.File(fp=f'{ctx.guild.id}.png'))
        await asyncio.sleep(5)
        os.remove(f'{ctx.guild.id}.png')

    @commands.command(name='vote4v')
    async def vote4v(self, ctx, *, msg: commands.clean_content):
        """Голосование A-B-C-D.

        Аргументы:
        `:message` - ваш вопрос
        __                                            __
        Например:
        ```
        n!vote2n Черный чай или зеленый? :thinking:
        ```
        """
        
        reactions = ['🇦', '🇧', '🇨', '🇩']

        embed = discord.Embed(title='Голосование открыто!',
                              description=msg)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        m = await ctx.send('Голосуем!', embed=embed)

        self.VOTE_A = 0
        self.VOTE_B = 0
        self.VOTE_C = 0
        self.VOTE_D = 0
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
                if str(r) == '🇦':
                    self.VOTE_A += 1
                if str(r) == '🇧':
                    self.VOTE_B += 1
                if str(r) == '🇨':
                    self.VOTE_C += 1
                if str(r) == '🇩':
                    self.VOTE_D += 1

                self.checked.append(u.id)
        checkloop = self.bot.loop.create_task(checking())
        await asyncio.sleep(30)
        checkloop.cancel()

        embed = discord.Embed(title='Голосование окончено!',
                              description=f'```{msg}```')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.add_field(name='Результаты:', value=f'🇦: {self.VOTE_A}\n🇧: {self.VOTE_B}\n🇨: {self.VOTE_C}\n🇩: {self.VOTE_D}')

        await ctx.send(embed=embed)

    @commands.command(name='vote2v')
    async def vote2n(self, ctx, *, msg: commands.clean_content):
        """Голосование A-B.

        Аргументы:
        `:message` - ваш вопрос
        __                                            __
        Например:
        ```
        n!vote2n Кому дать конфетку ставим "1"!
        n!vote2n Черный чай или зеленый? :thinking:
        ```
        """

        reactions = ['1⃣', '2⃣']

        embed = discord.Embed(title='Голосование открыто!',
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
                if str(r) == '1⃣':
                    self.voted_up += 1
                if str(r) == '2⃣':
                    self.voted_down += 1

                self.checked.append(u.id)
        checkloop = self.bot.loop.create_task(checking())
        await asyncio.sleep(30)
        checkloop.cancel()

        embed = discord.Embed(title='Голосование окончено!',
                              description=f'```{msg}```')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.add_field(name='Результаты:', value=f'1⃣: {self.voted_up}\n2⃣: {self.voted_down}')

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
            'вероятно, нет.', 'вряд ли...', 'очень сомневаюсь.', 'может быть.',
            'это невозможно!', 'мой ответ: Нет.', 'вообще понятия не имею.',
            'возможно, но шансы очень малы.', 'думаю, это возможно.', 'не отрицаю :thinking:',
            'мой ответ: Да.', 'полагаю, это так.', 'несомненно.', 'разумеется, да.']

        if len(message) <= 1:
            i_choice_it = randint(0, 5)
            return await ctx.send('{0}, {1}'.format(ctx.author.mention, possible[i_choice_it]))

        elif len(message) >= 15:
            i_choice_it = randint(0, 8)
            await ctx.send('{0}, {1}'.format(ctx.author.mention, possible[i_choice_it]))

        elif len(message) >= 2 and len(message) <= 14:
            i_choice_it = randint(0, 13)
            await ctx.send('{0}, {1}'.format(ctx.author.mention, possible[i_choice_it]))

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
        embed = discord.Embed(timestamp=ctx.message.created_at,
            color=randint(0x000000, 0xFFFFFF),
            description=f'{choice([x.mention for x in ctx.guild.members])} {message}')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='myname')
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
        await ctx.send('Успешно.', delete_after=5)

    @commands.command(name='talk', aliases=['t'])
    async def talk(self, ctx, lang: commands.clean_content = None, *, \
                    message: commands.clean_content):
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
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0xF13875)

        if tag not in nekos_tags:
            embed.add_field(name='Доступные теги:',
                            value=', '.join(nekos_tags))
        else:
            embed.set_image(url=get_neko(tag))

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

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

        embed = discord.Embed(timestamp=ctx.message.created_at, color=0xfA0000, title=f'Аватарка {member}')

        if not member.avatar_url:
            embed.set_image(url=member.default_avatar_url)
        else:
            embed.set_image(url=member.avatar_url_as(static_format='png', size=1024))

        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))

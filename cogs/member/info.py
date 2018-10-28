# python3.6
# -*- coding: utf-8 -*-

from discord.ext import commands
from random import randint
import discord
import json
import requests
import time
import psutil
import wikipedia as w

from utils.HelpPaginator import HelpPaginator, CannotPaginate
from mcstatus import MinecraftServer

class Info(object):
    """Команды пользователей - Info"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='invite')
    async def invite(self, ctx):
        """Получить ссылку для приглашения меня к Вам на сервер.
        """
        full_url = '<:naomi_arrow_up:506078581227651098> Хотите раскрыть все мои способности? [Клик сюда <3](https://discordapp.com/oauth2/authorize?client_id=452534618520944649&scope=bot&permissions=473197655)'
        low_url = '<:naomi_arrow_down:506078605672054785> Нужны только основные команды и ничего более? [И так тоже можно](https://discordapp.com/oauth2/authorize?client_id=452534618520944649&scope=bot&permissions=3435584)!'
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302,
                              title=f'Ссылки для приглашения',
                              description=f'{full_url}\n{low_url}')
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.set_author(name=ctx.message.author.name,
                         icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='wiki', aliases=['wikipedia', 'wikia'], hidden=True)
    @commands.is_owner()
    async def wiki(self, ctx, query: commands.clean_content):
        """[!InDev!] Поиск в Википедии.

        Аргументы:
        `:query` - Ваш запрос
        __                                            __
        Например:
        ```
        n!wikia Python
        ```
        """
        wiki_query = w.search(query)
        if len(wiki_query) >= 1:
            result = w.page(wiki_query[0])
            result = result.content[0:1940]
            url = f'.. [Читать далее]({result.url})'
        else:
            result = ':x: Я ничего не нашла на Википедии... Извините!'
            url = ''

        embed = discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302,
                              title=f'Поиск в Википедии - "{query}"',
                              description=f'{result}{url}')
        embed.set_footer(text=f'{ctx.prefix}{ctx.command} <query>')
        embed.set_author(name=ctx.message.author.name,
                         icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed)


    @commands.command(name='cryptoprice')
    async def cryptoprice(self, ctx, cryptocurrency: commands.clean_content = 'bitcoin', \
                            currency: commands.clean_content = 'rub'):
        """Стоимость криптовалют.

        Аргументы:
        `:cryptocurrency` - имя криптовалюты
        `:currency` - имя валюты
        __                                            __
        Например:
        ```
        n!cryptoprice bitcoin rub
        ```
        """

        request = requests.get(f'https://api.coinmarketcap.com/v1/ticker/{cryptocurrency}/?convert={currency}')
        resp = request.json()

        if type(resp) is dict:
            return await ctx.send(f'Что-то пошло не так.\n*Может быть, {ctx.author.mention} ввел несуществующую валюту?')

        price =  'price_' + currency.lower()

        try:
            resp[0][price]

        except KeyError:
            return await ctx.send(f'Что-то пошло не так.\n*Может быть, {ctx.author.mention} ввел несуществующую валюту?')

        await ctx.send(embed=discord.Embed(color=0xF4F624, title=f'Стоимость криптовалюты {cryptocurrency}.',
               description=f'USD: `{resp[0]["price_usd"]}`\n{currency.upper()}: `{resp[0][price]}`'))

    @commands.command(name='anime', aliases=['search-anime', 'aninfo'])
    async def anime(self, ctx, *, query: str):
        """Поиск аниме по названию.

        Аргументы:
        `:query` - название
        __                                            __
        Например:
        ```
        n!anime Re: Zero
        n!aninfo Another
        ```
        """
        async with ctx.typing():
            try:
                async with self.bot.session.get(f"https://api.jikan.moe/search/anime/{query}") as response:
                    data = await response.json()
                    embed = discord.Embed(timestamp=ctx.message.created_at, color=randint(0x000000, 0xFFFFFF), title=data["result"][0].get("title"))

                    embed.add_field(name="Описание:",               value=f"{data['result'][0].get('description')} **[Больше информации об {data['result'][0].get('title')}...]({data['result'][0].get('url')})**", inline=True)
                    embed.add_field(name="Эпизодов:",               value=f"**{data['result'][0].get('episodes')}**", inline=True)
                    embed.add_field(name="Оценка на MyAnimeList:",  value=f"**{data['result'][0].get('score')}/10**", inline=True)
                    embed.add_field(name="Пользователей:",          value=f"**{data['result'][0].get('members')}**", inline=True)
                    embed.add_field(name="Тип:",                    value=f"**{data['result'][0].get('type')}**", inline=True)

                    embed.set_thumbnail(url=data['result'][0].get('image_url'))
                    embed.set_footer(text=f"Поиск аниме - {query}", icon_url=ctx.author.avatar_url)
                    
                    await ctx.send(embed=embed)

            except KeyError:
                await ctx.send(f'По запросу ``{query}`` ничего не найдено..')

    @commands.command(name='about', aliases=['info'])
    async def about(self, ctx):
        """Некоторая информация обо мне.
        """

        github_url = 'https://github.com/AkiraSumato-01/Rewrite-Discord-Bot-Naomi'
        server_url = 'https://discord.gg/ZQfNQ43'
        discordbots_url = 'https://discordbots.org/bot/452534618520944649'
        invite_url = 'https://discordapp.com/oauth2/authorize?client_id=452534618520944649&scope=bot&permissions=490040390'

        embed = discord.Embed(timestamp=ctx.message.created_at, color=randint(0x000000, 0xFFFFFF),
                    title=f'Спасибо, что используете {self.bot.user.name}!',
                    description=f'''**[[GitHub]]({github_url}) [[Наш Discord сервер]]({server_url}) [[Пригласить меня]]({invite_url}) [[DiscordBots]]({discordbots_url})**

<:naomiserver:491308550707085312> Серверов: {len(self.bot.guilds)}
<:naomiusers:491313467962294296> Участников: {len(self.bot.users)}
<:naomicmds:491314340029530132> Команд: {len([x.name for x in self.bot.commands if not x.hidden])}
:smiley: Эмодзи: {len(self.bot.emojis)}

**Если вы довольны моим функционалом и хотите поддержать меня и моего разработчика, пожалуйста, [проголосуйте здесь](https://discordbots.org/bot/452534618520944649) <3**
**Мы надеемся на Вашу поддержку!**''')
        await ctx.send(embed=embed)

    @commands.command(name='help', aliases=['commands', 'cmds'])
    async def thelp(self, ctx, *, command:str=None):
        """Справочник по командам.

        Аргументы:
        `:command` - имя команды / категории.
        __                                            __
        Например:
        ```
        n!cmds
        n!help neko
        n!help Management
        ```
        """
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

    @commands.command(name='userinfo', aliases=['user-info'])
    @commands.guild_only()
    async def userinfo(self, ctx, member:discord.Member=None):
        """Показать информацию об участнике сервера.

        Аргументы:
        `:member` - участник сервера
        __                                            __
        Например:
        ```
        n!userinfo Username
        n!userinfo @Username#1234
        ```
        """

        if not member:
            member = ctx.author

        if member.nick == '':
            stats = discord.Embed(timestamp=ctx.message.created_at, color=0x18C30B, title='Информация об участнике %s (%s) [%s]' % (member.nick, member.name, member.id))
        else:
            stats = discord.Embed(timestamp=ctx.message.created_at, color=0x18C30B, title='Информация об участнике %s [%s]' % (member.name, member.id))

        if member.name == self.bot.user.name:
            owner = (await self.bot.application_info()).owner

            stats.add_field(name='Создал аккаунт', value=member.created_at)
            stats.add_field(name='Цвет никнейма', value=member.colour)
            stats.add_field(name='Кол-во ролей', value=len(member.roles))
            stats.add_field(name='Высшая роль', value=member.top_role.name)
            stats.add_field(name='Бот?', value=str(member.bot).replace('True', 'Да').replace('False', 'Нет'))
            stats.add_field(name='Серверов со мной', value=len(self.bot.guilds))
            stats.add_field(name='Мой разработчик', value=owner)
            stats.set_thumbnail(url=member.avatar_url)

        else:
            stats.add_field(name='Присоединился', value=member.joined_at)
            stats.add_field(name='Создал аккаунт', value=member.created_at)
            stats.add_field(name='Цвет никнейма', value=member.colour)
            stats.add_field(name='Кол-во ролей', value=len(member.roles))
            stats.add_field(name='Высшая роль', value=member.top_role.name)
            stats.add_field(name='Бот?', value=str(member.bot).replace('True', 'Да').replace('False', 'Нет'))
            stats.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=stats)

    @commands.command(name='guild', aliases=['server'])
    @commands.guild_only()
    async def guild(self, ctx):
        """Информация о сервере.
        """

        stats = discord.Embed(timestamp=ctx.message.created_at,
            color=0x18C30B,
            title='Информация о сервере %s [%s]' % (ctx.guild.name, ctx.guild.id))
        stats.add_field(name='Регион', value=ctx.guild.region)
        stats.add_field(name='Всего эмодзи', value=len(ctx.guild.emojis))
        stats.add_field(name='Всего участников', value=len(ctx.guild.members))
        stats.add_field(name='Всего ролей', value=len(ctx.guild.roles))
        stats.add_field(name='Текстовых каналов', value=len(ctx.guild.text_channels))
        stats.add_field(name='Голосовых каналов', value=len(ctx.guild.voice_channels))
        stats.add_field(name='Владелец', value=ctx.guild.owner)
        stats.add_field(name='Участников', value=len(ctx.guild.members))
        stats.add_field(name='Пользователей', value=len([x.name for x in ctx.guild.members if not x.bot]))
        stats.add_field(name='Ботов', value=len([x.name for x in ctx.guild.members if x.bot]))
        stats.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=stats)

    @commands.command(name='mcplayer', aliases=['mcuser'])
    async def mcplayer(self, ctx, nickname:str):
        """Статистика игрока Minecraft.

        Аргументы:
        `:nickname` - никнейм игрока
        __                                            __
        Например:
        ```
        n!mcplayer AkiraSumato_01
        n!mcuser Player
        ```
        """

        request = requests.get('https://minecraft-statistic.net/api/player/info/' + nickname)
        content = request.json()

        try:
            stats = discord.Embed(timestamp=ctx.message.created_at, color=0x18C30B, title='Статистика игрока %s' % content['data']['name'])
            stats.add_field(name='UUID', value=content['data']['uuid'])
            stats.add_field(name='Всего сыграно', value=content['data']['total_time_play'])
            stats.add_field(name='В сети?', value=str(content['data']['online']).replace('1', 'Да').replace('0', 'Нет'))
            stats.add_field(name='Лицензия?', value=str(content['data']['license']).replace('1', 'Да').replace('0', 'Нет'))
            # stats.add_field(name='Последний раз в сети', value=time.time() - content['data']['last_play'])
        except:
            stats = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text=ctx.prefix + 'mcplayer [ник]')
        await ctx.send(embed=stats)

    @commands.command(name='mcstats', aliases=['mcserver'])
    async def mcstats(self, ctx, adress: str):
        """Статистика сервера Minecraft.

        Аргументы:
        `:adress` - адрес сервера (домен / IP)
        __                                            __
        Например:
        ```
        n!mcserver hypixel.net
        n!mcstats play.hypixel.net:25565
        ```
        """

        try:
            server = MinecraftServer.lookup(adress)
            status = server.status()
        except ConnectionRefusedError:
            return await ctx.send(':x: Не удалось подключиться к серверу "%s".' % adress)

        try:
            stats = discord.Embed(timestamp=ctx.message.created_at, color=0x18C30B, description="```%s```" % ''.join([x['text'] for x in status.description['extra']]))
            stats.add_field(name='Адрес', value=server.host)
            stats.add_field(name='Порт', value=server.port)
            stats.add_field(name='Игроки', value='%s/%s' % (status.players.online, status.players.max))
            stats.add_field(name='Задержка', value='%s мс' % status.latency)
            stats.add_field(name='Ядро', value=status.version.name)
        except:
            stats = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text=ctx.prefix + 'mcstats [адрес_существующего_сервера]')

        await ctx.send(embed=stats)

    @commands.command(name='osu', aliases=['osu!'])
    async def osu(self, ctx, player: commands.clean_content, \
                            mode: commands.clean_content = 'osu!'):
        """Статистика игрока osu!

        Аргументы:
        `:player` - имя игрока
        `:mode` - режим (osu!, taiko, mania, catch)
        __                                            __
        Например:
        ```
        n!osu AkiraSumato_01 mania
        ```
        """

        if mode == 'osu!'  or mode == 'o':
            game_mode = {'num': 0, 'name': 'osu!'}

        if mode == 'taiko' or mode == 't':
            game_mode = {'num': 1, 'name': 'osu!taiko'}

        if mode == 'catch' or mode == 'ctb' or mode == 'c':
            game_mode = {'num': 2, 'name': 'osu!catch'}

        if mode == 'mania' or mode == 'm':
            game_mode = {'num': 3, 'name': 'osu!mania'}

        _colour = randint(0x000000, 0xFFFFFF)
        _tc = lambda: randint(0, 255)
        osu_desk_color = '%02X%02X%02X' % (_tc(), _tc(), _tc())

        _image_url = f'http://lemmmy.pw/osusig/sig.php?colour=hex{osu_desk_color}&uname={player}&mode={game_mode["num"]}&pp=1&countryrank&removeavmargin&flagshadow&flagstroke&darktriangles&opaqueavatar&avatarrounding=5&onlineindicator=undefined&xpbar&xpbarhex'

        osu_st = discord.Embed(timestamp=ctx.message.created_at, color=_colour, title=f'Статистика {player} в {game_mode["name"]}')
        osu_st.set_image(url=_image_url)
        osu_st.set_footer(text=ctx.prefix + 'osu [ник_игрока] | lemmy.pw')
        await ctx.send(embed=osu_st)

def setup(bot):
    bot.add_cog(Info(bot))
    print('[info.py] Модуль "Member/Info" загружен.')

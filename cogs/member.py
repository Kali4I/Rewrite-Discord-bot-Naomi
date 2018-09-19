import discord
import nekos
import whois
import json
import time
import apiai
import requests
from discord.ext import commands
from random import choice, randint
from mcstatus import MinecraftServer

from utils.HelpPaginator import HelpPaginator, CannotPaginate

class Member(object):

    def __init__(self, bot):
        self.bot = bot






    @commands.command(name='myname', aliases=['my-name'])
    async def myname(self, ctx, *, nickname:str=None):
        """Сменить Ваш никнейм.

        Подробности:
        --------------
        [nickname] - новый никнейм (ничего для сброса).
        """

        try:
            await ctx.author.edit(nick=nickname, reason='Запрошено пользователем.')
        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='У меня нет прав.'))








    @commands.command(name='idea', aliases=['myidea', 'my-idea'])
    async def idea(self, ctx, *, message:str):
        """Поделиться Вашей идеей для меня.

        Подробности:
        --------------
        <message> - описание вашей идеи.
        """

        try:
            ideas_guild = discord.utils.get(self.bot.guilds, id=457092470472179712)
            ideas_channel = discord.utils.get(ideas_guild.channels, id=483662616921767956)

            await ctx.send('Ваша идея отправлена на наш Discord-сервер;\n Спасибо за помощь.')
            await ideas_channel.send(embed=discord.Embed(color=0xF56415, 
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

        try:
            rep_guild = discord.utils.get(self.bot.guilds, id=457092470472179712)
            rep_channel = discord.utils.get(rep_guild.channels, id=483662931377127424)

            await ctx.send('Ваш баг-репорт отправлен на наш Discord-сервер;\n Спасибо за помощь.')
            await rep_channel.send(embed=discord.Embed(color=0xF56415, 
                                title='Новый баг-репорт!',
                                description='Отправил: %s\nОписание:```markup\n%s```\n\n%s' % (ctx.author, message, time.ctime())))
        except Exception as e:
            await ctx.send('Не удалось отправить репорт.\n%s' % e)






    @commands.command(name='help', aliases=['info', 'h'])
    async def thelp(self, ctx, *, command:str=None):
        """Справочник по командам.

        Подробности:
        --------------
        [command] - команда, описание которой нужно показать.
            (например, `help osu`)
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
    async def userinfo(self, ctx, member:discord.Member=None):
        """Информация об участнике сервера.

        Подробности:
        --------------
        [member] - участник.
            (если не указан, выдается информация об авторе команды)
        """

        if not member:
            member = ctx.author

        if member.nick == '':
            stats = discord.Embed(color=0x18C30B, title='Информация об участнике %s (%s) [%s]' % (member.nick, member.name, member.id))
        else:
            stats = discord.Embed(color=0x18C30B, title='Информация об участнике %s [%s]' % (member.name, member.id))

        if member.name == self.bot.user.name:
            owner = (await self.bot.application_info()).owner

            stats.add_field(name='Присоединился', value=self.bot.user.joined_at)
            stats.add_field(name='Создал аккаунт', value=self.bot.user.created_at)
            stats.add_field(name='Цвет никнейма', value=self.bot.user.colour)
            stats.add_field(name='Кол-во ролей', value=len(self.bot.user.roles))
            stats.add_field(name='Высшая роль', value=self.bot.user.top_role.name)
            stats.add_field(name='Бот?', value='Да')
            stats.add_field(name='Серверов со мной', value=len(self.bot.guilds))
            stats.add_field(name='Мой разработчик', value=owner)
            stats.set_thumbnail(url=self.bot.user.avatar_url)

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
    async def guild(self, ctx):
        """Информация о гильдии (Discord-сервере).

        Подробности:
        --------------
        Аргументы не требуются.
        """

        stats = discord.Embed(color=0x18C30B, title='Информация о сервере %s [%s]' % (ctx.guild.name, ctx.guild.id))
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

        Подробности:
        --------------
        <nickname> - никнейм игрока Minecraft.
        """

        request = requests.get('https://minecraft-statistic.net/api/player/info/' + nickname)
        content = request.json()

        try:
            stats = discord.Embed(color=0x18C30B, title='Статистика игрока %s' % content['data']['name'])
            stats.add_field(name='UUID', value=content['data']['uuid'])
            stats.add_field(name='Всего сыграно', value=content['data']['total_time_play'])
            stats.add_field(name='В сети?', value=str(content['data']['online']).replace('1', 'Да').replace('0', 'Нет'))
            stats.add_field(name='Лицензия?', value=str(content['data']['license']).replace('1', 'Да').replace('0', 'Нет'))
            stats.add_field(name='Последний раз в сети', value=time.time() - content['data']['last_play'])
        except:
            stats = discord.Embed(color=0xff0000).set_footer(text='mcplayer [ник]')

        await ctx.send(embed=stats)






    @commands.command(name='mcstats', aliases=['mcserver', 'mcserv', 'mcinfo', 'mcstatus'])
    async def mcstats(self, ctx, adress:str):
        """Статистика сервера Minecraft.

        Подробности:
        --------------
        <adress> - IP адрес или домен сервера Minecraft.
        """

        server = MinecraftServer.lookup(adress)
        status = server.status()

        try:
            stats = discord.Embed(color=0x18C30B, description="```%s```" % ''.join([x['text'] for x in status.description['extra']]))
            stats.add_field(name='Адрес', value=server.host)
            stats.add_field(name='Порт', value=server.port)
            stats.add_field(name='Игроки', value='%s/%s' % (status.players.online, status.players.max))
            stats.add_field(name='Задержка', value='%s мс' % status.latency)
            stats.add_field(name='Ядро', value=status.version.name)
        except:
            stats = discord.Embed(color=0xff0000).set_footer(text='mcstats [адрес_существующего_сервера]')

        await ctx.send(embed=stats)






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
                                '(Как же ответить, как же ответить...)',
                                'Извиняюсь, но я не знаю, как ответить...'])
            await ctx.send(no_answer)






    @commands.command(name='hostinfo', aliases=['host', 'whoisweb'])
    async def hostinfo(self, ctx, domain:str):
        """WHOIS-информация о домене.

        Подробности:
        --------------
        <domain> - домен (например google.com).
        """

        whois_info = whois.whois(domain)

        hostinfo = discord.Embed(color=0xff0000, title=f'WHOIS-информация для {domain}')

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






    @commands.command(name='helloworld', description='Hello World!!', aliases=['hw'])
    async def _helloworld(self, ctx):
        await ctx.send('Hello, %s' % ctx.author.mention)






    @commands.command(name='say', aliases=['repeat', 'msg'])
    async def _say(self, ctx, *, msg:str):
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






    @commands.command(name='neko', aliases=['anime', 'catgirl', 'nekogirl'])
    async def _catgirl(self, ctx, tag:str=None):
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
                return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='Вы не в NSFW канале!'))
        except:
            pass

        tags = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
                'solog', 'feetg', 'cum', 'erokemo', 'les', 'lewdk', 'ngif',
                'tickle', 'lewd', 'feed', 'eroyuri', 'eron', 'cum_jpg',
                'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'poke',
                'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo', 'keta',
                'blowjob', 'pussy', 'tits', 'holoero', 'pussy_jpg', 'pwankg',
                'classic', 'kuni', 'pat', 'kiss', 'femdom', 'neko', 'cuddle',
                'erok', 'fox_girl', 'boobs', 'smallboobs', 'hug', 'ero', 'wallpaper']

        n = discord.Embed(color=0xF13875)

        if tag is None:
            n.set_image(url=nekos.img(choice(tags)))

        else:
            if tag in [x for x in tags]:
                n.set_image(url=nekos.img(tag))

            else:
                n.add_field(name='Доступные теги:', value=', '.join(tags))

        await ctx.send(embed=n)






    @commands.command(name='calc', aliases=['calculator', 'calculate'])
    async def _calc(self, ctx, *, numbers:str):
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
            return await ctx.send(embed=discord.Embed(color=0xfA0000).set_footer(text='Недопустимо по причине снижения производительности.'))

        else:
            try: __eval = str(eval(b))
            except ZeroDivisionError: __eval = '∞'
            except Exception as e:
                return await ctx.send(embed=discord.Embed(color=0xf0a302).set_footer(text='Выражение имеет ошибку.\nИсправьте его.'))

            if len(__eval) > 12 and not __eval.isnumeric():
                await ctx.send(embed=discord.Embed(color=0xf0a302, description=f'```css\n{numbers}\n({b})\n```(Указаны первые 12 цифр)\n{__eval[:12]}\n\nОкругленный:\n{round(float(__eval))}').set_footer(text='calc [матем.выражение]'))

            elif len(__eval) > 12 and __eval.isnumeric():
                await ctx.send(embed=discord.Embed(color=0xf0a302, description=f'```css\n{numbers}\n({b})\n```(Указаны первые 12 цифр)\n{__eval[:12]}').set_footer(text='calc [матем.выражение]'))

            else:
                await ctx.send(embed=discord.Embed(color=0xf0a302, description=f'```css\n{numbers}\n({b})\n```{__eval}').set_footer(text='calc [матем.выражение]'))






    @commands.command(name='osu', aliases=['osu!'])
    async def osu(self, ctx, player:str, mode:str=None):
        """Статистика игрока osu!.

        Подробности:
        --------------
        <player> - никнейм игрока osu!.
        [mode] - режим игры.
            (mania, catch, osu!, taiko)
        """

        if not mode:
            mode = 'osu!'

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

        osu_st = discord.Embed(color=_colour, title=f'Статистика {player} в {game_mode["name"]}')
        osu_st.set_image(url=_image_url)
        osu_st.set_footer(text='osu [ник_игрока] | lemmy.pw')
        await ctx.send(embed=osu_st)






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
            a = discord.Embed(color=0xfA0000, title=f'Аватарка {member}')
            a.set_image(url=member.default_avatar_url)
            a.set_footer(text='avatar [@пользователь]')
            await ctx.send(embed=a)

        else:
            a = discord.Embed(color=0xfA0000, title=f'Аватарка {member}')
            a.set_image(url=member.avatar_url_as(static_format='png', size=1024))
            a.set_footer(text='avatar [@пользователь]')
            await ctx.send(embed=a)







def setup(bot):
    bot.add_cog(Member(bot))
    print('[member.py] Модуль стандартных команд загружен.')
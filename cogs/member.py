import discord
import nekos
import whois
import json
import apiai
from discord.ext import commands
from random import choice, randint
from mcstatus import MinecraftServer

class Member(object):

    def __init__(self, bot):
        self.bot = bot






    @commands.command(name='mcstats', description='Статистика сервера Minecraft.', aliases=['mcserver', 'mcserv', 'mcinfo'])
    async def mcstats(self, ctx, adress:str=None):

        if not adress:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='mcstats [адрес_сервера]'))

        server = MinecraftServer.lookup(adress)
        status = server.status()

        try:
            stats = discord.Embed(color=0x18C30B, description="```%s```" % (''.join([x['text'] for x in s.description['extra']])))
            stats.add_field(name='Адрес', value=server.host)
            stats.add_field(name='Порт', value=server.port)
            stats.add_field(name='Игроки', value='%s/%s' % (status.players.online, status.players.max))
            stats.add_field(name='Задержка', value='%s мс' % status.latency)
            stats.add_field(name='Ядро', value=status.version.name)
        except:
            stats = discord.Embed(color=0xff0000).set_footer(text='mcstats [адрес_существующего_сервера]')

        await ctx.send(embed=stats)






    @commands.command(name='help', description='Справочник по командам.', aliases=['info', self.bot.user.mention])
    async def help(self, ctx):

        naomiserver = discord.utils.get(discord.utils.get(self.bot.guilds, id=347635213670678528).emojis, name='naomiserver')
        naomiusers = discord.utils.get(discord.utils.get(self.bot.guilds, id=347635213670678528).emojis, name='naomiusers')
        naomicmds = discord.utils.get(discord.utils.get(self.bot.guilds, id=347635213670678528).emojis, name='naomicmds')

        help_main = f'''
Спасибо, что используете {self.bot.user.name}!

{naomiserver} | Серверов: {len(self.bot.guilds)}
{naomiusers} | Пользователей: {len(self.bot.users)}
:smiley: | Эмодзи: {len(self.bot.emojis)}
{naomicmds} | Команд: {len(self.bot.all_commands)}


Некоторая помощь в разработке - [F4stZ4p](https://github.com/F4stZ4p)

Для навигации по справочнику,
используйте реакции под этим сообщением
в качестве панели управления.
'''
        help_f01 = f'''```css
play     | Музыка;
neko     | [#] Аниме арты;
talk     | Общение с ботом;
avatar   | Получить аватарку пользователя;
osu      | Статистика игрока osu!;
say      | Отправка сообщения от имени бота;```
`[#] - только в NSFW-каналах.`
`[*] - требуются права Администратора.`
`[X] - команда не завершена.`
'''
        help_f02 = f'''```css
banlist  | [*] Банлист;
purge    | [*] Очистка чата;
kick     | [*] Выгнать пользователя;
ban      | [*] Забанить пользователя;
unban    | [X];```
`[#] - только в NSFW-каналах.`
`[*] - требуются права Администратора.`
`[X] - команда не завершена.`
'''
        help_f03 = f'''```css
help     | Список команд;
hostinfo | WHOIS-информация о домене;
calc     | Калькулятор;
guild    | [X];
bot      | [X];```
`[#] - только в NSFW-каналах.`
`[*] - требуются права Администратора.`
`[X] - команда не завершена.`
'''

        _description = f'[「Наш Discord-сервер」](https://discord.gg/ZQfNQ43) [「Пригласить меня」](https://discordapp.com/oauth2/authorize?client_id=452534618520944649&scope=bot&permissions=301296759) [「GitHub」](https://github.com/AkiraSumato-01/Discord-Bot-Naomi)  \nПрефикс на этом сервере: '

        help_list = {
            'page_00': discord.Embed(color=0x00C6FF, title=':page_facing_up: Справочник по командам', description=_description),
            'page_01': discord.Embed(color=0x00C6FF, title=':page_facing_up: Справочник по командам', description=_description),
            'page_02': discord.Embed(color=0x00C6FF, title=':page_facing_up: Справочник по командам', description=_description),
            'page_03': discord.Embed(color=0x00C6FF, title=':page_facing_up: Справочник по командам', description=_description),
        }


        help_list['page_00'].set_footer(text=f'help | Главная')
        help_list['page_00'].add_field(name='Главная:', value=help_main)

        help_list['page_01'].set_footer(text=f'help | Стр. #1')
        help_list['page_01'].add_field(name='Развлечение:', value=help_f01)

        help_list['page_02'].set_footer(text=f'help | Стр. #2')
        help_list['page_02'].add_field(name='Администрирование:', value=help_f02)

        help_list['page_03'].set_footer(text=f'help | Стр. #3')
        help_list['page_03'].add_field(name='Прочее:', value=help_f03)

        _buttons = {
            '⬛': '00',
            '1⃣': '01',
            '2⃣': '02',
            '3⃣': '03'
        }

        _user_ = ctx.author

        _current = await ctx.send(embed=help_list['page_00'], delete_after=120)

        async def __menu_controller(current, help_list, _buttons):
            for react in _buttons:
                await current.add_reaction(react)

            def check(r, u):
                if not current:
                    return False
                elif str(r) not in _buttons.keys():
                    return False
                elif u.id != _user_.id or r.message.id != current.id:
                    return False
                return True

            while current:
                react, user = await self.bot.wait_for('reaction_add', check=check)
                try:
                    control = _buttons.get(str(react))
                except:
                    control = None


                if control == '00':
                    await current.edit(embed=help_list['page_00'])
                if control == '01':
                    await current.edit(embed=help_list['page_01'])
                if control == '02':
                    await current.edit(embed=help_list['page_02'])
                if control == '03':
                    await current.edit(embed=help_list['page_03'])

                try:
                    await current.remove_reaction(react, user)
                except discord.HTTPException:
                    pass
                    
        self.bot.loop.create_task(__menu_controller(_current, help_list, _buttons))






    @commands.command(name='talk', description='Общение с ботом.', aliases=['t'])
    async def _talking(self, ctx, *, message:str=None):
        if not message:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='talk [сообщение] | Dialogflow'))
        
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






    @commands.command(name='hostinfo', description='WHOIS-информация о домене.', aliases=['host', 'whoisweb'])
    async def _hostinfo(self, ctx, domain:str=None):

        if not domain:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='hostinfo [домен]'))

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






    @commands.command(name='say', description='Повторить сообщение пользователя.', aliases=['repeat', 'msg'])
    async def _say(self, ctx, *, msg:str=None):
        if msg is None:
            await ctx.send('%s, вы не указали сообщение.' % ctx.author.mention)
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(msg)






    @commands.command(name='neko', description='Отправляет аниме изображение [Только в NSFW-каналах]', aliases=['anime', 'catgirl', 'nekogirl'])
    async def _catgirl(self, ctx, tag:str=None):
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

        print([x for x in tags])

        if tag is None:
            n.set_image(url=nekos.img(choice(tags)))

        else:
            if tag in [x for x in tags]:
                n.set_image(url=nekos.img(tag))

            else:
                n.add_field(name='Доступные теги:', value=', '.join(tags))

        await ctx.send(embed=n)






    @commands.command(name='calc', description='Калькулятор', aliases=['calculator', 'calculate'])
    async def _calc(self, ctx, *, numbers:str=None):
        if not numbers:
            return await ctx.send(embed=discord.Embed(color=0xff00ff).set_footer(text='calc [матем.выражение]'))

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
                await ctx.send(embed=discord.Embed(color=0xf0a302, description=f'(Указаны первые 12 цифр)\n{__eval[:12]}\n\nОкругленный:\n{round(float(__eval))}').set_footer(text='calc [матем.выражение]'))

            elif len(__eval) > 12 and __eval.isnumeric():
                await ctx.send(embed=discord.Embed(color=0xf0a302, description=f'(Указаны первые 12 цифр)\n{__eval[:12]}').set_footer(text='calc [матем.выражение]'))

            else:
                await ctx.send(embed=discord.Embed(color=0xf0a302, description=f'{__eval}').set_footer(text='calc [матем.выражение]'))






    @commands.command(name='osu', description='Статистика игрока osu!.', aliases=['osu!'])
    async def _osu(self, ctx, player:str=None, mode:str='osu!'):

        if not player:
            return await ctx.send(embed=discord.Embed(color=0xD587F2).set_footer(text='osu [ник_игрока] | lemmy.pw'))

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






    @commands.command(name='avatar', description='Выдает аватарку пользователя.', aliases=['useravatar'])
    async def _avatar(self, ctx, member:discord.Member=None):

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
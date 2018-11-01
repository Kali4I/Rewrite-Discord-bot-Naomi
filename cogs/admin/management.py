import discord
import asyncio
from discord.ext import commands
from random import choice
import traceback


class Management(object):
    """Набор команд для Администрирования."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setcolor', aliases=['givecolor'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def set_member_color(self, ctx, color: discord.Color, member: discord.Member = None):
        """Разукрасить ник участника. *Да будут яркие краски и цвета!*

        [!] В разработке.

        Аргументы:
        `:color` - цвет в HEX
        __                                            __
        Например:
        ```
        n!setcolor FFCC33
        n!givecolor FF0000 @Username#1234
        ```
        """
        if not member:
            member = ctx.message.author

        role_exists = f'NaomiColored - {member.name}' in [x.name for x in member.roles]
        
        try:
            if role_exists:
                role = discord.utils.get(ctx.guild.roles, name=f'NaomiColored - {member.name}')
                await role.edit(color=color)
                await ctx.send('%s, ваша цветовая роль успешно изменена (новый цвет: %s).' % (member.mention, color))
            else:
                role = await ctx.guild.create_role(name=f'NaomiColored - {member.name}', color=color)
                await member.add_roles(role)
                await ctx.send('%s, вам успешно добавлена роль с цветом %s' % (member.mention, color))
        except discord.errors.HTTPException:
            await ctx.send(':x: Не удалось. \nВозможно, вы неверно ввели цвет?\nПроверьте на всякий случай: %s' % color)

    @commands.command(name='pin')
    @commands.has_permissions(manage_messages=True)
    async def pin_message(self, ctx, *, message: commands.clean_content):
        """Скопировать ваше сообщение в стильную и современную рамку, а затем закрепить его!

        Аргументы:
        `:message` - сообщение
        __                                            __
        Например:
        ```
        n!pin Этот текст был написан древними Эльфами во имя Discord!
        ```
        """
        embed = discord.Embed(color=0x71f442,
                              title='Закрепить это!',
                              description=message)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        msg = await ctx.send(embed=embed)
        await msg.pin()

    @commands.command(name='resetmute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def resetmute(self, ctx):
        """Сбросить настройки `n!mute` и удалить роль NaomiMute. *Когда настали мирные времена без флуда!*
        """

        mute = discord.utils.get(ctx.guild.roles, name='NaomiMute')
        if not mute:
            return await ctx.send('Нечего сбрасывать.')

        try:
            await mute.delete()

        except discord.errors.Forbidden:
            await ctx.message.add_reaction('❌')

        else:
            await ctx.message.add_reaction('✅')

    @commands.command(name='mute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = 'отсутствует'):
        """Приглушить участника. *Он не сможет отправлять сообщения, круто!*

        Аргументы:
        `:member` - участник
        `:reason` - причина
        __                                            __
        Например:
        ```
        n!mute @Username#1234 Спам
        n!mute Username
        ```
        Для корректной работы команды мне нужно внести некоторые правки в текстовые каналы и роли на этом сервере.
        [!?] Какие правки будут внесены?
        > Будет создана роль NaomiMute;
        > Роль NaomiMute будет добавлена в настройки доступа всех текстовых каналов;
        > У всех ролей (кроме @everyone) будет убрано право "send_messages" (отправка сообщений);```
        """
        mute = discord.utils.get(ctx.guild.roles, name='NaomiMute')

        if not mute:
            try:
                def message_check(m):
                    return m.author.id == ctx.author.id

                failed_channels = []
                failed_roles = []

                await ctx.send(f'Команда {ctx.prefix}{ctx.command} использована первый раз на этом сервере.\nМогу-ли я внести правки в настройки каналов и ролей для корректной работы этой команды? (Да/Нет)', delete_after=120.0)
                msg = await self.bot.wait_for('message', check=message_check, timeout=120.0)

                if msg.content.lower() in ['да', 'ага', 'угу']:
                    counter_msg = await ctx.send('Хорошо, выполняю... \nМодификация каналов: в ожидании.\nМодификация ролей: в ожидании.')

                    mute = await ctx.guild.create_role(name='NaomiMute',
                                                reason='Использована команда n!mute, но роль "NaomiMute" отсутствовала.')

                    modified_channels = 0
                    modified_roles = 0
                    for tchannel in ctx.guild.text_channels:
                        try:
                            await tchannel.set_permissions(mute,
                                                            send_messages=False,
                                                            add_reactions=False)

                        except:
                            failed_channels.append(f'`{tchannel.name}`')

                        else:
                            modified_channels += 1
                            try:
                                await counter_msg.edit(content=f'Хорошо, выполняю... \nМодификация каналов: {modified_channels}/{len(ctx.guild.text_channels)}\nМодификация ролей: в ожидании.')
                            except:
                                pass

                    # mute_perms = discord.Permissions()
                    # mute_perms.update(send_messages=False)
                    # К черту discord.Permissions()

                    mute_perms = discord.PermissionOverwrite()
                    mute_perms.send_messages = False
                    mute_perms.add_reactions = False

                    for role in ctx.guild.roles:
                        if role != ctx.guild.default_role:
                            try:
                                await role.edit(permissions=mute_perms)
                            except:
                                failed_roles.append(f'`{role.name}`')
                            else:
                                modified_roles += 1
                            await counter_msg.edit(content=f'Хорошо, выполняю... \nМодификация каналов: {modified_roles}/{len(ctx.guild.text_channels)}.\nМодификация ролей: {x1}/{len(ctx.guild.roles) - 1}')
                else:
                    return await ctx.send(':x: Отменено.')
            except asyncio.TimeoutError:
                await ctx.send('Я не столь терпелива, чтобы ждать ответа так долго...\nПросто повторно введите команду.')
        try:
            if not len(failed_channels) == 0 or not len(failed_roles) == 0:
                await ctx.send(f'Модификация завершена не полностью:\n- Каналы: {", ".join(failed_channels)}\n- Роли: {", ".join(failed_roles)}')
        except:
            pass

        await member.add_roles(mute, reason='Был приглушен через n!mute.')

        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x35FF81, description=f'Участник {member.mention} приглушен.\nПричина: {reason}')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='unmute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = 'отсутствует'):
        """Снять приглушение с участника. *Да будет свобода чата!*

        Аргументы:
        `:member` - участник
        `:reason` - причина
        __                                            __
        Например:
        ```
        n!unmute @Username#1234
        n!unmute Username Просто так
        ```
        """

        mute = discord.utils.get(ctx.guild.roles, name='NaomiMute')

        if not mute:
            embed = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000,
                            description='Не найдена роль "NaomiMute", а раз ее нет, то и снимать мут мне не с кого...')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        elif mute not in member.roles:
            embed = discord.Embed(timestamp=ctx.message.created_at, color=0xff0000,
                            description=f'{member.mention} не приглушен!')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        else:
            await member.remove_roles(mute, reason='Приглушение снято - n!unmute.')

            embed = discord.Embed(timestamp=ctx.message.created_at, color=0x35FF81,
                    description=f'Снято приглушение с участника {member.mention}.\nПричина: {reason}')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='newname', aliases=['new-name', 'change-name', 'changename', 'newnick'])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def newname(self, ctx, member: discord.Member, *, nickname: str = None):
        """Сменить никнейм участника.

        Аргументы:
        `:member` - участник
        `:nickname` - новый никнейм (оставьте пустым для сброса)
        __                                            __
        Например:
        ```
        n!newname @Username#1234 Топ пользователь
        n!newname Username Ламповая няша
        ```
        """

        await member.edit(nick=nickname, reason='n!newname в помощь участникам! xD')
        
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                description='Никнейм успешно изменен.')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='cleanup')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def cleanup(self, ctx, member: discord.Member, count: int):
        """Удалить сообщения конкретного участника.

        Аргументы:
        `:member` - участник
        `:count` - кол-во сообщений
        __                                            __
        Например:
        ```
        n!cleanup @Username#1234 5
        n!cleanup Username 100
        ```
        """
        if count > 100:
            await ctx.send(f'Число сообщений не должно превышать {count}.')
        else:
            def is_member(m):
                return m.author == member
            await ctx.channel.purge(limit=count, check=is_member)

    @commands.command(name='purge', aliases=['clean', 'clear', 'clearchat'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, count: int):
        """Удалить последние сообщения в чате. *Во имя чистоты чата!*

        Аргументы:
        `:count` - кол-во сообщений.
        __                                            __
        Например:
        ```
        n!purge 100
        ```
        """
        if count > 100:
            await ctx.send(f'Число сообщений не должно превышать {count}')
        else:
            await ctx.channel.purge(limit=count)

    @commands.command(name='ban')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = 'отсутствует'):
        """Заблокировать участника на сервере. *Да вознесется банхаммер над <member>!*

        Аргументы:
        `:member` - участник
        `:reason` - причина
        __                                            __
        Например:
        ```
        n!ban Username Ты был плохим парнем
        n!ban @Username#1234
        ```
        """
        await ctx.guild.ban(user=member, reason=reason)

        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                description=f'Пользователь {member.mention} забанен!\nПричина: {reason}.')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='unban', aliases=['pardon'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason: str = 'отсутствует'):
        """Разблокировать участника на сервере.

        Аргументы:
        `:user` - пользователь
        `:reason` - причина
        __                                            __
        Например:
        ```
        n!unban @Username#1234 Ты хороший
        ```
        """
        ban_entries = await ctx.guild.bans()
        banned_users = [user.user.name for user in ban_entries]

        for u in banned_users:
            if u.id == user.id:
                try:
                    await ctx.guild.unban(user=u, reason=reason)
                except:
                    stats = f'Не удалось разбанить {user}.'
                else:
                    stats = f'Пользователь {u.mention} успешно разбанен.'

        embed = discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000,
                description=stats)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='banlist', aliases=['bans'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def banlist(self, ctx):
        """Список заблокированных участников.
        """
        bans = await ctx.guild.bans()

        if len(bans) <= 0:
            embed = discord.Embed(timestamp=ctx.message.created_at,
                            color=0xff0000,
                            description='Забаненных пользователей нет.')
        else:
            embed = discord.Embed(timestamp=ctx.message.created_at,
                            color=0xff0000,
                            description=f'Забаненные пользователи:\n{", ".join([user.user.name for user in bans])}')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)

    @commands.command(name='kick')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = 'отсутствует'):
        """Выгнать участника с сервера.

        Аргументы:
        `:member` - участник
        `:reason` - причина
        __                                            __
        Например:
        ```
        n!kick Username Ты плохой
        n!kick @Username#1234
        ```
        """
        await member.kick(reason=reason)

        embed = discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00,
                description=f'Пользователь {member} был кикнут.\nПричина: {reason}.')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Management(bot))
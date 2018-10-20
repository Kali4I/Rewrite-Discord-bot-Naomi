import discord
import asyncio
from discord.ext import commands
from random import choice
import traceback


class Admin(object):
    """Набор команд для Администрирования."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pin')
    @commands.has_permissions(manage_messages=True)
    async def pin_message(self, ctx, *, message: commands.clean_content):
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
        """Удаляет роль NaomiMute сбрасывая настройки n!mute в исходное состояние.
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
    async def mute(self, ctx, member: discord.Member, *, reason: str=None):
        """Приглушить участника (он не сможет отправлять сообщения).

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

        if not reason:
            reason = 'отсутствует'

        try:
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


                        mute_perms = discord.Permissions()
                        mute_perms.update(send_messages=False)

                        for role in ctx.guild.roles:
                            if role != ctx.guild.default_role:
                                try:
                                    await role.edit(permissions=mute_perms)

                                except:
                                    failed_roles.append(f'`{role.name}`')

                                else:
                                    modified_roles += 1
                                try:
                                    await counter_msg.edit(content=f'Хорошо, выполняю... \nМодификация каналов: {modified_roles}/{len(ctx.guild.text_channels)}.\nМодификация ролей: {x1}/{len(ctx.guild.roles) - 1}')
                                except:
                                    pass

                    elif msg.content.lower() in ['нет', 'не', 'не-а', 'неа']:
                        await ctx.send('В таком случае, команда может работать некорректно.')

                    else:
                        return await ctx.send(':x: Отменено.', delete_after=10)

                except asyncio.TimeoutError:
                    await ctx.send('Я не столь терпелива, чтобы ждать ответа так долго...\nПросто повторно введите команду.', delete_after=10)
                    await asyncio.sleep(10)
                    await ctx.message.delete()
                    return False

            try:
                if not len(failed_channels) == 0 or not len(failed_roles) == 0:
                    await ctx.send(f'Модификация завершена не полностью:\n- Каналы: {", ".join(failed_channels)}\n- Роли: {", ".join(failed_roles)}')
            except:
                pass

            await member.add_roles(mute, reason='Был приглушен через n!mute.')

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

        except Exception:
            await ctx.send(f'```python\n{traceback.format_exc()}```', delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0x35FF81, description=f'Участник {member.mention} приглушен.\nПричина: {reason}'), delete_after=20)
        await asyncio.sleep(20)
        await ctx.message.delete()
        return True

    @commands.command(name='unmute')
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str=None):
        """Снять приглушение с участника.

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

        if not reason:
            reason = 'отсутствует'

        try:
            if not mute:
                return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000, description='Не найдена роль "NaomiMute", а раз ее нет, то и снимать мут мне не с кого...'))

            if mute not in member.roles:
                return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000, description=f'{member.mention} не приглушен!'))

            await member.remove_roles(mute, reason='Приглушение снято - n!unmute.')

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

        await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0x35FF81, description=f'Снято приглушение с участника {member.mention}.\nПричина: {reason}'), delete_after=20)
        await asyncio.sleep(20)
        await ctx.message.delete()
        return True

    @commands.command(name='newname', aliases=['new-name', 'change-name', 'changename', 'newnick'])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def newname(self, ctx, member: discord.Member, *, nickname: str=None):
        """Сменить никнейм участника.

        Аргументы:
        `:member` - участник
        `:nickname` - новый никнейм (оставьте пустым для сброса)
        __                                            __
        Например:
        ```
        n!newname @Username#1234 Топ пользователь
        n!newname Username Я топ чел
        ```
        """

        try:
            await member.edit(nick=nickname, reason='Запрошено, используя n!newname.')

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

    @commands.command(name='cleanup')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def cleanup(self, ctx, member: discord.Member, count: int=None):
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
            return await ctx.send(f'Число сообщений не должно превышать {count}.')

        def is_member(m):
            return m.author == member

        try:
            await ctx.channel.purge(limit=count, check=is_member)

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

    @commands.command(name='purge', aliases=['clean', 'clear', 'clearchat'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, count: int):
        """Удалить последние сообщения в чате.

        Аргументы:
        `:count` - кол-во сообщений.
        __                                            __
        Например:
        ```
        n!purge 100
        ```
        """
        if count > 100:
            return await ctx.send(f'Число сообщений не должно превышать {count}')

        try:
            await ctx.channel.purge(limit=count)

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

    @commands.command(name='ban')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str=None):
        """Заблокировать участника на сервере.

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
        if not reason:
            reason = 'отсутствует.'
        try:
            await ctx.guild.ban(user=member, reason=reason)

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

        else:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00, description=f'Пользователь {member} забанен!\nПричина: {reason}.').set_footer(text='ban [@пользователь] [причина]'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

    @commands.command(name='unban', aliases=['pardon'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason: str=None):
        """Разблокировать участника на сервере.

        Аргументы:
        `:member` - участник
        `:reason` - причина
        __                                            __
        Например:
        ```
        n!unban @Username#1234 Ты хороший
        n!unban Username
        ```
        """
        if not reason:
            reason = 'отсутствует.'

        try:
            ban_entries = await ctx.guild.bans()
            banned_users = [user.user.name for user in ban_entries]

            for user in banned_users:
                if user == member:
                    await ctx.guild.unban(user=user, reason=reason)

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='У меня нет прав.'))
            return False

    @commands.command(name='banlist', aliases=['bans'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def banlist(self, ctx):
        """Список заблокированных участников.
        """
        try:
            bans = await ctx.guild.bans()

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

        if len(bans) <= 0:
            return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='Забаненные пользователи отсутствуют.'))

        return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000, description=f'Забаненные пользователи:\n{", ".join([user.user.name for user in bans])}').set_footer(text='banlist'))

    @commands.command(name='kick')
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str=None):
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
        if not reason:
            reason = 'отсутствует.'

        try:
            await member.kick(reason=reason)

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

        else:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0x00ff00, description=f'Пользователь {member} был кикнут.\nПричина: {reason}.').set_footer(text='kick [@пользователь] [причина]'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return True


def setup(bot):
    bot.add_cog(Admin(bot))
    print('[admin.py] Админский модуль загружен.')

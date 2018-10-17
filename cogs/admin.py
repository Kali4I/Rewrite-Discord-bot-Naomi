import discord
import asyncio
from discord.ext import commands
from random import choice
import traceback


class Admin(object):
    """Набор команд для Администрирования."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mute')
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member, *, reason: str=None):
        """Заглушить (выдать мут) пользователя в текстовых чатах.

        Подробности:
        --------------
        <member> - участник.
        [reason] - причина.
        """
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'))

        mute = discord.utils.get(ctx.guild.roles, name='NaomiMute')

        if not reason:
            reason = 'отсутствует'

        try:
            if not mute:
                mute = await ctx.guild.create_role(name='NaomiMute',
                                                   reason='Использована команда n!mute, но роль "NaomiMute" отсутствовала.')

                try:
                    def message_check(m):
                        return m.author.id == ctx.author.id

                    question_msg = await ctx.send(f'''Команда {ctx.prefix}{ctx.command} использована первый раз на этом сервере.
Для корректной работы команды мне нужно внести некоторые правки в текстовые каналы и роли на этом сервере.
```? Какие правки будут внесены?
> Будет создана роль NaomiMute;
> Роль NaomiMute будет добавлена в настройки доступа всех текстовых каналов;
> У всех ролей (кроме @everyone) будет убрано право "send_messages" (отправка сообщений);

Добавление роли в настройки всех каналов нужно, чтобы роль недопускала возможности отправлять сообщения в канал, а удаление права отправки сообщений у других ролей нужно для корректной работы n!mute.```
Могу-ли я внести правки в настройки каналов и ролей для корректной работы этой команды? (Да/Нет)''')
                    msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)

                    if msg.content.lower() in ['да', 'ага', 'угу']:
                        counter_msg = await ctx.send('Хорошо, выполняю... \nМодификация каналов: в ожидании.\nМодификация ролей: в ожидании.')

                        x = 0
                        for tchannel in ctx.guild.text_channels:
                            try:
                                await tchannel.set_permissions(mute,
                                                               read_messages=True,
                                                               send_messages=False,
                                                               add_reactions=False)

                            except discord.errors.Forbidden:
                                pass
                            
                            else:
                                x += 1
                                await counter_msg.edit(content=f'Хорошо, выполняю... \nМодификация каналов: {x}/{len(ctx.guild.text_channels)}\nМодификация ролей: в ожидании.')


                        mute_perms = discord.Permissions()
                        mute_perms.update(send_messages=False)

                        x1 = 0
                        for role in ctx.guild.roles:
                            if role != ctx.guild.default_role:
                                try:
                                    await role.edit(permissions=mute_perms)

                                except discord.errors.Forbidden:
                                    pass
                                
                                else:
                                    x1 += 1
                                    await counter_msg.edit(content=f'Хорошо, выполняю... \nМодификация каналов: Успешно закончено.\nМодификация ролей: {x1}/{len(ctx.guild.roles)}')

                    if msg.content.lower() in ['нет', 'не', 'не-а', 'неа']:
                        await ctx.send('В таком случае, команда может работать некорректно.')

                except asyncio.TimeoutError:
                    await ctx.send('Я не столь терпелива, чтобы ждать ответа так долго...\nПросто повторно введите команду.', delete_after=10)
                    await asyncio.sleep(10)
                    await ctx.message.delete()
                    return False

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
        await question_msg.delete()
        await counter_msg.delete()
        return True

    @commands.command(name='unmute')
    @commands.guild_only()
    async def unmute(self, ctx, member: discord.Member, *, reason: str=None):
        """Снять приглушение с участника.

        Подробности:
        --------------
        <member> - участник.
        [reason] - причина.
        """
        if not ctx.author.permissions_in(ctx.channel).manage_roles:
            return await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'))

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
    async def newname(self, ctx, member: discord.Member, *, nickname: str=None):
        """Сменить никнейм пользователя.

        Подробности:
        --------------
        <member> - участник.
        [nickname] - новый никнейм (ничего для сброса).
        """

        if not ctx.author.permissions_in(ctx.channel).manage_nicknames:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

        try:
            await member.edit(nick=nickname, reason='Запрошено, используя n!newname.')

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

    @commands.command(name='cleanup')
    @commands.guild_only()
    async def cleanup(self, ctx, member: discord.Member, count: int=None):
        """Удалить последние `count` сообщений участника `member`.

        Подробности:
        --------------
        <member> - участник, чьи сообщения удалить.
        [count] - кол-во сообщений, которые будут удалены.
        """

        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

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
    async def purge(self, ctx, count: int):
        """Удалить последние `count` сообщений в чате.

        Подробности:
        --------------
        <count> - кол-во сообщений, которые будут удалены.
        """

        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

        try:
            await ctx.channel.purge(limit=count)

        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xff0000).set_footer(text='У меня нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

    @commands.command(name='ban')
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason: str=None):
        """Заблокировать пользователя на сервере.

        Подробности:
        --------------
        <member> - участник, которого нужно заблокировать.
        [reason] - причина.
        """

        if not ctx.author.permissions_in(ctx.channel).ban_members:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

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
    async def unban(self, ctx, member: discord.Member, *, reason: str=None):
        """Разблокировать пользователя на этом Discord сервере.

        Подробности:
        --------------
        <member> - заблокированный пользователь.
        [reason] - причина.
        """

        if not reason:
            reason = 'отсутствует.'

        if not ctx.author.permissions_in(ctx.channel).ban_members:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

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
    async def banlist(self, ctx):
        """Список заблокированных здесь пользователей.

        Подробности:
        --------------
        Аргументы не требуются.
        """

        if not ctx.author.permissions_in(ctx.channel).ban_members:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

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
    async def kick(self, ctx, member: discord.Member, *, reason: str=None):
        """Выгнать пользователя с сервера.

        Подробности:
        --------------
        <member> - пользователь, которого нужно выгнать.
        [reason] - причина.
        """

        if not ctx.author.permissions_in(ctx.channel).kick_members:
            await ctx.send(embed=discord.Embed(timestamp=ctx.message.created_at, color=0xFF0000).set_footer(text='Нет прав.'), delete_after=20)
            await asyncio.sleep(20)
            await ctx.message.delete()
            return False

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

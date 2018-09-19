import discord
from discord.ext import commands
from random import choice

class Admin(object):

    def __init__(self, bot):
        self.bot = bot






    @commands.command(name='newname', aliases=['new-name', 'change-name', 'changename', 'newnick'])
    async def newname(self, ctx, member:discord.Member, *, nickname:str=None):
        """Сменить Ваш никнейм.

        Подробности:
        --------------
        <member> - участник.
        [nickname] - новый никнейм (ничего для сброса).
        """

        if not ctx.author.permissions_in(ctx.channel).manage_nicknames:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        try:
            await member.edit(nick=nickname, reason='Запрошено пользователем.')
        except discord.errors.Forbidden:
            await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='У меня нет прав.'))






    @commands.command(name='cleanup')
    async def cleanup(self, ctx, member:discord.Member, count:int=None):
        """Удалить последние `count` сообщений участника `member`.

        Подробности:
        --------------
        <member> - участник, чьи сообщения удалить.
        [count] - кол-во сообщений, которые будут удалены.
        """

        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        def is_member(m):
            return m.author == member

        await ctx.channel.purge(limit=count, check=is_member)






    @commands.command(name='purge', aliases=['clean', 'clear', 'clearchat'])
    async def purge(self, ctx, count:int):
        """Удалить последние `count` сообщений в чате.

        Подробности:
        --------------
        <count> - кол-во сообщений, которые будут удалены.
        """

        if not ctx.author.permissions_in(ctx.channel).manage_messages:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        await ctx.channel.purge(limit=count)






    @commands.command(name='ban')
    async def ban(self, ctx, member:discord.Member, *, reason:str=None):
        """Заблокировать пользователя на сервере.

        Подробности:
        --------------
        <member> - участник, которого нужно заблокировать.
        [reason] - причина.
        """

        if not ctx.author.permissions_in(ctx.channel).ban_members:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        if not reason:
            reason = 'отсутствует.'
        try:
            await ctx.guild.ban(user=member, reason=reason)

        except discord.errors.Forbidden:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='У меня нет прав.'))

        else:
            return await ctx.send(embed=discord.Embed(color=0x00ff00, description=f'Пользователь {member} забанен!\nПричина: {reason}.').set_footer(text='ban [@пользователь] [причина]'))






    @commands.command(name='unban', aliases=['pardon'])
    async def unban(self, ctx, member:discord.Member, *, reason:str=None):
        """Разблокировать пользователя на этом Discord сервере.

        Подробности:
        --------------
        <member> - заблокированный пользователь.
        [reason] - причина.
        """

        if not reason:
            reason = 'отсутствует.'

        if not ctx.author.permissions_in(ctx.channel).ban_members:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        try:
            ban_entries = await ctx.guild.bans()
            banned_users = [user.user.name for user in ban_entries]

            for user in banned_users:
                if user == member:
                    await ctx.guild.unban(user=user, *, reason=None)
        except discord.errors.Forbidden:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='У меня нет прав.'))






    @commands.command(name='banlist', aliases=['bans'])
    async def banlist(self, ctx):
        """Список заблокированных здесь пользователей.

        Подробности:
        --------------
        Аргументы не требуются.
        """

        if not ctx.author.permissions_in(ctx.channel).ban_members:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        try:
            bans = await ctx.guild.bans()

        except discord.errors.Forbidden:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='У меня нет прав.'))

        if len(bans) <= 0:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='Забаненные пользователи отсутствуют.'))

        return await ctx.send(embed=discord.Embed(color=0xff0000, description=f'Забаненные пользователи:\n{", ".join([user.user.name for user in bans])}').set_footer(text='banlist'))






    @commands.command(name='kick')
    async def kick(self, ctx, member:discord.Member, *, reason:str=None):
        """Выгнать пользователя с сервера.

        Подробности:
        --------------
        <member> - пользователь, которого нужно выгнать.
        [reason] - причина.
        """

        if not ctx.author.permissions_in(ctx.channel).kick_members:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        if not reason:
            reason = 'отсутствует.'

        try:
            await member.kick(reason=reason)
            
        except discord.errors.Forbidden:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='У меня нет прав.'))

        else:
            return await ctx.send(embed=discord.Embed(color=0x00ff00, description=f'Пользователь {member} был кикнут.\nПричина: {reason}.').set_footer(text='kick [@пользователь] [причина]'))






def setup(bot):
    bot.add_cog(Admin(bot))
    print('[admin.py] Админский модуль загружен.')
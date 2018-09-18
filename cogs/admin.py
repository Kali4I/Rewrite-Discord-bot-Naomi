import discord
from discord.ext import commands
from random import choice

class Admin(object):

    def __init__(self, bot):
        self.bot = bot






    @commands.command(name='cleanup')
    @commands.cooldown(1.4)
    async def cleanup(self, ctx, member:discord.Member, count:int=None):
        """Удалить последние `count` сообщений участника `member`."""

        def is_member(m):
            return m.author == member

        await ctx.channel.purge(limit=count, check=is_member)






    @commands.command(name='purge', aliases=['clean', 'clear', 'clearchat'])
    @commands.cooldown(1.4)
    async def purge(self, ctx, count:int):
        """Удалить последние `count` сообщений в чате."""
        await ctx.channel.purge(limit=count)






    @commands.command(name='ban')
    @commands.cooldown(1.4)
    async def ban(self, ctx, member:discord.Member, reason:str=None):
        """Заблокировать пользователя на сервере."""

        if not ctx.author.permissions_in(ctx.channel).ban_members:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        if not reason:
            reason = 'отсутствует.'
        try:
            await ctx.guild.ban(user=member, reason=reason)

        except discord.errors.Forbidden:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='У меня нет прав.'))

        else:
            return await self.channel.send(embed=discord.Embed(color=0x00ff00, description=f'Пользователь {member} забанен!\nПричина: {reason}.').set_footer(text='ban [@пользователь] [причина]'))






    @commands.command(name='banlist', aliases=['bans'])
    @commands.cooldown(1.4)
    async def banlist(self, ctx):
        """Список заблокированных здесь пользователей."""

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
    @commands.cooldown(1.4)
    async def kick(self, ctx, member:discord.Member, reason:str=None):
        """Выгнать пользователя с сервера."""

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
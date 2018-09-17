import discord
from discord.ext import commands
from random import choice

class Admin(object):

    def __init__(self, bot):
        self.bot = bot






    @commands.command(name='cleanup', description='Очистка чата от сообщений конкретного пользователя.')
    async def _cleanup(self, ctx, member:discord.Member=None, count:int=None):
        if not member or not count:
            return await ctx.send(embed=discord.Embed(color=0xff00ff).set_footer(text='cleanup [@пользователь] [кол-во сообщений]'))

        def is_member(m):
            return m.author == member

        await ctx.channel.purge(limit=count, check=is_member)


    @commands.command(name='purge', description='Очистка чата.', aliases=['clean', 'clear', 'clearchat'])
    async def _cleanup(self, ctx, count:int=None):
        if not count:
            return await ctx.send(embed=discord.Embed(color=0xff00ff).set_footer(text='purge [кол-во сообщений]'))

        await ctx.channel.purge(limit=count)






    @commands.command(name='ban', description='Забанить пользователя.')
    async def _ban(self, ctx, member:discord.Member=None, reason:str=None):
        if not ctx.author.permissions_in(ctx.channel).ban_members:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        if not member:
            return await ctx.send(embed=discord.Embed(color=0xD587F2).set_footer(text='ban [@пользователь] [причина]'))

        if not reason:
            reason = 'отсутствует.'
        try:
            await ctx.guild.ban(user=member, reason=reason)

        except discord.errors.Forbidden:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='У меня нет прав.'))

        else:
            return await self.channel.send(embed=discord.Embed(color=0x00ff00, description=f'Пользователь {member} забанен!\nПричина: {reason}.').set_footer(text='ban [@пользователь] [причина]'))






    @commands.command(name='banlist', description='Банлист сервера.', aliases=['bans'])
    async def _banlist(self, ctx):
        if not ctx.author.permissions_in(ctx.channel).ban_members:
            return await ctx.send(embed=discord.Embed(color=0xFF0000).set_footer(text='Нет прав.'))

        try:
            bans = await ctx.guild.bans()

        except discord.errors.Forbidden:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='У меня нет прав.'))

        if len(bans) <= 0:
            return await ctx.send(embed=discord.Embed(color=0xff0000).set_footer(text='Забаненные пользователи отсутствуют.'))

        return await ctx.send(embed=discord.Embed(color=0xff0000, description=f'Забаненные пользователи:\n{", ".join([user.user.name for user in bans])}').set_footer(text='banlist'))






    @commands.command(name='kick', description='Выгнать пользователя.')
    async def _kick(self, ctx, member:discord.Member=None, reason:str=None):
        if not member:
            return await ctx.send(embed=discord.Embed(color=0xD587F2).set_footer(text='kick [@пользователь] [причина]'))
        
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
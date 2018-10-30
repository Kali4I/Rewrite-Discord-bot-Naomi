# python3.6
# coding: utf-8

from discord.ext import commands
from random import choice
import discord

class OwO(object):
    """<3"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tea')
    async def tea(self, ctx):
        """---"""
        image = 'http://images.vfl.ru/ii/1540901885/ba9f757a/23999576.jpg'
        messages = ['У Вас был тяжелый день? Позвольте мне предложить Вам чай и печеньку! :з',
                    'Рада вас видеть! Вот, выпейте чаю <3',
                    'Чай готов! :з', 'Наслаждайтесь, господин!']
        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.group(name='emote', aliases=['emotes'])
    async def emotes(self, ctx):
        """Эмоции и анимешные картинки <3"""
        if not ctx.invoked_subcommand:
            await ctx.send(f'{ctx.prefix}{ctx.command} -\nlove\nsad\njoy\nangry\nlonely')

    @emotes.command(name='love')
    async def love(self, ctx):
        """---"""
        image = 'http://images.vfl.ru/ii/1540905231/0cf06cf3/24000410.jpg'
        author = ctx.message.author.name
        messages = [f'{author} полон любви и заботы <3']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @emotes.command(name='sad')
    async def sad(self, ctx):
        """---"""
        image = 'http://images.vfl.ru/ii/1540905169/1859d59c/24000401.jpg'
        author = ctx.message.author.name
        messages = [f'{author} чувствует грусть :c',
                    f'Так печально, когда {author} грустит...']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @emotes.command(name='joy')
    async def joy(self, ctx):
        """---"""
        image = 'http://images.vfl.ru/ii/1540905081/27bd14ca/24000379.jpg'
        author = ctx.message.author.name
        messages = [f'Я рада, {author} счастлив!',
                    f'Счастья полон {author}, это так прекрасно! :з',
                    f'{author} счастлив! Меня это радует <3']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @emotes.command(name='angry')
    async def angry(self, ctx):
        """---"""
        image = 'http://images.vfl.ru/ii/1540904890/5fce2341/24000340.jpg'
        author = ctx.message.author.name
        messages = [f'{author} испытывает злость... Не стоит беспокоить его!',
                    f'Мне так грустно видеть, что {author} испытывает злость...',
                    f'{author} зол... Это наполняет меня грустью :c']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @emotes.command(name='lonely')
    async def lonely(self, ctx):
        """---"""
        image = 'http://images.vfl.ru/ii/1540905345/1bab6eb8/24000432.jpg'
        author = ctx.message.author.name
        messages = [f'Мне жаль {author}. Он чувствует одиночество :c',
                    f'Ах, как жаль... Чувство одинокости наполнило {author}...',
                    f'{author} чувствует одиночество...']

        embed = discord.Embed(color=0xFF6AE5,
                              title=choice(messages))
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        embed.set_image(url=image)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(OwO(bot))
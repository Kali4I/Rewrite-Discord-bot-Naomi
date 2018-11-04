# coding: utf-8
## https://github.com/LyricLy/hastebin.py/blob/master/hastebin/async_hastebin.py
import aiohttp

class PostCodeError(Exception):
    pass

async def post(content):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("https://hastebin.com/documents", data=content.encode('utf-8')) as post:
                post = await post.json()
                return "https://hastebin.com/{}".format(post['key'])
        except:
            raise PostCodeError('Что-то пошло не так.')
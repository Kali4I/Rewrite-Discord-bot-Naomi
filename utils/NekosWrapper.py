# python3.6
# coding: utf-8

# Nekos.life images wrapper for discord bot Naomi
# https://github.com/AkiraSumato-01/Rewrite-Discord-Bot-Naomi

import requests
from random import choice


class NekosWrapperError(Exception):
    """Base class for NekosWrapper exceptions."""
    pass


class NekoNotInTags(NekosWrapperError):
    pass


nekos_tags = [
    'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
    'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
    'ngif', 'meow', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
    'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
    'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
    'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
    'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
    'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'Random_hentai_gif',
    'smallboobs', 'hug', 'ero']


def get_neko(tag=None):
    """Get image from nekos.life and return image URL"""

    if not tag:
        tag = choice(nekos_tags)

    if tag not in nekos_tags:
        raise NekoNotInTags('Given tag not in possible "nekos_tags" list.')

    response = requests.get('https://nekos.life/api/v2/img/' + tag)
    return response.json()['url']

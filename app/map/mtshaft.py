from common import *

ID = 43

MS_2F = 4300
MS_1F = 4301

def setup(areas, ow):
    areas[ID] = {
        'name': 'Mountain Shaft',
        'emoji': '<:zub:414542932482326529>',
        'dialog': '',
    }


    # 2F
    async def ms_2f_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(MS_1F)
            return True

    ow[MS_2F] = {
        'name': '2F',
        'desc': '',
        'img': 'https://i.imgur.com/UD4UE5Z.png',
        'ex': ms_2f_ex,
        'actions': ['ladder'],
    }

    # 1F
    async def ms_1f_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(MS_2F)
            return True

    ow[MS_1F] = {
        'name': '1F',
        'desc': '',
        'img': 'https://i.imgur.com/D4HBmZB.png',
        'ex': ms_1f_ex,
        'actions': ['ladder'],
    }
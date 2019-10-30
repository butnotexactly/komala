from common import *

ID = 47

MM_LITWICK_WAXTONE_3F = 4700
MM_AN_EERIE_SENSATION_2F = 4701
MM_WHITEOUT_1F = 4702
MM_SPIRIT_GATHERING_2F = 4703

def setup(areas, ow):
    areas[ID] = {
        'name': 'Monochrome Mines',
        'emoji': '<:abs:414474447244754954>', #<:mabs:414474447387361284>
        'dialog': '',
        # 'map': [[MM_LITWICK_WAXTONE_1F, MM_AN_EERIE_SENSATION_2F],
        #     [MM_WHITEOUT_1F, MM_SPIRIT_GATHERING_2F]]
    }


    # Litwick Waxtone 3F
    async def mm_litwick_waxtone_3f_ex(handler, arg):
        if arg == 'ladder':
            await handler.move_to(MM_AN_EERIE_SENSATION_2F)
            return True

    ow[MM_LITWICK_WAXTONE_3F] = {
        'name': '3F Litwick Waxtone',
        'desc': '',
        'img': 'https://i.imgur.com/ZRniMtc.png',
        'ex': mm_litwick_waxtone_3f_ex,
        'actions': ['ladder'],
    }

    # An eerie sensation... 2F
    async def mm_an_eerie_sensation_2f_ex(handler, arg):
        if arg == 'ladder':
            await handler.move_to(MM_LITWICK_WAXTONE_3F)
            return True

    ow[MM_AN_EERIE_SENSATION_2F] = {
        'name': '2F An eerie sensation...',
        'desc': '',
        'img': 'https://i.imgur.com/FDu2f5G.png',
        'ex': mm_an_eerie_sensation_2f_ex,
        'paths': [None, None, MM_SPIRIT_GATHERING_2F, None],
        'actions': ['ladder'],
    }

    # Whiteout 1F
    async def mm_whiteout_1f_ex(handler, arg):
        if arg == 'ladder':
            await handler.move_to(MM_SPIRIT_GATHERING_2F)
            return True

    ow[MM_WHITEOUT_1F] = {
        'name': '1F Whiteout',
        'desc': '',
        'img': 'https://i.imgur.com/5URTKBT.png',
        'ex': mm_whiteout_1f_ex,
        'actions': ['ladder'],
    }

    # Spirit Gathering 2F
    async def mm_spirit_gathering_2f_ex(handler, arg):
        if arg == 'ladder':
            await handler.move_to(MM_WHITEOUT_1F)
            return True

        if 'arch' in arg:
            # You feel a strange energy eminating from it. It physically repels you.
            pass

    ow[MM_SPIRIT_GATHERING_2F] = {
        'name': '2F Spirit Gathering',
        'desc': '',
        'img': 'https://i.imgur.com/0nIUYJ6.png',
        'ex': mm_spirit_gathering_2f_ex,
        'paths': [MM_AN_EERIE_SENSATION_2F, None, None, None],
        'actions': ['ladder', 'archway'],
    }
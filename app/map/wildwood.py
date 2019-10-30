from common import *

ID = 60

WWP_WILDERNESS = 6000
WWP_FEAROW_CAMP = 6001
WWP_MOUNTAINSIDE = 6002

def setup(areas, ow):
    areas[ID] = {
        'name': 'Wildwood Pass',
        'emoji': '<:urs:414540757458878465>',
        'dialog': '',
        'map': [[None, WWP_WILDERNESS],
            [WWP_FEAROW_CAMP, WWP_MOUNTAINSIDE]]
    }


    # Wilderness
    async def wwp_wilderness_ex(handler, arg):
        if arg == 'tunnel':
            await handler.move_to(WWP_MOUNTAINSIDE)
            return True

    ow[WWP_WILDERNESS] = {
        'name': 'Wilderness',
        'desc': '',
        'img': 'https://i.imgur.com/uBF3svM.png',
        'ex': wwp_wilderness_ex,
        'blocked': [S],
        'actions': ['tunnel'],
    }

    # Fearow Camp
    async def wwp_fearow_camp_ex(handler, arg):
        pass

    ow[WWP_FEAROW_CAMP] = {
        'name': 'Fearow Camp',
        'desc': '',
        'img': 'https://i.imgur.com/Nuv3CPp.png',
        'ex': wwp_fearow_camp_ex,
        #'actions': [''],
    }

    # Mountainside
    async def wwp_mountainside_ex(handler, arg):
        if arg == 'tunnel':
            await handler.move_to(WWP_WILDERNESS)
            return True

    ow[WWP_MOUNTAINSIDE] = {
        'name': 'Mountainside',
        'desc': '',
        'img': 'https://i.imgur.com/qmYvYmS.png',
        'ex': wwp_mountainside_ex,
        'blocked': [N],
        'actions': ['tunnel'],
    }
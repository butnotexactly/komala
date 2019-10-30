from common import *

ID = 2

PIKI_NORTH = 200
PIKI_SOUTH = 201

def setup(areas, ow):
    areas[ID] = {
        'name': 'Pikipek Path',
        'emoji': '<:piki:414522871235346445>',#'🐦 ',
        'dialog': '',
        'map': [[PIKI_NORTH],
                [PIKI_SOUTH]],
        'wilds': [['Rattata', 3, 6, 20],
                  ['Alolan Rattata', 4, 8, 20],
                  ['Fletchling', 3, 6, 20],
                  ['Chatot', 10, 10, 5, RARE],
                  ['Pikipek', 3, 6, 20],
                  ['Minccino', 3, 9, 15, UNCOMMON]]
    }



    # North
    async def piki_north_ex(handler, arg):
        pass

    ow[PIKI_NORTH] = {
        'name': 'North',
        'desc': '',
        'img': 'https://i.imgur.com/XtahuoV.png',
        'ex': piki_north_ex,
        'trainers': ['vincent', 'quinn'],
    }

    # South
    async def piki_south_ex(handler, arg):
        pass

    ow[PIKI_SOUTH] = {
        'name': 'South',
        'desc': '',
        'img': 'https://i.imgur.com/3hZeLhX.png',
        'ex': piki_south_ex,
        'actions': ['sign'],
        'trainers': ['rocket', 'joey', 'emma']
    }
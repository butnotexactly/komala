from common import *
from . import clocktower

ID = 45

SC_MINE_ENTRANCE = 4500
SC_VALLEY = 4501
SC_RUSTIC_HOMES = 4502
SC_WHITEGRASS = 4503

def setup(areas, ow):
    areas[ID] = {
        'name': 'Sepia City',
        'emoji': '<:dusk2:414510136384684035>',
        'dialog': '',
        'map': [[SC_MINE_ENTRANCE, SC_VALLEY],
            [SC_RUSTIC_HOMES, SC_WHITEGRASS]]
    }


    # Mine Entrance
    async def sc_mine_entrance_ex(handler, arg):
        if arg == 'gym':
            await handler.move_to(clocktower.SCG_FIRST_FLOOR)
            return True

    ow[SC_MINE_ENTRANCE] = {
        'name': 'Mine Entrance',
        'desc': '',
        'img': 'https://i.imgur.com/6PkBIUh.png',
        'ex': sc_mine_entrance_ex,
        'actions': ['gym'],
    }

    # Valley
    async def sc_valley_ex(handler, arg):
        pass

    ow[SC_VALLEY] = {
        'name': 'Ghost Valley',
        'desc': '',
        'img': 'https://i.imgur.com/pt0UlDI.png',
        'ex': sc_valley_ex,
        'blocked': [S],
        #'actions': [''],
    }

    # Rustic Homes
    async def sc_rustic_homes_ex(handler, arg):
        pass

    ow[SC_RUSTIC_HOMES] = {
        'name': 'Rustic Homes',
        'desc': '',
        'img': 'https://i.imgur.com/i0gIoCd.png',
        'ex': sc_rustic_homes_ex,
        #'actions': [''],
    }

    # Whitegrass
    async def sc_whitegrass_ex(handler, arg):
        pass

    ow[SC_WHITEGRASS] = {
        'name': 'Whitegrass',
        'desc': '',
        'img': 'https://i.imgur.com/E85TZgr.png',
        'ex': sc_whitegrass_ex,
        #'actions': [''],
    }
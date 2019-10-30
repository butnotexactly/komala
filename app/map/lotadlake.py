from common import *

ID = 4
PREFIX = 'LL'

LL_WARDENS_HOME = 400
LL_GREENHOUSE = 401
LL_HILLTOP = 402
LL_ANGLERS_POINT = 403
LL_GARDEN_MAZE = 404
LL_ASCENT = 405
LL_BIDOOF_BRIDGE = 406
LL_LAKE_CENTER = 407
LL_ENTRANCE_EAST = 408
LL_TRANQUIL_CORNER = 409
LL_ENTRANCE_SOUTH = 410
LL_POLIWAG_NEST = 411

def setup(areas, ow):
    areas[ID] = {
        'name': 'Lotad Lake',
        'emoji': '<:lud:414510862989131776>', #<:lom:414510862674559003>
        'dialog': '',
        'map': [[LL_WARDENS_HOME, LL_GREENHOUSE, LL_HILLTOP],
                [LL_ANGLERS_POINT, LL_GARDEN_MAZE, LL_ASCENT],
                [LL_BIDOOF_BRIDGE, LL_LAKE_CENTER, LL_ENTRANCE_EAST],
                [LL_TRANQUIL_CORNER, LL_ENTRANCE_SOUTH, LL_POLIWAG_NEST]],

        'wilds': [['Bidoof', 8, 12, 25],
                  ['Lotad (Water)', 4, 8, 25],
                  ['Lotad (Nature)', 4, 8, 25],
                  ['Dewpider', 10, 10, 25]]
    }


    # Warden's Home
    async def ll_wardens_home_ex(handler, arg):
        pass

    ow[LL_WARDENS_HOME] = {
        'name': 'Warden\'s Home',
        'desc': '',
        'img': 'https://i.imgur.com/KSzEjq3.png',
        'ex': ll_wardens_home_ex,
        'wilds': None,
        #'actions': [''],
    }

    # Greenhouse
    async def ll_greenhouse_ex(handler, arg):
        pass

    ow[LL_GREENHOUSE] = {
        'name': 'Greenhouse',
        'desc': '',
        'img': 'https://i.imgur.com/2TF6hm5.png',
        'ex': ll_greenhouse_ex,
        'blocked': [E],
        'wilds': None,
        #'actions': [''],
    }

    # Hilltop
    async def ll_hilltop_ex(handler, arg):
        pass

    ow[LL_HILLTOP] = {
        'name': 'Hilltop',
        'desc': '',
        'img': 'https://i.imgur.com/XcAEkao.png',
        'ex': ll_hilltop_ex,
        'blocked': [W],
        #'actions': [''],
        'wilds': [['Bidoof', 8, 12, 50],
                  ['Seedot (Nature)', 7, 12, 25, UNCOMMON],
                  ['Seedot (Dark)', 7, 12, 25, UNCOMMON]]
    }

    # Angler's Point
    async def ll_anglers_point_ex(handler, arg):
        #todo fish
        pass

    ow[LL_ANGLERS_POINT] = {
        'name': 'Angler\'s Point',
        'desc': '',
        'img': 'https://i.imgur.com/WniTRCC.png',
        'ex': ll_anglers_point_ex,
        'actions': ['fish'],
    }

    # Garden Maze
    async def ll_garden_maze_ex(handler, arg):
        pass

    ow[LL_GARDEN_MAZE] = {
        'name': 'Garden Maze',
        'desc': '',
        'img': 'https://i.imgur.com/p9iyf24.png',
        'ex': ll_garden_maze_ex,
        #'actions': [''],
    }

    # Ascent
    async def ll_ascent_ex(handler, arg):
        pass

    ow[LL_ASCENT] = {
        'name': 'Ascent',
        'desc': '',
        'img': 'https://i.imgur.com/xtZCNY3.png',
        'ex': ll_ascent_ex,
        #'actions': [''],
    }

    # Bidoof Bridge
    async def ll_bidoof_bridge_ex(handler, arg):
        pass

    ow[LL_BIDOOF_BRIDGE] = {
        'name': 'Bidoof Bridge',
        'desc': '',
        'img': 'https://i.imgur.com/YGChhO4.png',
        'ex': ll_bidoof_bridge_ex,
        #'actions': [''],
        'wilds': [['Bidoof', 8, 12, 30],
                  ['Lotad (Water)', 4, 8, 20],
                  ['Lotad (Nature)', 4, 8, 20],
                  ['Dewpider', 10, 10, 20],
                  ['Lombre (Water)', 16, 21, 5, RARE],
                  ['Lombre (Nature)', 16, 21, 5, RARE]]
    }

    # Lake Center
    async def ll_lake_center_ex(handler, arg):
        pass

    ow[LL_LAKE_CENTER] = {
        'name': 'Lake Center',
        'desc': '',
        'img': 'https://i.imgur.com/HyDedxH.png',
        'ex': ll_lake_center_ex,
        #'actions': [''],
        'wilds': [['Bidoof', 8, 12, 22.5],
                  ['Lotad (Water)', 4, 8, 22.5],
                  ['Lotad (Nature)', 4, 8, 22.5],
                  ['Dewpider', 10, 10, 22.5],
                  ['Lombre (Water)', 16, 21, 5, RARE],
                  ['Lombre (Nature)', 16, 21, 5, RARE]]
    }

    # Entrance (East)
    async def ll_entrance_east_ex(handler, arg):
        pass

    ow[LL_ENTRANCE_EAST] = {
        'name': 'Entrance (East)',
        'desc': '',
        'img': 'https://i.imgur.com/aJZUzVF.png',
        'ex': ll_entrance_east_ex,
        #'actions': [''],
        'wilds': [['Bidoof', 8, 12, 22.5],
                  ['Lotad (Water)', 4, 8, 22.5],
                  ['Lotad (Nature)', 4, 8, 22.5],
                  ['Dewpider', 10, 10, 22.5],
                  ['Lombre (Water)', 16, 21, 5, RARE],
                  ['Lombre (Nature)', 16, 21, 5, RARE]]
    }

    # Tranquil Corner
    async def ll_tranquil_corner_ex(handler, arg):
        pass

    ow[LL_TRANQUIL_CORNER] = {
        'name': 'Tranquil Corner',
        'desc': '',
        'img': 'https://i.imgur.com/SK7fxgI.png',
        'ex': ll_tranquil_corner_ex,
        #'actions': [''],
        'wilds': [['Azurill', 5, 5, 100, UNCOMMON]]
    }

    # Entrance (South)
    async def ll_entrance_south_ex(handler, arg):
        pass

    ow[LL_ENTRANCE_SOUTH] = {
        'name': 'Entrance (South)',
        'desc': '',
        'img': 'https://i.imgur.com/1KN0uxR.png',
        'ex': ll_entrance_south_ex,
        'blocked': [E],
        #'actions': [''],
        'wilds': [['Bidoof', 8, 12, 22.5],
                  ['Lotad (Water)', 4, 8, 22.5],
                  ['Lotad (Nature)', 4, 8, 22.5],
                  ['Dewpider', 10, 10, 22.5],
                  ['Lombre (Water)', 16, 21, 5, RARE],
                  ['Lombre (Nature)', 16, 21, 5, RARE]]
    }

    # Poliwag Nest
    async def ll_poliwag_nest_ex(handler, arg):
        pass

    ow[LL_POLIWAG_NEST] = {
        'name': 'Poliwag Nest',
        'desc': '',
        'img': 'https://i.imgur.com/MJZatvn.png',
        'ex': ll_poliwag_nest_ex,
        'blocked': [W],
        'wilds': [['Poliwag', 15, 15, 10, UNCOMMON],
                  ['Bidoof', 8, 12, 22.5],
                  ['Lotad (Water)', 4, 8, 22.5],
                  ['Lotad (Nature)', 4, 8, 22.5],
                  ['Dewpider', 10, 10, 22.5]]

        #'actions': [''],
    }
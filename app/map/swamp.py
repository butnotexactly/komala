from common import *

ID = 8
PREFIX = 'MS'

MS_CITY_EXIT = 800
MS_TOXIC_POOLS = 801
MS_FOREST_HOLLOWS = 802
MS_MARSHLAND = 803
MS_BOARDWALK_BOG = 804
MS_OFF_THE_BEATEN_PATH = 805

def setup(areas, ow):
    areas[ID] = {
        'name': 'Marshstomp Swamp',
        'emoji': '<:marg:414515644227125269>',
        'dialog': '',
        'map': [[MS_CITY_EXIT, MS_TOXIC_POOLS, MS_FOREST_HOLLOWS],
            [MS_MARSHLAND, MS_BOARDWALK_BOG, MS_OFF_THE_BEATEN_PATH]]
    }


    # City Exit
    async def ms_city_exit_ex(handler, arg):
        pass

    ow[MS_CITY_EXIT] = {
        'name': 'City Entrance',
        'desc': '',
        'img': 'https://i.imgur.com/PkdoZ1l.png',
        'ex': ms_city_exit_ex,
        #'actions': [''],
    }

    # Toxic Pools
    async def ms_toxic_pools_ex(handler, arg):
        pass

    ow[MS_TOXIC_POOLS] = {
        'name': 'Toxic Pools',
        'desc': '',
        'img': 'https://i.imgur.com/6Kvzpg4.png',
        'ex': ms_toxic_pools_ex,
        #'actions': [''],
    }

    # Forest Hollows
    async def ms_forest_hollows_ex(handler, arg):
        pass

    ow[MS_FOREST_HOLLOWS] = {
        'name': 'Forest Hollows',
        'desc': '',
        'img': 'https://i.imgur.com/N6Di19C.png',
        'ex': ms_forest_hollows_ex,
        #'actions': [''],
    }

    # Marshland
    async def ms_marshland_ex(handler, arg):
        pass

    ow[MS_MARSHLAND] = {
        'name': 'Marshland',
        'desc': '',
        'img': 'https://i.imgur.com/9DqeNhk.png',
        'ex': ms_marshland_ex,
        #'actions': [''],
    }

    # Boardwalk Bog
    async def ms_boardwalk_bog_ex(handler, arg):
        pass

    ow[MS_BOARDWALK_BOG] = {
        'name': 'Boardwalk Bog',
        'desc': '',
        'img': 'https://i.imgur.com/vxQHRMN.png',
        'ex': ms_boardwalk_bog_ex,
        #'actions': [''],
    }

    # Off the beaten path...
    async def ms_off_the_beaten_path_ex(handler, arg):
        pass

    ow[MS_OFF_THE_BEATEN_PATH] = {
        'name': 'Off the beaten path...',
        'desc': '',
        'img': 'https://i.imgur.com/oNUOnSv.png',
        'ex': ms_off_the_beaten_path_ex,
        'hidden': [E],
        #'actions': [''],
    }
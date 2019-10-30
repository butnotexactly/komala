from common import *

ID = 17

MM_DOWNTOWN = 1700
MM_MT_CINDER_ENTRANCE = 1701
MM_POKEMON_GYM = 1702
MM_CITY_OF_DRAGONS = 1703
MM_MOUNTAIN_GRASSLAND = 1704
MM_CRAG_FOREST = 1705

def setup(areas, ow):
    areas[ID] = {
        'name': 'Montmartre',
        'emoji': '<:sal:414524337878728704> ',
        'dialog': '',
        'map': [[MM_DOWNTOWN, MM_MT_CINDER_ENTRANCE],
                [MM_POKEMON_GYM, MM_CITY_OF_DRAGONS],
                [MM_MOUNTAIN_GRASSLAND, MM_CRAG_FOREST]]
    }


    # Downtown
    async def mm_downtown_ex(handler, arg):
        pass

    ow[MM_DOWNTOWN] = {
        'name': 'Downtown',
        'desc': '',
        'img': 'https://i.imgur.com/e80SyyD.png',
        'ex': mm_downtown_ex,
        'blocked': [S],
        #'actions': [''],
    }

    # Mt. Cinder Entrance
    async def mm_mt_cinder_entrance_ex(handler, arg):
        pass

    ow[MM_MT_CINDER_ENTRANCE] = {
        'name': 'Mt. Cinder Entrance',
        'desc': '',
        'img': 'https://i.imgur.com/LkZZtgG.png',
        'ex': mm_mt_cinder_entrance_ex,
        #'actions': [''],
    }

    # Pokémon Gym
    async def mm_pokemon_gym_ex(handler, arg):
        pass

    ow[MM_POKEMON_GYM] = {
        'name': 'Pokémon Gym',
        'desc': '',
        'img': 'https://i.imgur.com/662Aznz.png',
        'ex': mm_pokemon_gym_ex,
        'blocked': [N, E],
        #'actions': [''],
    }

    # City of Dragons
    async def mm_city_of_dragons_ex(handler, arg):
        pass

    ow[MM_CITY_OF_DRAGONS] = {
        'name': 'City of Dragons',
        'desc': '',
        'img': 'https://i.imgur.com/jL2jKBC.png',
        'ex': mm_city_of_dragons_ex,
        'blocked': [W],
        #'actions': [''],
    }

    # Mountain Grassland
    async def mm_mountain_grassland_ex(handler, arg):
        pass

    ow[MM_MOUNTAIN_GRASSLAND] = {
        'name': 'Mountain Grassland',
        'desc': '',
        'img': 'https://i.imgur.com/2TKZPTG.png',
        'ex': mm_mountain_grassland_ex,
        #'actions': [''],
    }

    # Crag Forest
    async def mm_crag_forest_ex(handler, arg):
        pass

    ow[MM_CRAG_FOREST] = {
        'name': 'Crag Forest',
        'desc': '',
        'img': 'https://i.imgur.com/B9FihFR.png',
        'ex': mm_crag_forest_ex,
        #'actions': [''],
    }
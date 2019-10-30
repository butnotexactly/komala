from common import *

ID = 5
PREFIX = 'SS'

SS_TROPICS = 500
SS_PALM_TREES = 501
SS_COCONUT_CABANAS = 502
SS_BEACH_WALKWAY = 503
SS_SANDSHREW_SANDS = 504
SS_HAMMOCKS = 505
SS_SANDCASTLE_SPOT = 506
SS_COASTLINE = 507
SS_DUNES = 508
SS_ISLES = 509
SS_DEEP_SEA = 510
SS_ROCKY_WATERS = 511

def setup(areas, ow):
    areas[ID] = {
        'name': 'Sleepy Shore',
        'emoji': '<:sno:414529924649451522>',
        'dialog': '',
        'map': [[SS_TROPICS, SS_PALM_TREES, SS_COCONUT_CABANAS],
            [SS_BEACH_WALKWAY, SS_SANDSHREW_SANDS, SS_HAMMOCKS],
            [SS_SANDCASTLE_SPOT, SS_COASTLINE, SS_DUNES],
            [SS_ISLES, SS_DEEP_SEA, SS_ROCKY_WATERS]]
    }


    treePkmn =  [['Starly', 12, 16, 1/3],
                 ['Burmy (Sandy)', 18, 18, 1/3],
                 ['Oddish', 12, 16, 1/3]]

    sleepyPkmn = [['Komala', 23, 27, 10, RARE],
                  ['Munchlax', 18, 22, 15, UNCOMMON],
                  ['Starly', 12, 16, 75/2, COMMON],
                  ['Burmy (Sandy)', 18, 18, 75/2, COMMON]]

    sandyPkmn = [['Sandshrew', 23, 27, 20],
                 ['Wingull', 18, 22, 35, COMMON],
                 ['Pelipper', 12, 16, 10, RARE],
                 ['Burmy (Sandy)', 18, 18, 35, COMMON]]

    waterPkmn = [['Buizel', 23, 27, 10, RARE],
                 ['Wingull', 18, 22, 30],
                 ['Pelipper', 12, 16, 10, RARE],
                 ['Magikarp', 18, 18, 50, COMMON]]

    # Tropics
    async def ss_tropics_ex(handler, arg):
        pass

    ow[SS_TROPICS] = {
        'name': 'Tropics',
        'desc': '',
        'img': 'https://i.imgur.com/ZbcB13F.png',
        'ex': ss_tropics_ex,
        #'actions': [''],
        'wilds': treePkmn
    }

    # Palm Trees
    async def ss_palm_trees_ex(handler, arg):
        pass

    ow[SS_PALM_TREES] = {
        'name': 'Palm Trees',
        'desc': '',
        'img': 'https://i.imgur.com/OSHdnNs.png',
        'ex': ss_palm_trees_ex,
        #'actions': [''],
        'wilds': sleepyPkmn
    }

    # Coconut Cabanas
    async def ss_coconut_cabanas_ex(handler, arg):
        pass

    ow[SS_COCONUT_CABANAS] = {
        'name': 'Coconut Cabanas',
        'desc': '',
        'img': 'https://i.imgur.com/7DrLjYc.png',
        'ex': ss_coconut_cabanas_ex,
        #'actions': [''],
        'wilds': sleepyPkmn
    }

    # Beach Walkway
    async def ss_beach_walkway_ex(handler, arg):
        pass

    ow[SS_BEACH_WALKWAY] = {
        'name': 'Beach Walkway',
        'desc': '',
        'img': 'https://i.imgur.com/oFy14Y2.png',
        'ex': ss_beach_walkway_ex,
        'blocked': [E],
        #'actions': [''],
        'wilds': treePkmn
    }

    # Sandshrew Sands
    async def ss_sandshrew_sands_ex(handler, arg):
        pass

    ow[SS_SANDSHREW_SANDS] = {
        'name': 'Sandshrew Sands',
        'desc': '',
        'img': 'https://i.imgur.com/yKezNYU.png',
        'ex': ss_sandshrew_sands_ex,
        'blocked': [W],
        #'actions': [''],
        'wilds': sandyPkmn
    }

    # Hammocks
    async def ss_hammocks_ex(handler, arg):
        pass

    ow[SS_HAMMOCKS] = {
        'name': 'Hammocks',
        'desc': '',
        'img': 'https://i.imgur.com/ZoF6xE7.png',
        'ex': ss_hammocks_ex,
        #'actions': [''],
        'wilds': sleepyPkmn
    }

    # Sandcastle Spot
    async def ss_sandcastle_spot_ex(handler, arg):
        pass

    ow[SS_SANDCASTLE_SPOT] = {
        'name': 'Sandcastle Spot',
        'desc': '',
        'img': 'https://i.imgur.com/9R2KIS1.png',
        'ex': ss_sandcastle_spot_ex,
        #'actions': [''],
        'wilds': sandyPkmn
    }

    # Coastline
    async def ss_coastline_ex(handler, arg):
        pass

    ow[SS_COASTLINE] = {
        'name': 'Coastline',
        'desc': '',
        'img': 'https://i.imgur.com/L76xJen.png',
        'ex': ss_coastline_ex,
        #'actions': [''],
        'wilds': sandyPkmn
    }

    # Dunes
    async def ss_dunes_ex(handler, arg):
        pass

    ow[SS_DUNES] = {
        'name': 'Dunes',
        'desc': '',
        'img': 'https://i.imgur.com/YARgbgU.png',
        'ex': ss_dunes_ex,
        #'actions': [''],
        'wilds': sandyPkmn
    }

    # Isles
    async def ss_isles_ex(handler, arg):
        pass

    ow[SS_ISLES] = {
        'name': 'Isles',
        'desc': '',
        'img': 'https://i.imgur.com/OXpvQcK.png',
        'ex': ss_isles_ex,
        #'actions': [''],
        'wilds': waterPkmn
    }

    # Deep Sea
    async def ss_deep_sea_ex(handler, arg):
        pass

    ow[SS_DEEP_SEA] = {
        'name': 'Deep Sea',
        'desc': '',
        'img': 'https://i.imgur.com/pFmAthF.png',
        'ex': ss_deep_sea_ex,
        #'actions': [''],
        'wilds': waterPkmn
    }

    # Rocky Waters
    async def ss_rocky_waters_ex(handler, arg):
        pass

    ow[SS_ROCKY_WATERS] = {
        'name': 'Rocky Waters',
        'desc': '',
        'img': 'https://i.imgur.com/nvp6PhE.png',
        'ex': ss_rocky_waters_ex,
        #'actions': [''],
        'wilds': waterPkmn
    }
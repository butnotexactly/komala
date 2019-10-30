from common import *
from . import iceshaft

ID = 42

SC_COZY_CORNER = 4200
SC_NORTHPOINT = 4201
SC_FROSTY_FOREST = 4202
SC_THE_HIGHEST_GYM = 4203
SC_SNOVER_TREES = 4204
SC_SNOWY_PASS = 4205
SC_SNOW_VALLEY = 4206

def setup(areas, ow):
    areas[ID] = {
        'name': 'Shiver City',
        'emoji': '<:snor:414529924486135809>',
        'dialog': '',
        'map': [[None, SC_COZY_CORNER, SC_NORTHPOINT],
                [SC_FROSTY_FOREST, SC_THE_HIGHEST_GYM, SC_SNOVER_TREES],
                [SC_SNOWY_PASS, SC_SNOW_VALLEY]]
    }


    # Cozy Corner
    async def sc_cozy_corner_ex(handler, arg):
        pass

    ow[SC_COZY_CORNER] = {
        'name': 'Cozy Corner',
        'desc': '',
        'img': 'https://i.imgur.com/PQOxD1N.png',
        'ex': sc_cozy_corner_ex,
        #'actions': [''],
    }

    # Northpoint
    async def sc_northpoint_ex(handler, arg):
        pass

    ow[SC_NORTHPOINT] = {
        'name': 'Northpoint',
        'desc': '',
        'img': 'https://i.imgur.com/AXJYz13.png',
        'ex': sc_northpoint_ex,
        #'actions': [''],
    }

    # Frosty Forest
    async def sc_frosty_forest_ex(handler, arg):
        pass

    ow[SC_FROSTY_FOREST] = {
        'name': 'Frosty Forest',
        'desc': '',
        'img': 'https://i.imgur.com/F1PLVbq.png',
        'ex': sc_frosty_forest_ex,
        #'actions': [''],
    }

    # The Highest Gym
    async def sc_the_highest_gym_ex(handler, arg):
        pass

    ow[SC_THE_HIGHEST_GYM] = {
        'name': 'The Highest Gym',
        'desc': '',
        'img': 'https://i.imgur.com/gsNtmT3.png',
        'ex': sc_the_highest_gym_ex,
        'blocked': [S],
        #'actions': [''],
    }

    # Snover Trees
    async def sc_snover_trees_ex(handler, arg):
        pass

    ow[SC_SNOVER_TREES] = {
        'name': 'Snover Trees',
        'desc': '',
        'img': 'https://i.imgur.com/RCe6rrm.png',
        'ex': sc_snover_trees_ex,
        #'actions': [''],
    }

    # Snowy Pass
    async def sc_snowy_pass_ex(handler, arg):
        if 'cave' in arg:
            await handler.move_to(iceshaft.IS_TITANS_DOMAIN)
            return True

    ow[SC_SNOWY_PASS] = {
        'name': 'Snowy Pass',
        'desc': '',
        'img': 'https://i.imgur.com/rmGI0JF.png',
        'ex': sc_snowy_pass_ex,
        'actions': ['cave'],
    }

    # Snow Valley
    async def sc_snow_valley_ex(handler, arg):
        pass

    ow[SC_SNOW_VALLEY] = {
        'name': 'Snow Valley',
        'desc': '',
        'img': 'https://i.imgur.com/qI7mSlC.png',
        'ex': sc_snow_valley_ex,
        #'blocked': [N],
        #'actions': [''],
    }
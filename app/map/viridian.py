import random

from common import *

ID = 3
PREFIX = 'VIR'

VIR_CROSSING = 300
VIR_DOWNTOWN = 301
VIR_POND = 302
VIR_POKÉMON_CENTER = 303

def setup(areas, ow):
    areas[ID] = {
        'name': 'Viridian City',
        'emoji': '<:nid1:414516409121505280> ',
        'dialog': '',
        'map': [[VIR_CROSSING, VIR_DOWNTOWN],
                [VIR_POND, VIR_POKÉMON_CENTER]]
    }

    # Crossing
    async def vir_crossing_ex(handler, arg):
        pass

    ow[VIR_CROSSING] = {
        'name': 'Crossing',
        'desc': '',
        'img': 'https://i.imgur.com/NoRh19C.png',
        'ex': vir_crossing_ex,
        #'actions': [''],
    }

    # Downtown
    async def vir_downtown_ex(handler, arg):
        pass

    ow[VIR_DOWNTOWN] = {
        'name': 'Downtown',
        'desc': '',
        'img': 'https://i.imgur.com/FbCCGUo.png',
        'ex': vir_downtown_ex,
        #'actions': [''],
    }

    # Pond
    async def vir_pond_ex(handler, arg):
        if 'fish' in arg:
            await handler.bot.explore.engage(handler.ctx, handler.state.location, 'Magikarp', random.randint(3, 6))
            return

    ow[VIR_POND] = {
        'name': 'Pond',
        'desc': '',
        'img': 'https://i.imgur.com/CtNbZGi.png',
        'ex': vir_pond_ex,
        'actions': ['fish'],
    }

    # Pokémon Center
    async def vir_pokémon_center_ex(handler, arg):
        pass

    ow[VIR_POKÉMON_CENTER] = {
        'name': 'Pokémon Center',
        'desc': '',
        'img': 'https://i.imgur.com/c6HZFZz.png',
        'ex': vir_pokémon_center_ex,
        #'actions': [''],
    }
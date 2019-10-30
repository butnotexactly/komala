from common import *
from . import skycity

ID = 6
PREFIX = 'FP'

FP_FLOWER_FOREST = 600
FP_FAIRY_BRIDGE = 601
FP_WATERSIDE_CLIFFS = 602
FP_AIR_LIFT = 603

def setup(areas, ow):
    areas[ID] = {
        'name': 'Fairy Pass',
        'emoji': '<:togt:414534719955402762>',
        'dialog': '',
        #'color': 0xFFAFAF,
        'map': [[FP_FLOWER_FOREST, FP_FAIRY_BRIDGE],
            [FP_WATERSIDE_CLIFFS, FP_AIR_LIFT]]
    }


    # Flower Forest
    async def fp_flower_forest_ex(handler, arg):
        pass

    ow[FP_FLOWER_FOREST] = {
        'name': 'Flower Forest',
        'desc': '',
        'img': 'https://i.imgur.com/cb7HEjw.png',
        'ex': fp_flower_forest_ex,
        #'actions': [''],
    }

    # Fairy Bridge
    async def fp_fairy_bridge_ex(handler, arg):
        pass

    ow[FP_FAIRY_BRIDGE] = {
        'name': 'Fairy Bridge',
        'desc': '',
        'img': 'https://i.imgur.com/fWApPeC.png',
        'ex': fp_fairy_bridge_ex,
        #'actions': [''],
    }

    # Waterside Cliffs
    async def fp_waterside_cliffs_ex(handler, arg):
        pass

    ow[FP_WATERSIDE_CLIFFS] = {
        'name': 'Waterside Cliffs',
        'desc': '',
        'img': 'https://i.imgur.com/o4VINEz.png',
        'ex': fp_waterside_cliffs_ex,
        #'actions': [''],
    }

    # Air Lift
    async def fp_air_lift_ex(handler, arg):

        if 'ho oh' in arg:
            dex = handler.dex_entry('Charizard')
            await handler.show_dialog('The Legendary Rainbow Pokémon', f'Ho-oh lowers its wings and bows. Accept its generous offer of flight?{DBL_BREAK}※  `yes` or `no`', color=TYPE_COLORS[dex['type']], image=dex['gif'], thumb=True)
            return True

        if arg == 'no':
            await handler.show_location()
            return True

        if arg == 'yes':
            await handler.move_to(skycity.SC_LANDING)
            return True

    ow[FP_AIR_LIFT] = {
        'name': 'Air Lift',
        'desc': '',
        'img': 'https://i.imgur.com/E3qYGok.png',
        'ex': fp_air_lift_ex,
        'actions': ['ho oh'],
    }
from common import *
from . import swamp

ID = 7
PREFIX = 'TT'

TT_TRAILS_END = 700
TT_NEW_TRAINER_ALLEY = 701
TT_SWAMP_EDGE = 702
TT_TRAIL_FORK = 703

def setup(areas, ow):
    areas[ID] = {
        'name': 'Turtwig Thicket',
        'emoji': '<:turt:414534719854870529>',
        'dialog': '',
        'map': [[TT_TRAILS_END],
            [TT_NEW_TRAINER_ALLEY],
            [TT_SWAMP_EDGE],
            [TT_TRAIL_FORK]],
        'wilds': [['Burmy (Plant)', 18, 18, 17.5],
              ['Combee', 8, 11, 17.5],
              ['Scatterbug', 8, 11, 17.5],
              ['Morelull', 14, 16, 25, COMMON],
              ['Shiinotic', 23, 27, 5, RARE],
              ['Oddish', 12, 16, 17.5]]
    }


    # Trail's End
    async def tt_trails_end_ex(handler, arg):
        if arg == 'tunnel':
            # do something
            return False

    ow[TT_TRAILS_END] = {
        'name': 'Trail\'s End',
        'desc': '',
        'img': 'https://i.imgur.com/3uexCjr.png',
        'ex': tt_trails_end_ex,
        'actions': ['tunnel'],
    }

    # New Trainer Alley
    async def tt_new_trainer_alley_ex(handler, arg):
        pass

    ow[TT_NEW_TRAINER_ALLEY] = {
        'name': 'New Trainer Alley',
        'desc': '',
        'img': 'https://i.imgur.com/JUD5sGU.png',
        'ex': tt_new_trainer_alley_ex,
        #'actions': [''],
    }

    # Swamp Edge
    async def tt_swamp_edge_ex(handler, arg):
        if arg == 'swamp':
            await handler.move_to(swamp.MS_BOARDWALK_BOG)
            return True

    ow[TT_SWAMP_EDGE] = {
        'name': 'Swamp Edge',
        'desc': '',
        'img': 'https://i.imgur.com/gfZfBwg.png',
        'ex': tt_swamp_edge_ex,
        'actions': ['swamp'],
    }

    # Trail Fork
    async def tt_trail_fork_ex(handler, arg):
        pass

    ow[TT_TRAIL_FORK] = {
        'name': 'Trail Fork',
        'desc': '',
        'img': 'https://i.imgur.com/YL8jmQX.png',
        'ex': tt_trail_fork_ex,
        #'actions': [''],
    }
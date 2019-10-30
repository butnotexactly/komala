from common import *

ID = 44

WISH_PEAK = 4400
WISH_DESCENT = 4401

def setup(areas, ow):
    areas[ID] = {
        'name': 'Wish Mountain',
        'emoji': '<:anin:414520574354915348> ',
        'dialog': '',
        'map': [[WISH_PEAK],
            [WISH_DESCENT]]
    }


    # Peak
    async def wish_peak_ex(handler, arg):
        pass

    ow[WISH_PEAK] = {
        'name': 'Peak',
        'desc': '',
        'img': 'https://i.imgur.com/oMCZWkP.png',
        'ex': wish_peak_ex,
        #'actions': [''],
    }

    # Descent
    async def wish_descent_ex(handler, arg):
        pass

    ow[WISH_DESCENT] = {
        'name': 'Descent',
        'desc': '',
        'img': 'https://i.imgur.com/Eyzu4D8.png',
        'ex': wish_descent_ex,
        #'actions': [''],
    }
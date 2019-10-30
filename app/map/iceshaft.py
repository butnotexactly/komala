from common import *
from . import christmas

ID = 41

IS_DROPDOWN = 4100
IS_TITANS_DOMAIN = 4101

def setup(areas, ow):
    areas[ID] = {
        'name': 'Ice Shaft',
        'emoji': '<:reg:414524337564024832>',
        'dialog': '',
        'map': [[IS_DROPDOWN],
                [IS_TITANS_DOMAIN]]
    }


    # Dropdown
    async def is_dropdown_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(christmas.NCV_CHIMNEY)
            return True

    ow[IS_DROPDOWN] = {
        'name': 'Dropdown',
        'desc': '',
        'img': 'https://i.imgur.com/mjTlNlr.png',
        'ex': is_dropdown_ex,
        'actions': ['ladder'],
    }

    # Titan's Domain
    async def is_titans_domain_ex(handler, arg):
        pass

    ow[IS_TITANS_DOMAIN] = {
        'name': 'Titan\'s Domain',
        'desc': '',
        'img': 'https://i.imgur.com/NB1A3XH.png',
        'ex': is_titans_domain_ex,
        #'actions': [''],
    }
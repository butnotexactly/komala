from common import *
from . import swamptemple

ID = 9
PREFIX = 'LV'

LV_TEMPLE_ENTRANCE = 900
LV_MANGROVES = 901
LV_VILLAGE_ENTRANCE = 902
LV_VILLAGE_HUTS = 903
LV_WILDLANDS = 904
LV_QUAGMIRE = 905

def setup(areas, ow):
    areas[ID] = {
        'name': 'Lost Village',
        'emoji': '<:tapk:414533899251744770> ',
        'dialog': '',
        'map': [[LV_TEMPLE_ENTRANCE, LV_MANGROVES],
            [LV_VILLAGE_ENTRANCE, LV_VILLAGE_HUTS],
            [LV_WILDLANDS, LV_QUAGMIRE]]
    }


    # Temple Entrance
    async def lv_temple_entrance_ex(handler, arg):
        if arg == 'temple':
            await handler.move_to(swamptemple.ST_ANTEROOM)
            return True

    ow[LV_TEMPLE_ENTRANCE] = {
        'name': 'Temple Entrance',
        'desc': '',
        'img': 'https://i.imgur.com/34Zmiz1.png',
        'ex': lv_temple_entrance_ex,
        'actions': ['temple'],
    }

    # Mangroves
    async def lv_mangroves_ex(handler, arg):
        pass

    ow[LV_MANGROVES] = {
        'name': 'Mangroves',
        'desc': '',
        'img': 'https://i.imgur.com/IjiyOdf.png',
        'ex': lv_mangroves_ex,
        #'actions': [''],
    }

    # Village Entrance
    async def lv_village_entrance_ex(handler, arg):
        pass

    ow[LV_VILLAGE_ENTRANCE] = {
        'name': 'Village Entrance',
        'desc': '',
        'img': 'https://i.imgur.com/E8hWlQS.png',
        'ex': lv_village_entrance_ex,
        #'actions': [''],
    }

    # Village Huts
    async def lv_village_huts_ex(handler, arg):
        pass

    ow[LV_VILLAGE_HUTS] = {
        'name': 'Village Huts',
        'desc': '',
        'img': 'https://i.imgur.com/Jx8mPn0.png',
        'ex': lv_village_huts_ex,
        #'actions': [''],
    }

    # Wildlands
    async def lv_wildlands_ex(handler, arg):
        pass

    ow[LV_WILDLANDS] = {
        'name': 'Wildlands',
        'desc': '',
        'img': 'https://i.imgur.com/Gu59QT5.png',
        'ex': lv_wildlands_ex,
        'blocked': [E],
        #'actions': [''],
    }

    # Quagmire
    async def lv_quagmire_ex(handler, arg):
        pass

    ow[LV_QUAGMIRE] = {
        'name': 'Quagmire',
        'desc': '',
        'img': 'https://i.imgur.com/PnbYnKN.png',
        'ex': lv_quagmire_ex,
        'blocked': [W],
        #'actions': [''],
    }
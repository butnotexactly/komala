from common import *
from . import cubchoo, iceshaft

ID = 40

NCV_WINTER_PARK = 4000
NCV_DOWNTOWN = 4001
NCV_GRAND_CHRISTMAS_TREE = 4002
NCV_ALLEYWAY = 4003
NCV_HOUSE = 4004
NCV_DELIBIRD_LAKE = 4005
NCV_VILLAGE_EDGE = 4006
NCV_CHIMNEY = 4007

def setup(areas, ow):
    areas[ID] = {
        'name': 'New Christmas Village',
        'emoji': '<:deli:414487929931431937> ',
        'dialog': '',
        'map': [[NCV_WINTER_PARK, NCV_DOWNTOWN],
            [NCV_GRAND_CHRISTMAS_TREE, NCV_ALLEYWAY],
            [NCV_HOUSE, NCV_DELIBIRD_LAKE],
            [NCV_VILLAGE_EDGE, NCV_CHIMNEY]]
    }


    # Winter Park
    async def ncv_winter_park_ex(handler, arg):
        pass

    ow[NCV_WINTER_PARK] = {
        'name': 'Winter Park',
        'desc': '',
        'img': 'https://i.imgur.com/3lFjoP6.png',
        'ex': ncv_winter_park_ex,
        #'actions': [''],
    }

    # Downtown
    async def ncv_downtown_ex(handler, arg):
        pass

    ow[NCV_DOWNTOWN] = {
        'name': 'Downtown',
        'desc': '',
        'img': 'https://i.imgur.com/Ebsr5uU.png',
        'ex': ncv_downtown_ex,
        #'actions': [''],
    }

    # Grand Christmas Tree
    async def ncv_grand_christmas_tree_ex(handler, arg):
        pass

    ow[NCV_GRAND_CHRISTMAS_TREE] = {
        'name': 'Grand Christmas Tree',
        'desc': '',
        'img': 'https://i.imgur.com/fjUdpNi.png',
        'ex': ncv_grand_christmas_tree_ex,
        #'actions': [''],
    }

    # Alleyway
    async def ncv_alleyway_ex(handler, arg):
        pass

    ow[NCV_ALLEYWAY] = {
        'name': 'Alleyway',
        'desc': '',
        'img': 'https://i.imgur.com/r2reXSa.png',
        'ex': ncv_alleyway_ex,
        #'actions': [''],
    }

    # ???'s House
    async def ncv_house_ex(handler, arg):
        pass

    ow[NCV_HOUSE] = {
        'name': '???\'s House',
        'desc': '',
        'img': 'https://i.imgur.com/DwyNfE9.png',
        'ex': ncv_house_ex,
        #'actions': [''],
    }

    # Delibird Lake
    async def ncv_delibird_lake_ex(handler, arg):
        pass

    ow[NCV_DELIBIRD_LAKE] = {
        'name': 'Delibird Lake',
        'desc': '',
        'img': 'https://i.imgur.com/Lmj6VDQ.png',
        'ex': ncv_delibird_lake_ex,
        #'actions': [''],
    }

    # Village Edge
    async def ncv_village_edge_ex(handler, arg):
        pass

    ow[NCV_VILLAGE_EDGE] = {
        'name': 'Pleasant Path',
        'desc': '',
        'img': 'https://i.imgur.com/q42QVaG.png',
        'ex': ncv_village_edge_ex,
        #'actions': [''],
    }

    # Chimney
    async def ncv_chimney_ex(handler, arg):
        if 'chimney' in arg:
            await handler.move_to(iceshaft.IS_DROPDOWN)
            return True

    ow[NCV_CHIMNEY] = {
        'name': 'Village Corner',
        'desc': '',
        'img': 'https://i.imgur.com/J8mRW71.png',
        'ex': ncv_chimney_ex,
        'actions': ['chimney'],
    }
from common import *

ID = 30

PT_FIRST_SNOW = 3000
PT_HIKE_START = 3001
PT_NIDORAN_NEST = 3002
PT_ASCENT = 3003

def setup(areas, ow):
    areas[ID] = {
        'name': 'Pewter Trail',
        'emoji': '<:nid4:414516445125410826>',
        'dialog': '',
        'map': [[None, None, PT_FIRST_SNOW],
                [PT_HIKE_START, PT_NIDORAN_NEST, PT_ASCENT]]
    }


    # First Snow
    async def pt_first_snow_ex(handler, arg):
        pass

    ow[PT_FIRST_SNOW] = {
        'name': 'First Snow',
        'desc': '',
        'img': 'https://i.imgur.com/lSyxtwT.png',
        'ex': pt_first_snow_ex,
        #'actions': [''],
    }

    # Hike Start
    async def pt_hike_start_ex(handler, arg):
        pass

    ow[PT_HIKE_START] = {
        'name': 'Hike Start',
        'desc': '',
        'img': 'https://i.imgur.com/v9OuXGw.png',
        'ex': pt_hike_start_ex,
        #'actions': [''],
    }

    # Nidoran Nest
    async def pt_nidoran_nest_ex(handler, arg):
        pass

    ow[PT_NIDORAN_NEST] = {
        'name': 'Nidoran Nest',
        'desc': '',
        'img': 'https://i.imgur.com/miFDo23.png',
        'ex': pt_nidoran_nest_ex,
        #'actions': [''],
    }

    # Ascent
    async def pt_ascent_ex(handler, arg):
        pass

    ow[PT_ASCENT] = {
        'name': 'Ascent',
        'desc': '',
        'img': 'https://i.imgur.com/hCEtwHt.png',
        'ex': pt_ascent_ex,
        #'actions': [''],
    }
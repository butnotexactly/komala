from common import *
from . import seacrevice

ID = 16

CW_WATERSIDE_CLIFFS = 1600
CW_ISLE = 1601
CW_MT_SULFUR = 1602
CW_RIDGELINE = 1603
CW_SURFACE = 1604
CW_EAST_SHORE = 1605
CW_LUSH_TRAIL = 1606
CW_SOUTH_SHORE = 1607
CW_SANDY_DUNES = 1608

def setup(areas, ow):
    areas[ID] = {
        'name': 'Coastwalk',
        'emoji': '<:exgu:414492391496744960>', #'<:fly:414492391530168321>',
        'dialog': '',
        'map': [[CW_WATERSIDE_CLIFFS, CW_ISLE, CW_MT_SULFUR],
			[CW_RIDGELINE, CW_SURFACE, CW_EAST_SHORE],
			[CW_LUSH_TRAIL, CW_SOUTH_SHORE, CW_SANDY_DUNES]]
    }


    # Waterside Cliffs
    async def cw_waterside_cliffs_ex(handler, arg):
        pass

    ow[CW_WATERSIDE_CLIFFS] = {
        'name': 'Waterside Cliffs',
        'desc': '',
        'img': 'https://i.imgur.com/b9J1wVh.png',
        'ex': cw_waterside_cliffs_ex,
        #'actions': [''],
    }

    # Isle
    async def cw_isle_ex(handler, arg):
        pass

    ow[CW_ISLE] = {
        'name': 'Isle',
        'desc': '',
        'img': 'https://i.imgur.com/eEmayBX.png',
        'ex': cw_isle_ex,
        'blocked': [E, S],
        #'actions': [''],
    }

    # Mt. Sulfur
    async def cw_mt_sulfur_ex(handler, arg):
        pass

    ow[CW_MT_SULFUR] = {
        'name': 'Mt. Sulfur',
        'desc': '',
        'img': 'https://i.imgur.com/Pdkg3pf.png',
        'ex': cw_mt_sulfur_ex,
        'blocked': [W],
        #'actions': [''],
    }

    # Ridgeline
    async def cw_ridgeline_ex(handler, arg):
        pass

    ow[CW_RIDGELINE] = {
        'name': 'Ridgeline',
        'desc': '',
        'img': 'https://i.imgur.com/kEQlir9.png',
        'ex': cw_ridgeline_ex,
        'blocked': [E],
        #'actions': [''],
    }

    # Surface
    async def cw_surface_ex(handler, arg):
        if 'dewgong' in arg:
            #todo fix
            dex = handler.dex_entry('Blastoise')
            await handler.show_dialog('Dewgong', f'Follow the Dewgong to the seafloor?{DBL_BREAK}※  `yes` or `no`', color=TYPE_COLORS[dex['type']], image=dex['gif'], thumb=True)
            return True

        if arg == 'no':
            await handler.show_location()
            return True

        if arg == 'yes':
            await handler.move_to(seacrevice.SFC_HORSEA_NEST)
            return True

    ow[CW_SURFACE] = {
        'name': 'Surface',
        'desc': '',
        'img': 'https://i.imgur.com/s2G2zBw.png',
        'ex': cw_surface_ex,
        'blocked': [N, W],
        'actions': ['dewgong'],
    }

    # East Shore
    async def cw_east_shore_ex(handler, arg):
        pass

    ow[CW_EAST_SHORE] = {
        'name': 'East Shore',
        'desc': '',
        'img': 'https://i.imgur.com/74JAq1N.png',
        'ex': cw_east_shore_ex,
        #'actions': [''],
    }

    # Lush Trail
    async def cw_lush_trail_ex(handler, arg):
        pass

    ow[CW_LUSH_TRAIL] = {
        'name': 'Lush Trail',
        'desc': '',
        'img': 'https://i.imgur.com/1nHotf6.png',
        'ex': cw_lush_trail_ex,
        #'actions': [''],
    }

    # South Shore
    async def cw_south_shore_ex(handler, arg):
        pass

    ow[CW_SOUTH_SHORE] = {
        'name': 'South Shore',
        'desc': '',
        'img': 'https://i.imgur.com/EOHnZDS.png',
        'ex': cw_south_shore_ex,
        #'actions': [''],
    }

    # Sandy Dunes
    async def cw_sandy_dunes_ex(handler, arg):
        pass

    ow[CW_SANDY_DUNES] = {
        'name': 'Sandy Dunes',
        'desc': '',
        'img': 'https://i.imgur.com/rP6n77H.png',
        'ex': cw_sandy_dunes_ex,
        #'actions': [''],
    }
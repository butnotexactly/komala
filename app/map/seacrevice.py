from common import *
from . import seafloor, coastwalk

ID = 15

SFC_SEA_PASSAGE_W = 1500
SFC_CORSOLA_CORALS = 1501
SFC_SEA_PASSAGE_E = 1502
SFC_CRAGS = 1503
SFC_GREAT_SEA_CREVICE = 1504
SFC_ABYSS_EDGE = 1505
SFC_HORSEA_NEST = 1506
SFC_STILL_WATERS = 1507
SFC_DEEP_SEA = 1508

def setup(areas, ow):
    areas[ID] = {
        'name': 'Sea Floor',
        'emoji': '',
        'dialog': '',
        'map': [[SFC_SEA_PASSAGE_W, SFC_CORSOLA_CORALS, SFC_SEA_PASSAGE_E],
                [SFC_CRAGS, SFC_GREAT_SEA_CREVICE, SFC_ABYSS_EDGE],
                [SFC_HORSEA_NEST, SFC_STILL_WATERS, SFC_DEEP_SEA]]
    }


    # Sea Passage
    async def sfc_sea_passage_w_ex(handler, arg):
        pass

    ow[SFC_SEA_PASSAGE_W] = {
        'name': 'Sea Passage',
        'desc': '',
        'img': 'https://i.imgur.com/gE0ryo9.png',
        'ex': sfc_sea_passage_w_ex,
        #'actions': [''],
    }

    # Corsola Corals
    async def sfc_corsola_corals_ex(handler, arg):
        pass

    ow[SFC_CORSOLA_CORALS] = {
        'name': 'Corsola Corals',
        'desc': '',
        'img': 'https://i.imgur.com/kGynehj.png',
        'ex': sfc_corsola_corals_ex,
        #'actions': [''],
    }

    # Sea Passage
    async def sfc_sea_passage_e_ex(handler, arg):
        pass

    ow[SFC_SEA_PASSAGE_E] = {
        'name': 'Sea Passage',
        'desc': '',
        'img': 'https://i.imgur.com/GsP2hGJ.png',
        'ex': sfc_sea_passage_e_ex,
        #'actions': [''],
    }

    # Crags
    async def sfc_crags_ex(handler, arg):
        pass

    ow[SFC_CRAGS] = {
        'name': 'Crags',
        'desc': '',
        'img': 'https://i.imgur.com/vP8e7Dy.png',
        'ex': sfc_crags_ex,
        #'actions': [''],
    }

    # Great Sea Crevice
    async def sfc_great_sea_crevice_ex(handler, arg):
        pass

    ow[SFC_GREAT_SEA_CREVICE] = {
        'name': 'Great Sea Crevice',
        'desc': '',
        'img': 'https://i.imgur.com/hf0VurJ.png',
        'ex': sfc_great_sea_crevice_ex,
        #'actions': [''],
    }

    # Abyss Edge
    async def sfc_abyss_edge_ex(handler, arg):
        pass

    ow[SFC_ABYSS_EDGE] = {
        'name': 'Abyss Edge',
        'desc': '',
        'img': 'https://i.imgur.com/fU86ZHw.png',
        'ex': sfc_abyss_edge_ex,
        #'actions': [''],
    }

    # Horsea Nest
    async def sfc_horsea_nest_ex(handler, arg):

        if 'dewgong' in arg:
            #todo fix
            dex = handler.dex_entry('Blastoise')
            await handler.show_dialog('Dewgong', f'Follow the Dewgong to the surface?{DBL_BREAK}※  `yes` or `no`', color=TYPE_COLORS[dex['type']], image=dex['gif'], thumb=True)
            return True

        if arg == 'no':
            await handler.show_location()
            return True

        if arg == 'yes':
            await handler.move_to(coastwalk.CW_SURFACE)
            return True


    ow[SFC_HORSEA_NEST] = {
        'name': 'Horsea Nest',
        'desc': '',
        'img': 'https://i.imgur.com/QcfcTBu.png',
        'ex': sfc_horsea_nest_ex,
        'actions': ['dewgong'],
    }

    # Still Waters
    async def sfc_still_waters_ex(handler, arg):
        pass

    ow[SFC_STILL_WATERS] = {
        'name': 'Still Waters',
        'desc': '',
        'img': 'https://i.imgur.com/AxY0dMS.png',
        'ex': sfc_still_waters_ex,
        #'actions': [''],
    }

    # Deep Sea
    async def sfc_deep_sea_ex(handler, arg):
        pass

    ow[SFC_DEEP_SEA] = {
        'name': 'Deep Sea',
        'desc': '',
        'img': 'https://i.imgur.com/G6OPRk1.png',
        'ex': sfc_deep_sea_ex,
        #'actions': [''],
    }
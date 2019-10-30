from common import *

ID = 61

DF_OLD_BRIDGE = 6100
DF_MURKROW_ELM = 6101
DF_SCARY_WOODS = 6102
DF_FUNGI_PATCH = 6103
DF_PANCHAM_PASS = 6104
DF_FOREST_DEPTHS = 6105
DF_LABYRINTH = 6106
DF_FOREST_EDGE = 6107
DF_CITY_OPENING = 6108
DF_WINDING_TRAIL = 6109
DF_BLACK_POND = 6110
DF_SHIFTRY_TREES = 6111

def setup(areas, ow):
    areas[ID] = {
        'name': 'Dark Forest',
        'emoji': '<:mur:414516274169643028>',
        'dialog': '',
        'map': [[DF_OLD_BRIDGE, DF_MURKROW_ELM, DF_SCARY_WOODS, DF_FUNGI_PATCH],
            [DF_PANCHAM_PASS, DF_FOREST_DEPTHS, DF_LABYRINTH, DF_FOREST_EDGE],
            [DF_CITY_OPENING, DF_WINDING_TRAIL, DF_BLACK_POND, DF_SHIFTRY_TREES]]
    }


    # Old Bridge
    async def df_old_bridge_ex(handler, arg):
        pass

    ow[DF_OLD_BRIDGE] = {
        'name': 'Old Bridge',
        'desc': '',
        'img': 'https://i.imgur.com/My1DefV.png',
        'ex': df_old_bridge_ex,
        #'actions': [''],
    }

    # Murkrow Elm
    async def df_murkrow_elm_ex(handler, arg):
        pass

    ow[DF_MURKROW_ELM] = {
        'name': 'Murkrow Elm',
        'desc': '',
        'img': 'https://i.imgur.com/ifz6bdz.png',
        'ex': df_murkrow_elm_ex,
        #'actions': [''],
    }

    # Scary Woods
    async def df_scary_woods_ex(handler, arg):
        pass

    ow[DF_SCARY_WOODS] = {
        'name': 'Scary Woods',
        'desc': '',
        'img': 'https://i.imgur.com/vfAlpZR.png',
        'ex': df_scary_woods_ex,
        #'actions': [''],
    }

    # Fungi Patch
    async def df_fungi_patch_ex(handler, arg):
        pass

    ow[DF_FUNGI_PATCH] = {
        'name': 'Fungi Patch',
        'desc': '',
        'img': 'https://i.imgur.com/MVKVx9Z.png',
        'ex': df_fungi_patch_ex,
        #'actions': [''],
    }

    # Pancham Pass
    async def df_pancham_pass_ex(handler, arg):
        pass

    ow[DF_PANCHAM_PASS] = {
        'name': 'Pancham Pass',
        'desc': '',
        'img': 'https://i.imgur.com/IrEdTLx.png',
        'ex': df_pancham_pass_ex,
        #'actions': [''],
    }

    # Forest Depths
    async def df_forest_depths_ex(handler, arg):
        pass

    ow[DF_FOREST_DEPTHS] = {
        'name': 'Forest Depths',
        'desc': '',
        'img': 'https://i.imgur.com/TyUPzsv.png',
        'ex': df_forest_depths_ex,
        #'actions': [''],
    }

    # Labyrinth
    async def df_labyrinth_ex(handler, arg):
        pass

    ow[DF_LABYRINTH] = {
        'name': 'Labyrinth',
        'desc': '',
        'img': 'https://i.imgur.com/0gxNwjY.png',
        'ex': df_labyrinth_ex,
        #'actions': [''],
    }

    # Forest Edge
    async def df_forest_edge_ex(handler, arg):
        pass

    ow[DF_FOREST_EDGE] = {
        'name': 'Forest Edge',
        'desc': '',
        'img': 'https://i.imgur.com/KmihC9A.png',
        'ex': df_forest_edge_ex,
        #'actions': [''],
    }

    # City Opening
    async def df_city_opening_ex(handler, arg):
        pass

    ow[DF_CITY_OPENING] = {
        'name': 'City Opening',
        'desc': '',
        'img': 'https://i.imgur.com/jetMwJJ.png',
        'ex': df_city_opening_ex,
        #'actions': [''],
    }

    # Winding Trail
    async def df_winding_trail_ex(handler, arg):
        pass

    ow[DF_WINDING_TRAIL] = {
        'name': 'Winding Trail',
        'desc': '',
        'img': 'https://i.imgur.com/5vDCVwZ.png',
        'ex': df_winding_trail_ex,
        #'actions': [''],
    }

    # Black Pond
    async def df_black_pond_ex(handler, arg):
        pass

    ow[DF_BLACK_POND] = {
        'name': 'Black Pond',
        'desc': '',
        'img': 'https://i.imgur.com/fuKTGwq.png',
        'ex': df_black_pond_ex,
        #'actions': [''],
    }

    # Shiftry Trees
    async def df_shiftry_trees_ex(handler, arg):
        pass

    ow[DF_SHIFTRY_TREES] = {
        'name': 'Shiftry Trees',
        'desc': '',
        'img': 'https://i.imgur.com/NDwSR4M.png',
        'ex': df_shiftry_trees_ex,
        #'actions': [''],
    }
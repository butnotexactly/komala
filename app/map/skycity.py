from common import *
from . import fairypass

ID = 12
PREFIX = 'SC'

SC_CREST = 1200
SC_STATUE = 1201
SC_TEMPLE_SUMMIT = 1202
SC_EASTERN_TEMPLE = 1203
SC_A_CALM_RESPITE = 1204
SC_TEMPLE_GROUNDS = 1205
SC_LILYWATER = 1206
SC_SUNFLOWER_FIELD = 1207
SC_RIVERSIDE = 1208
SC_RAINBOW_ORCHARD = 1209
SC_BRIDGE = 1210
SC_SKY_CAVERNS = 1211
SC_ALTARIA_FALLS = 1212
SC_DROPOFF = 1213
SC_FAIRY_FALLS = 1214
SC_ISLAND_RAPIDS = 1215
SC_CLOUDY_CLIMB = 1216
SC_WHITE_SEA = 1217
SC_LANDING = 1218
SC_ISLAND_HOPPING = 1219

def setup(areas, ow):
    areas[ID] = {
        'name': 'Skycity of Arceus',
        'emoji': '<:mpid:414520574241406976> ',
        'dialog': '',
        'map': [[SC_CREST, SC_STATUE, SC_TEMPLE_SUMMIT, SC_EASTERN_TEMPLE],
            [SC_A_CALM_RESPITE, SC_TEMPLE_GROUNDS, SC_LILYWATER, SC_SUNFLOWER_FIELD],
            [SC_RIVERSIDE, SC_RAINBOW_ORCHARD, SC_BRIDGE, SC_SKY_CAVERNS],
            [SC_ALTARIA_FALLS, SC_DROPOFF, SC_FAIRY_FALLS, SC_ISLAND_RAPIDS],
            [SC_CLOUDY_CLIMB, SC_WHITE_SEA, SC_LANDING, SC_ISLAND_HOPPING]]
    }


    # Crest
    async def sc_crest_ex(handler, arg):
        pass

    ow[SC_CREST] = {
        'name': 'Crest',
        'desc': '',
        'img': 'https://i.imgur.com/Boz7ths.png',
        'ex': sc_crest_ex,
        'blocked': [E],
        #'actions': [''],
    }

    # Statue
    async def sc_statue_ex(handler, arg):
        pass

    ow[SC_STATUE] = {
        'name': 'Statue',
        'desc': '',
        'img': 'https://i.imgur.com/3aBVV5u.png',
        'ex': sc_statue_ex,
        'blocked': [W],
        #'actions': [''],
    }

    # Temple Summit
    async def sc_temple_summit_ex(handler, arg):
        pass

    ow[SC_TEMPLE_SUMMIT] = {
        'name': 'Temple Summit',
        'desc': '',
        'img': 'https://i.imgur.com/JISH7BL.png',
        'ex': sc_temple_summit_ex,
        'blocked': [E],
        #'actions': [''],
    }

    # Eastern Temple
    async def sc_eastern_temple_ex(handler, arg):
        pass

    ow[SC_EASTERN_TEMPLE] = {
        'name': 'Eastern Temple',
        'desc': '',
        'img': 'https://i.imgur.com/B3WNRnN.png',
        'ex': sc_eastern_temple_ex,
        'blocked': [W],
        #'actions': [''],
    }

    # A Calm Respite
    async def sc_a_calm_respite_ex(handler, arg):
        pass

    ow[SC_A_CALM_RESPITE] = {
        'name': 'A Calm Respite',
        'desc': '',
        'img': 'https://i.imgur.com/pUnfM63.png',
        'ex': sc_a_calm_respite_ex,
        #'actions': [''],
    }

    # Temple Grounds
    async def sc_temple_grounds_ex(handler, arg):
        pass

    ow[SC_TEMPLE_GROUNDS] = {
        'name': 'Temple Grounds',
        'desc': '',
        'img': 'https://i.imgur.com/X524dzw.png',
        'ex': sc_temple_grounds_ex,
        #'actions': [''],
    }

    # Lilywater
    async def sc_lilywater_ex(handler, arg):
        pass

    ow[SC_LILYWATER] = {
        'name': 'Lilywater',
        'desc': '',
        'img': 'https://i.imgur.com/woqBsiq.png',
        'ex': sc_lilywater_ex,
        'blocked': [E],
        #'actions': [''],
    }

    # Sunflower Field
    async def sc_sunflower_field_ex(handler, arg):
        pass

    ow[SC_SUNFLOWER_FIELD] = {
        'name': 'Sunflower Field',
        'desc': '',
        'img': 'https://i.imgur.com/uXtdleR.png',
        'ex': sc_sunflower_field_ex,
        'blocked': [W],
        #'actions': [''],
    }

    # Riverside
    async def sc_riverside_ex(handler, arg):
        pass

    ow[SC_RIVERSIDE] = {
        'name': 'Riverside',
        'desc': '',
        'img': 'https://i.imgur.com/VkAX2rQ.png',
        'ex': sc_riverside_ex,
        #'actions': [''],
    }

    # Rainbow Orchard
    async def sc_rainbow_orchard_ex(handler, arg):
        pass

    ow[SC_RAINBOW_ORCHARD] = {
        'name': 'Rainbow Orchard',
        'desc': '',
        'img': 'https://i.imgur.com/poT9Qcy.png',
        'ex': sc_rainbow_orchard_ex,
        #'actions': [''],
    }

    # Bridge
    async def sc_bridge_ex(handler, arg):
        pass

    ow[SC_BRIDGE] = {
        'name': 'Bridge',
        'desc': '',
        'img': 'https://i.imgur.com/WO4PCyP.png',
        'ex': sc_bridge_ex,
        'blocked': [S],
        #'actions': [''],
    }

    # Sky Caverns
    async def sc_sky_caverns_ex(handler, arg):
        pass

    ow[SC_SKY_CAVERNS] = {
        'name': 'Sky Caverns',
        'desc': '',
        'img': 'https://i.imgur.com/ZMKvhmc.png',
        'ex': sc_sky_caverns_ex,
        #'actions': [''],
    }

    # Altaria Falls
    async def sc_altaria_falls_ex(handler, arg):
        pass

    ow[SC_ALTARIA_FALLS] = {
        'name': 'Altaria Falls',
        'desc': '',
        'img': 'https://i.imgur.com/An5tLEX.png',
        'ex': sc_altaria_falls_ex,
        'blocked': [E],
        #'actions': [''],
    }

    # Dropoff
    async def sc_dropoff_ex(handler, arg):
        pass

    ow[SC_DROPOFF] = {
        'name': 'Dropoff',
        'desc': '',
        'img': 'https://i.imgur.com/LXu1U9T.png',
        'ex': sc_dropoff_ex,
        'blocked': [W],
        #'actions': [''],
    }

    # Fairy Falls
    async def sc_fairy_falls_ex(handler, arg):
        pass

    ow[SC_FAIRY_FALLS] = {
        'name': 'Fairy Falls',
        'desc': '',
        'img': 'https://i.imgur.com/FMHqt1H.png',
        'ex': sc_fairy_falls_ex,
        'blocked': [N, E],
        #'actions': [''],
    }

    # Island Rapids
    async def sc_island_rapids_ex(handler, arg):
        pass

    ow[SC_ISLAND_RAPIDS] = {
        'name': 'Island Rapids',
        'desc': '',
        'img': 'https://i.imgur.com/UL8qw60.png',
        'ex': sc_island_rapids_ex,
        #'actions': [''],
    }

    # Cloudy Climb
    async def sc_cloudy_climb_ex(handler, arg):
        pass

    ow[SC_CLOUDY_CLIMB] = {
        'name': 'Cloudy Climb',
        'desc': '',
        'img': 'https://i.imgur.com/gyfwKV4.png',
        'ex': sc_cloudy_climb_ex,
        'blocked': [E],
        #'actions': [''],
    }

    # White Sea
    async def sc_white_sea_ex(handler, arg):
        pass

    ow[SC_WHITE_SEA] = {
        'name': 'White Sea',
        'desc': '',
        'img': 'https://i.imgur.com/HdfexmI.png',
        'ex': sc_white_sea_ex,
        'blocked': [E, W],
        #'actions': [''],
    }

    # Landing
    async def sc_landing_ex(handler, arg):
        #todo fix
        if 'latias' in arg:
            dex = handler.dex_entry('Charizard')
            await handler.show_dialog('The Legendary Eon Pokémon', f'Return to ground level with Latias?{DBL_BREAK}※  `yes` or `no`', color=TYPE_COLORS[dex['type']], image=dex['gif'], thumb=True)
            return True

        if arg == 'no':
            await handler.show_location()
            return True

        if arg == 'yes':
            await handler.move_to(fairypass.FP_AIR_LIFT)
            return True

    ow[SC_LANDING] = {
        'name': 'Landing',
        'desc': '',
        'img': 'https://i.imgur.com/2zNXWKb.png',
        'ex': sc_landing_ex,
        'blocked': [E, W],
        'actions': ['latias'],
    }

    # Island Hopping
    async def sc_island_hopping_ex(handler, arg):
        pass

    ow[SC_ISLAND_HOPPING] = {
        'name': 'Island Hopping',
        'desc': '',
        'img': 'https://i.imgur.com/xoHjICC.png',
        'ex': sc_island_hopping_ex,
        #'actions': [''],
    }


from common import *

ID = 31

CC_CAVE_TUNNEL = 3100
CC_CLIMB = 3101
CC_ICE_FOSSILS = 3102
CC_PEWTER_ENTRANCE = 3103

CC_VANILLITE_STALAGMITES = 3104
CC_BERGMITE_STALACTITES = 3105
CC_CUBCHOO_DEN = 3106
CC_SWINUB_NEST = 3107

CC_SPHEAL_SANCTUARY = 3108
CC_A_FROZEN_RESPITE = 3109

CC_SNOWS_SECRET = 3110

CC_FROSTY_SLIDE = 3111
CC_LAST_STRETCH = 3112
CC_NORTH_FACE = 3113
CC_CHRISTMAS_ENTRANCE = 3114


def setup(areas, ow):
    areas[ID] = {
        'name': 'Cubchoo Caverns',
        'emoji': '<:cub:414487644655845376> ',
        'dialog': '',
    }

    r1map = [[CC_CAVE_TUNNEL, CC_CLIMB],
             [CC_ICE_FOSSILS, CC_PEWTER_ENTRANCE]]

    # Cave Tunnel
    async def cc_cave_tunnel_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(CC_CUBCHOO_DEN)
            return True

    ow[CC_CAVE_TUNNEL] = {
        'name': 'Cave Tunnel',
        'desc': '',
        'img': 'https://i.imgur.com/3uLOMqd.png',
        'ex': cc_cave_tunnel_ex,
        'map': r1map,
        'actions': ['ladder'],
    }

    # Climb
    async def cc_climb_ex(handler, arg):
        pass

    ow[CC_CLIMB] = {
        'name': 'Climb',
        'desc': '',
        'img': 'https://i.imgur.com/3PCTRkj.png',
        'ex': cc_climb_ex,
        'map': r1map,
        #'actions': [''],
    }

    # Ice Fossils
    async def cc_ice_fossils_ex(handler, arg):
        pass

    ow[CC_ICE_FOSSILS] = {
        'name': 'Ice Fossils',
        'desc': '',
        'img': 'https://i.imgur.com/0a1tqxT.png',
        'ex': cc_ice_fossils_ex,
        'map': r1map,
        #'actions': [''],
    }

    # Pewter Entrance
    async def cc_pewter_entrance_ex(handler, arg):
        pass

    ow[CC_PEWTER_ENTRANCE] = {
        'name': 'Pewter Entrance',
        'desc': '',
        'img': 'https://i.imgur.com/dCEUnFB.png',
        'ex': cc_pewter_entrance_ex,
        'map': r1map,
        #'actions': [''],
    }







    r2map = [[CC_VANILLITE_STALAGMITES, CC_BERGMITE_STALACTITES],
             [CC_CUBCHOO_DEN, CC_SWINUB_NEST]]

    # Vanillite Stalagmites
    async def cc_vanillite_stalagmites_ex(handler, arg):
        if 'left' in arg:
            await handler.move_to(CC_SNOWS_SECRET)
            return True

        if 'right' in arg:
            await handler.move_to(CC_NORTH_FACE)
            return True

    ow[CC_VANILLITE_STALAGMITES] = {
        'name': 'Vanillite Stalagmites',
        'desc': '',
        'img': 'https://i.imgur.com/Jlzagxt.png',
        'ex': cc_vanillite_stalagmites_ex,
        'map': r2map,
        'actions': ['left ladder', 'right ladder'],
    }

    # Bergmite Stalactites
    async def cc_bergmite_stalactites_ex(handler, arg):
        pass

    ow[CC_BERGMITE_STALACTITES] = {
        'name': 'Bergmite Stalactites',
        'desc': '',
        'img': 'https://i.imgur.com/O0GxLGo.png',
        'ex': cc_bergmite_stalactites_ex,
        'map': r2map,
        #'actions': [''],
    }

    # Cubchoo Den
    async def cc_cubchoo_den_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(CC_CAVE_TUNNEL)
            return True

    ow[CC_CUBCHOO_DEN] = {
        'name': 'Cubchoo Den',
        'desc': '',
        'img': 'https://i.imgur.com/mQGspf9.png',
        'ex': cc_cubchoo_den_ex,
        'map': r2map,
        'actions': ['ladder'],
    }

    # Swinub Nest
    async def cc_swinub_nest_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(CC_SPHEAL_SANCTUARY)
            return True

    ow[CC_SWINUB_NEST] = {
        'name': 'Swinub Nest',
        'desc': '',
        'img': 'https://i.imgur.com/o03YhaW.png',
        'ex': cc_swinub_nest_ex,
        'map': r2map,
        'actions': ['ladder'],
    }








    # Spheal Sanctuary
    async def cc_spheal_sanctuary_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(CC_SWINUB_NEST)
            return True

    ow[CC_SPHEAL_SANCTUARY] = {
        'name': 'Spheal Sanctuary',
        'desc': '',
        'img': 'https://i.imgur.com/XaMPBEt.png',
        'ex': cc_spheal_sanctuary_ex,
        'paths': [None, None, CC_A_FROZEN_RESPITE, None],
        'actions': ['ladder'],
    }

    # A Frozen Respite
    async def cc_a_frozen_respite_ex(handler, arg):
        pass

    ow[CC_A_FROZEN_RESPITE] = {
        'name': 'A Frozen Respite',
        'desc': '',
        'img': 'https://i.imgur.com/amXADS6.png',
        'ex': cc_a_frozen_respite_ex,
        'paths': [CC_SPHEAL_SANCTUARY, None, None, None],
        #'actions': [''],
    }







    # Snow's Secret
    async def cc_snows_secret_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(CC_VANILLITE_STALAGMITES)
            return True

    ow[CC_SNOWS_SECRET] = {
        'name': 'Snow\'s Secret',
        'desc': '',
        'img': 'https://i.imgur.com/jQVlhqS.png',
        'ex': cc_snows_secret_ex,
        'actions': ['ladder'],
    }






    r5map = [[CC_FROSTY_SLIDE, CC_LAST_STRETCH],
             [CC_NORTH_FACE, CC_CHRISTMAS_ENTRANCE]]

    # Frosty Slide
    async def cc_frosty_slide_ex(handler, arg):
        pass

    ow[CC_FROSTY_SLIDE] = {
        'name': 'Frosty Slide',
        'desc': '',
        'img': 'https://i.imgur.com/kAzwz3T.png',
        'ex': cc_frosty_slide_ex,
        'map': r5map,
        #'actions': [''],
    }

    # Last Stretch
    async def cc_last_stretch_ex(handler, arg):
        pass

    ow[CC_LAST_STRETCH] = {
        'name': 'Last Stretch',
        'desc': '',
        'img': 'https://i.imgur.com/KZIR4ag.png',
        'ex': cc_last_stretch_ex,
        'map': r5map,
        #'actions': [''],
    }

    # North Face
    async def cc_north_face_ex(handler, arg):
        if 'ladder' in arg:
            await handler.move_to(CC_VANILLITE_STALAGMITES)
            return True

    ow[CC_NORTH_FACE] = {
        'name': 'North Face',
        'desc': '',
        'img': 'https://i.imgur.com/2pdXUnB.png',
        'ex': cc_north_face_ex,
        'map': r5map,
        'blocked': [E],
        'actions': ['ladder'],
    }

    # Christmas Entrance
    async def cc_christmas_entrance_ex(handler, arg):
        pass

    ow[CC_CHRISTMAS_ENTRANCE] = {
        'name': 'Christmas Entrance',
        'desc': '',
        'img': 'https://i.imgur.com/EGzY0zi.png',
        'ex': cc_christmas_entrance_ex,
        'map': r5map,
        'blocked': [W],
        #'actions': [''],
    }
from common import *
from . import cinnasea, seacrevice

ID = 14

SF_WEST_CAVERN = 1400
SF_GYM_TUNNEL = 1401
SF_EAST_CAVERN = 1402
SF_LAPRAS_DEN = 1403
SF_CHANNEL = 1404
SF_ALGAE_FARM = 1405

def setup(areas, ow):
    areas[ID] = {
        'name': 'Sea Floor',
        'emoji': '',
        'dialog': '',
        'map': [[SF_WEST_CAVERN, SF_GYM_TUNNEL, SF_EAST_CAVERN],
                [SF_LAPRAS_DEN, SF_CHANNEL, SF_ALGAE_FARM]]
    }


    # West Cavern
    async def sf_west_cavern_ex(handler, arg):
        if arg == 'cavern':
            await handler.move_to(seacrevice.SFC_SEA_PASSAGE_W)
            return True

    ow[SF_WEST_CAVERN] = {
        'name': 'West Cavern',
        'desc': '',
        'img': 'https://i.imgur.com/54xhOqu.png',
        'ex': sf_west_cavern_ex,
        'actions': ['cavern'],
    }

    # Gym Tunnel
    async def sf_gym_tunnel_ex(handler, arg):
        pass

    ow[SF_GYM_TUNNEL] = {
        'name': 'Gym Tunnel',
        'desc': '',
        'img': 'https://i.imgur.com/3wWp1AE.png',
        'ex': sf_gym_tunnel_ex,
        'actions': ['tunnel'],
    }

    # East Cavern
    async def sf_east_cavern_ex(handler, arg):

        if arg == 'cavern':
            await handler.move_to(seacrevice.SFC_SEA_PASSAGE_E)
            return True

        if 'lapras' in arg:
            #todo fix
            dex = handler.dex_entry('Blastoise')
            await handler.show_dialog('Lapras', f'Follow the Lapras to the surface?{DBL_BREAK}※  `yes` or `no`', color=TYPE_COLORS[dex['type']], image=dex['gif'], thumb=True)
            return True

        if arg == 'no':
            await handler.show_location()
            return True

        if arg == 'yes':
            await handler.move_to(cinnasea.CS_ROCKLINE)
            return True

    ow[SF_EAST_CAVERN] = {
        'name': 'East Cavern',
        'desc': '',
        'img': 'https://i.imgur.com/G7565sP.png',
        'ex': sf_east_cavern_ex,
        'actions': ['lapras', 'cavern'],
    }

    # Lapras Den
    async def sf_lapras_den_ex(handler, arg):
        pass

    ow[SF_LAPRAS_DEN] = {
        'name': 'Lapras Den',
        'desc': '',
        'img': 'https://i.imgur.com/FX82vbu.png',
        'ex': sf_lapras_den_ex,
        #'actions': [''],
    }

    # Channel
    async def sf_channel_ex(handler, arg):
        pass

    ow[SF_CHANNEL] = {
        'name': 'Channel',
        'desc': '',
        'img': 'https://i.imgur.com/yE1HEVH.png',
        'ex': sf_channel_ex,
        #'actions': [''],
    }

    # Algae Farm
    async def sf_algae_farm_ex(handler, arg):
        pass

    ow[SF_ALGAE_FARM] = {
        'name': 'Algae Farm',
        'desc': '',
        'img': 'https://i.imgur.com/LyEyqIv.png',
        'ex': sf_algae_farm_ex,
        #'actions': [''],
    }
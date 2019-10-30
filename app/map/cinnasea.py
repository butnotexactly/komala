from common import *
from . import seafloor

ID = 13

CS_SHORE = 1300
CS_ROCKLINE = 1301

def setup(areas, ow):
    areas[ID] = {
        'name': 'Cinnabar Sea',
        'emoji': '<:lap:414510862540341269>',
        'dialog': '',
        'map': [[CS_SHORE],
                [CS_ROCKLINE]]
    }

    # Shore
    async def cs_shore_ex(handler, arg):
        pass

    ow[CS_SHORE] = {
        'name': 'Shore',
        'desc': '',
        'img': 'https://i.imgur.com/ZD2OckJ.png',
        'ex': cs_shore_ex,
        #'actions': [''],
    }

    # Rockline
    async def cs_rockline_ex(handler, arg):

        if 'lapras' in arg:
            #todo fix
            dex = handler.dex_entry('Blastoise')
            await handler.show_dialog('Lapras', f'Follow the Lapras to the seafloor?{DBL_BREAK}※  `yes` or `no`', color=TYPE_COLORS[dex['type']], image=dex['gif'], thumb=True)
            return True

        if arg == 'no':
            await handler.show_location()
            return True

        if arg == 'yes':
            await handler.move_to(seafloor.SF_EAST_CAVERN)
            return True


    ow[CS_ROCKLINE] = {
        'name': 'Rockline',
        'desc': '',
        'img': 'https://i.imgur.com/SI3UGfQ.png',
        'ex': cs_rockline_ex,
        'actions': ['lapras'],
    }
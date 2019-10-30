from common import *
from . import sepia

ID = 46

SCG_SECOND_FLOOR = 4600
SCG_FIRST_FLOOR = 4601

def setup(areas, ow):
    areas[ID] = {
        'name': 'Sepia City Gym',
        'emoji': '',
        'dialog': '',
        'map': [[SCG_SECOND_FLOOR],
                [SCG_FIRST_FLOOR]]
    }


    # Second Floor
    async def scg_second_floor_ex(handler, arg):
        pass

    ow[SCG_SECOND_FLOOR] = {
        'name': 'Clocktower 2F',
        'desc': '',
        'img': 'https://i.imgur.com/OUH8FE3.png',
        'ex': scg_second_floor_ex,
        'actions': ['acerola'],
    }

    # First Floor
    async def scg_first_floor_ex(handler, arg):
        if arg == 'exit':
            await handler.move_to(sepia.SC_MINE_ENTRANCE)
            return True

    ow[SCG_FIRST_FLOOR] = {
        'name': 'Clocktower 1F',
        'desc': '',
        'img': 'https://i.imgur.com/JXMgx6A.png',
        'ex': scg_first_floor_ex,
        'paths': [None, None, sepia.SC_MINE_ENTRANCE, None],
        'actions': ['lydia', 'bo', 'mortimer', 'wednesday'],
    }
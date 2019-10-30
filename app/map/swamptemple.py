from common import *
from . import lostvillage

ID = 10
PREFIX = 'ST'

ST_CLASS_S = 1000
ST_LEADER = 1001
ST_CLASS_A = 1002
ST_CLASS_B = 1003
ST_ANTEROOM = 1004
ST_CLASS_C = 1005

def setup(areas, ow):
    areas[ID] = {
        'name': 'Swamp Temple',
        'emoji': '',
        'dialog': '',
        'map': [[ST_CLASS_S, ST_LEADER],
                [ST_CLASS_A, ST_CLASS_B],
                [ST_ANTEROOM, ST_CLASS_C]]
    }


    # Class S
    async def st_class_s_ex(handler, arg):
        pass

    ow[ST_CLASS_S] = {
        'name': 'Class S',
        'desc': '',
        'img': 'https://i.imgur.com/uNNPHos.png',
        'ex': st_class_s_ex,
        #'actions': [''],
    }

    # Leader
    async def st_leader_ex(handler, arg):
        pass

    ow[ST_LEADER] = {
        'name': 'Leader',
        'desc': '',
        'img': 'https://i.imgur.com/J7hRLWD.png',
        'ex': st_leader_ex,
        #'actions': [''],
    }

    # Class A
    async def st_class_a_ex(handler, arg):
        pass

    ow[ST_CLASS_A] = {
        'name': 'Bridge',
        'desc': '',
        'img': 'https://i.imgur.com/WfOfhGJ.png',
        'ex': st_class_a_ex,
        'blocked': [S],
        #'actions': [''],
    }

    # Class B
    async def st_class_b_ex(handler, arg):
        pass

    ow[ST_CLASS_B] = {
        'name': 'Class A',
        'desc': '',
        'img': 'https://i.imgur.com/TPAHagd.png',
        'ex': st_class_b_ex,
        'blocked': [N],
        #'actions': [''],
    }

    # Anteroom
    async def st_anteroom_ex(handler, arg):
        pass

    ow[ST_ANTEROOM] = {
        'name': 'Anteroom',
        'desc': '',
        'img': 'https://i.imgur.com/Xq1llpg.png',
        'ex': st_anteroom_ex,
        'blocked': [N],
        'paths': [None, None, lostvillage.LV_TEMPLE_ENTRANCE, None],
        #'actions': [''],
    }

    # Class C
    async def st_class_c_ex(handler, arg):
        pass

    ow[ST_CLASS_C] = {
        'name': 'Class B',
        'desc': '',
        'img': 'https://i.imgur.com/T70jLH9.png',
        'ex': st_class_c_ex,
        #'actions': [''],
    }


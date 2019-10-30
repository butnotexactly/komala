from common import *

ID = 11

PC_DOWNTOWN = 1100
PC_MARKET_STREET = 1101
PC_BOULDER_POINT = 1102
PC_CITY_OUTSKIRTS = 1103
PC_GYM = 1104

def setup(areas, ow):
    areas[ID] = {
        'name': 'Pewter City',
        'emoji': '<:oni:414520573998268418> ',
        'dialog': '',
        'map': [[PC_DOWNTOWN, PC_MARKET_STREET],
            [PC_BOULDER_POINT, PC_CITY_OUTSKIRTS]]
    }


    # Downtown
    async def pc_downtown_ex(handler, arg):
        if arg == 'gym':
            await handler.move_to(PC_GYM)
            return True

    ow[PC_DOWNTOWN] = {
        'name': 'Downtown',
        'desc': '',
        'img': 'https://i.imgur.com/0Kj2Q3N.png',
        'ex': pc_downtown_ex,
        'actions': ['gym'],
    }

    # Market Street
    async def pc_market_street_ex(handler, arg):
        pass

    ow[PC_MARKET_STREET] = {
        'name': 'Market Street',
        'desc': '',
        'img': 'https://i.imgur.com/Zy2fVH6.png',
        'ex': pc_market_street_ex,
        #'actions': [''],
    }

    # Boulder Point
    async def pc_boulder_point_ex(handler, arg):
        pass

    ow[PC_BOULDER_POINT] = {
        'name': 'Boulder Point',
        'desc': '',
        'img': 'https://i.imgur.com/5n5wAbQ.png',
        'ex': pc_boulder_point_ex,
        #'actions': [''],
    }

    # City Outskirts
    async def pc_city_outskirts_ex(handler, arg):
        pass

    ow[PC_CITY_OUTSKIRTS] = {
        'name': 'City Outskirts',
        'desc': '',
        'img': 'https://i.imgur.com/OEjOBkz.png',
        'ex': pc_city_outskirts_ex,
        #'actions': [''],
    }

    # Gym
    async def pc_gym_ex(handler, arg):
        if arg == 'exit':
            await handler.move_to(PC_DOWNTOWN)
            return True

        return False

    ow[PC_GYM] = {
        'name': 'Pewter City Gym',
        'desc': '',
        'img': 'https://i.imgur.com/46NEfwk.png',
        'ex': pc_gym_ex,
        'actions': ['parker', 'lucas', 'russell', 'brock'],
        'paths': [None, None, PC_DOWNTOWN, None],
        #'actions': ['trainee', 'cooltrainer', 'hiker', 'exit'],

    }
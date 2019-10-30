from common import *

ID = 35

MW_TECH_DISTRICT = 3500
MW_CITY_CENTER = 3501
MW_MAREEP_MEADOWS = 3502
MW_CHINCHOU_FALLS = 3503
MW_DOCKS = 3504
MW_CITY_CROSSING = 3505
MW_POWER_PLANT = 3506
MW_CONSTRUCTION_YARD = 3507
MW_CABIN = 3508
MW_FLAAFY_FOREST = 3509

def setup(areas, ow):
    areas[ID] = {
        'name': 'Magnemite Works',
        'emoji': '<:magg:414515644382576640>',
        'dialog': '',
        'map': [[None, MW_TECH_DISTRICT],
            [None, MW_CITY_CENTER, MW_MAREEP_MEADOWS, MW_CHINCHOU_FALLS, MW_DOCKS, MW_CITY_CROSSING],
            [MW_POWER_PLANT, MW_CONSTRUCTION_YARD],
            [MW_CABIN],
            [MW_FLAAFY_FOREST]]
    }


    # Tech District
    async def mw_tech_district_ex(handler, arg):
        pass

    ow[MW_TECH_DISTRICT] = {
        'name': 'Tech District',
        'desc': '',
        'img': 'https://i.imgur.com/f4Jpkkw.png',
        'ex': mw_tech_district_ex,
        #'actions': [''],
    }

    # City Center
    async def mw_city_center_ex(handler, arg):
        pass

    ow[MW_CITY_CENTER] = {
        'name': 'City Center',
        'desc': '',
        'img': 'https://i.imgur.com/1VfXHI0.png',
        'ex': mw_city_center_ex,
        #'actions': [''],
    }

    # Mareep Meadows
    async def mw_mareep_meadows_ex(handler, arg):
        pass

    ow[MW_MAREEP_MEADOWS] = {
        'name': 'Mareep Meadows',
        'desc': '',
        'img': 'https://i.imgur.com/C1j9IFJ.png',
        'ex': mw_mareep_meadows_ex,
        #'actions': [''],
    }

    # Chinchou Falls
    async def mw_chinchou_falls_ex(handler, arg):
        pass

    ow[MW_CHINCHOU_FALLS] = {
        'name': 'Chinchou Falls',
        'desc': '',
        'img': 'https://i.imgur.com/r06OP4C.png',
        'ex': mw_chinchou_falls_ex,
        #'actions': [''],
    }

    # Docks
    async def mw_docks_ex(handler, arg):
        pass

    ow[MW_DOCKS] = {
        'name': 'Docks',
        'desc': '',
        'img': 'https://i.imgur.com/hyUcsGm.png',
        'ex': mw_docks_ex,
        #'actions': [''],
    }

    # City Crossing
    async def mw_city_crossing_ex(handler, arg):
        pass

    ow[MW_CITY_CROSSING] = {
        'name': 'City Crossing',
        'desc': '',
        'img': 'https://i.imgur.com/BF0CgUs.png',
        'ex': mw_city_crossing_ex,
        #'actions': [''],
    }

    # Power Plant
    async def mw_power_plant_ex(handler, arg):
        pass

    ow[MW_POWER_PLANT] = {
        'name': 'Power Plant',
        'desc': '',
        'img': 'https://i.imgur.com/23A73zw.png',
        'ex': mw_power_plant_ex,
        #'actions': [''],
    }

    # Construction Yard
    async def mw_construction_yard_ex(handler, arg):
        pass

    ow[MW_CONSTRUCTION_YARD] = {
        'name': 'Construction Yard',
        'desc': '',
        'img': 'https://i.imgur.com/8JOtZZr.png',
        'ex': mw_construction_yard_ex,
        #'actions': [''],
    }

    # Cabin
    async def mw_cabin_ex(handler, arg):
        pass

    ow[MW_CABIN] = {
        'name': '???\'s Cabin',
        'desc': '',
        'img': 'https://i.imgur.com/xC2ez8J.png',
        'ex': mw_cabin_ex,
        #'actions': [''],
    }

    # Flaafy Forest
    async def mw_flaafy_forest_ex(handler, arg):
        pass

    ow[MW_FLAAFY_FOREST] = {
        'name': 'Flaafy Forest',
        'desc': '',
        'img': 'https://i.imgur.com/mINXqJc.png',
        'ex': mw_flaafy_forest_ex,
        #'actions': [''],
    }
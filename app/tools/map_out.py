from common import *

ID = 62

JA_OUTSKIRTS = 6200
JA_POKÉMON_INSTITUTE = 6201
JA_RESIDENCES = 6202
JA_WEST_EXIT = 6203
JA_CITY_FOUNTAIN = 6204
JA_EAST_EXIT = 6205
JA_SIDE_STREET = 6206
JA_MARKET_STREET = 6207
JA_FINANCE_DISTRICT = 6208
JA_BACKALLEY = 6209
JA_SOUTH_EXIT = 6210
JA_???S_HOUSE = 6211

def setup(areas, ow):
    areas[ID] = {
        'name': '',
        'emoji': '',
        'dialog': '',
        'map': [[JA_OUTSKIRTS, JA_POKÉMON_INSTITUTE, JA_RESIDENCES],
			[JA_WEST_EXIT, JA_CITY_FOUNTAIN, JA_EAST_EXIT],
			[JA_SIDE_STREET, JA_MARKET_STREET, JA_FINANCE_DISTRICT],
			[JA_BACKALLEY, JA_SOUTH_EXIT, JA_???S_HOUSE]]
    }


    # Outskirts
    async def ja_outskirts_ex(handler, arg):
        pass

    ow[JA_OUTSKIRTS] = {
        'name': 'Outskirts',
        'desc': '',
        'img': 'https://i.imgur.com/d4GFqf4.png',
        'ex': ja_outskirts_ex,
        #'actions': [''],
    }

    # Pokémon Institute
    async def ja_pokémon_institute_ex(handler, arg):
        pass

    ow[JA_POKÉMON_INSTITUTE] = {
        'name': 'Pokémon Institute',
        'desc': '',
        'img': 'https://i.imgur.com/7uExDn3.png',
        'ex': ja_pokémon_institute_ex,
        #'actions': [''],
    }

    # Residences
    async def ja_residences_ex(handler, arg):
        pass

    ow[JA_RESIDENCES] = {
        'name': 'Residences',
        'desc': '',
        'img': 'https://i.imgur.com/r7Tx9wB.png',
        'ex': ja_residences_ex,
        #'actions': [''],
    }

    # West Exit
    async def ja_west_exit_ex(handler, arg):
        pass

    ow[JA_WEST_EXIT] = {
        'name': 'West Exit',
        'desc': '',
        'img': 'https://i.imgur.com/CEyaGQh.png',
        'ex': ja_west_exit_ex,
        #'actions': [''],
    }

    # City Fountain
    async def ja_city_fountain_ex(handler, arg):
        pass

    ow[JA_CITY_FOUNTAIN] = {
        'name': 'City Fountain',
        'desc': '',
        'img': 'https://i.imgur.com/fAnatKp.png',
        'ex': ja_city_fountain_ex,
        #'actions': [''],
    }

    # East Exit
    async def ja_east_exit_ex(handler, arg):
        pass

    ow[JA_EAST_EXIT] = {
        'name': 'East Exit',
        'desc': '',
        'img': 'https://i.imgur.com/htK7JKr.png',
        'ex': ja_east_exit_ex,
        #'actions': [''],
    }

    # Side Street
    async def ja_side_street_ex(handler, arg):
        pass

    ow[JA_SIDE_STREET] = {
        'name': 'Side Street',
        'desc': '',
        'img': 'https://i.imgur.com/3MSAVaJ.png',
        'ex': ja_side_street_ex,
        #'actions': [''],
    }

    # Market Street
    async def ja_market_street_ex(handler, arg):
        pass

    ow[JA_MARKET_STREET] = {
        'name': 'Market Street',
        'desc': '',
        'img': 'https://i.imgur.com/rbeXeBd.png',
        'ex': ja_market_street_ex,
        #'actions': [''],
    }

    # Finance District
    async def ja_finance_district_ex(handler, arg):
        pass

    ow[JA_FINANCE_DISTRICT] = {
        'name': 'Finance District',
        'desc': '',
        'img': 'https://i.imgur.com/RVJuevZ.png',
        'ex': ja_finance_district_ex,
        #'actions': [''],
    }

    # Backalley
    async def ja_backalley_ex(handler, arg):
        pass

    ow[JA_BACKALLEY] = {
        'name': 'Backalley',
        'desc': '',
        'img': 'https://i.imgur.com/MvNpcAn.png',
        'ex': ja_backalley_ex,
        #'actions': [''],
    }

    # South Exit
    async def ja_south_exit_ex(handler, arg):
        pass

    ow[JA_SOUTH_EXIT] = {
        'name': 'South Exit',
        'desc': '',
        'img': 'https://i.imgur.com/MrPG6lR.png',
        'ex': ja_south_exit_ex,
        #'actions': [''],
    }

    # ???'s House
    async def ja_???s_house_ex(handler, arg):
        pass

    ow[JA_???S_HOUSE] = {
        'name': '???'s House',
        'desc': '',
        'img': 'https://i.imgur.com/vpwO1HM.png',
        'ex': ja_???s_house_ex,
        #'actions': [''],
    }
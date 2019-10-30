from common import *

ID = 62

EC_OUTSKIRTS = 6200
EC_POKEMON_INSTITUTE = 6201
EC_RESIDENCES = 6202
EC_WEST_EXIT = 6203
EC_CITY_FOUNTAIN = 6204
EC_EAST_EXIT = 6205
EC_SIDE_STREET = 6206
EC_MARKET_STREET = 6207
EC_FINANCE_DISTRICT = 6208
EC_BACKALLEY = 6209
EC_SOUTH_EXIT = 6210
EC_HOUSE = 6211

def setup(areas, ow):
    areas[ID] = {
        'name': 'Erudite City',
        'emoji': '<:artt:414524337488527360>',
        'dialog': '',
        'map': [[EC_OUTSKIRTS, EC_POKEMON_INSTITUTE, EC_RESIDENCES],
            [EC_WEST_EXIT, EC_CITY_FOUNTAIN, EC_EAST_EXIT],
            [EC_SIDE_STREET, EC_MARKET_STREET, EC_FINANCE_DISTRICT],
            [EC_BACKALLEY, EC_SOUTH_EXIT, EC_HOUSE]]
    }


    # Outskirts
    async def ec_outskirts_ex(handler, arg):
        pass

    ow[EC_OUTSKIRTS] = {
        'name': 'Outskirts',
        'desc': '',
        'img': 'https://i.imgur.com/d4GFqf4.png',
        'blocked': [E],
        'ex': ec_outskirts_ex,
        #'actions': [''],
    }

    # Pokémon Institute
    async def ec_pokemon_institute_ex(handler, arg):
        pass

    ow[EC_POKEMON_INSTITUTE] = {
        'name': 'Pokémon Institute',
        'desc': '',
        'img': 'https://i.imgur.com/7uExDn3.png',
        'blocked': [E, W],
        'ex': ec_pokemon_institute_ex,
        #'actions': [''],
    }

    # Residences
    async def ec_residences_ex(handler, arg):
        pass

    ow[EC_RESIDENCES] = {
        'name': 'Residences',
        'desc': '',
        'img': 'https://i.imgur.com/r7Tx9wB.png',
        'blocked': [W],
        'ex': ec_residences_ex,
        #'actions': [''],
    }

    # West Exit
    async def ec_west_exit_ex(handler, arg):
        pass

    ow[EC_WEST_EXIT] = {
        'name': 'West Exit',
        'desc': '',
        'img': 'https://i.imgur.com/CEyaGQh.png',
        'ex': ec_west_exit_ex,
        #'actions': [''],
    }

    # City Fountain
    async def ec_city_fountain_ex(handler, arg):
        pass

    ow[EC_CITY_FOUNTAIN] = {
        'name': 'City Fountain',
        'desc': '',
        'img': 'https://i.imgur.com/fAnatKp.png',
        'ex': ec_city_fountain_ex,
        #'actions': [''],
    }

    # East Exit
    async def ec_east_exit_ex(handler, arg):
        pass

    ow[EC_EAST_EXIT] = {
        'name': 'East Exit',
        'desc': '',
        'img': 'https://i.imgur.com/htK7JKr.png',
        'ex': ec_east_exit_ex,
        #'actions': [''],
    }

    # Side Street
    async def ec_side_street_ex(handler, arg):
        pass

    ow[EC_SIDE_STREET] = {
        'name': 'Side Street',
        'desc': '',
        'img': 'https://i.imgur.com/3MSAVaJ.png',
        'ex': ec_side_street_ex,
        #'actions': [''],
    }

    # Market Street
    async def ec_market_street_ex(handler, arg):
        pass

    ow[EC_MARKET_STREET] = {
        'name': 'Market Street',
        'desc': '',
        'img': 'https://i.imgur.com/rbeXeBd.png',
        'ex': ec_market_street_ex,
        #'actions': [''],
    }

    # Finance District
    async def ec_finance_district_ex(handler, arg):
        pass

    ow[EC_FINANCE_DISTRICT] = {
        'name': 'Finance District',
        'desc': '',
        'img': 'https://i.imgur.com/RVJuevZ.png',
        'ex': ec_finance_district_ex,
        #'actions': [''],
    }

    # Backalley
    async def ec_backalley_ex(handler, arg):
        pass

    ow[EC_BACKALLEY] = {
        'name': 'Backalley',
        'desc': '',
        'img': 'https://i.imgur.com/MvNpcAn.png',
        'ex': ec_backalley_ex,
        #'actions': [''],
    }

    # South Exit
    async def ec_south_exit_ex(handler, arg):
        pass

    ow[EC_SOUTH_EXIT] = {
        'name': 'South Exit',
        'desc': '',
        'img': 'https://i.imgur.com/MrPG6lR.png',
        'blocked': [E],
        'ex': ec_south_exit_ex,
        #'actions': [''],
    }

    # ???'s House
    async def ec_house_ex(handler, arg):
        pass

    ow[EC_HOUSE] = {
        'name': '???\'s House',
        'desc': '',
        'img': 'https://i.imgur.com/vpwO1HM.png',
        'blocked': [W],
        'ex': ec_house_ex,
        #'actions': [''],
    }
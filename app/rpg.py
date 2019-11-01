import time
import pytz
import importlib
import random
import re
import numpy as np

from datetime import datetime
from enum import IntFlag

from common import *
from map import *

compass = ('n', 'e', 's', 'w')
arrows = ('↑', '→', '↓', '←')

ow = {}
areas = {}
bridges = {}

RPG_NO_POKEMON = 'You don\'t have a Pokémon equipped in that slot. Check your `.party` or `.equip` one!'

'''
store thing whenever someone does .x with time
only react to n e s w if thing is stored + time is recent
'''

class RpgState(object):
    def __init__(self, uid):
        self.uid = uid
        self.location = pallet.PAL_PALLET_TOWN
        self.items = None
        self.flags = IntFlag(0)
        self.progress = {}
        self.roomdata = None
        self.name = None

    def __repr__(self):
        return ''

class RpgHandler(object):
    def __init__(self, bot, state, ctx=None):
        #self.state = self.get_rpg_state(uid)
        self.bot = bot
        self.state = state
        self.ctx = ctx
        self.message = None
        self.embed = None
        #self.raids = self.get_raid_data()

    def name(self):
        return self.ctx.author.name

    async def handle_message(self, message):
        if message.content.startswith((',', '.', ';', '!')):
            return
        await self.run(message.content.lower().strip(), message)

    async def run(self, cmd, message=None, arg=''):
        if cmd in compass:
            direction = compass.index(cmd)
            result = await self.move_directional(direction)
            #if result:
            await message.delete()
            return result
            # else:
            #     self.message = None
            # return result

        self.message = None
        if cmd == 'x':
            #await message.delete()
            await self.show_location()
            return True

        areaId = self.state.location // 100
        area = areas[areaId]

        #m = get_module(areaId)
        #ex = f'''{m.PREFIX.lower()}_{fmt(ow[self.state.location]['name'], -1)}_ex'''
        # if getattr(m, ex)(cmd):
        #     return True

        room = ow[self.state.location]

        if cmd in ('ex', 'explore'):
            if 'wilds' in room:
                if room['wilds']:
                    await self.engage_one(room['wilds'])
                    return
            elif 'wilds' in area:
                await self.engage_one(area['wilds'])
                return


            await send_message(self.ctx, 'Not a wild Pokémon in sight...')
            return

        if 'ex' in room:
            result = await room['ex'](self, cmd)
            if not result:
                self.message = None
            return result

    async def move_to(self, location, edit=False):
        # if not edit:
        #     self.message = None
        self.state.roomdata = None
        self.state.location = location
        await self.show_location()
        #self.save(True)
        return True

    async def move_directional(self, direction):
        room = ow[self.state.location]
        area = areas[self.state.location // 100]

        to = get_adjacent_location(self.state.location, direction, area)
        if to is None:
            print('There\'s no path that way...')
            return False

        if 'move' in room:
            if not await room['move'](self, direction):
                return False



        # if area['paths'][direction] is not None:
        #     # if 'move' in area:
        #     #     if not area['move'](self, fromLocation, direction):
        #     #         return False

        #     hidden = area['hidepaths'] if 'hidepaths' in area else []
        #     if direction in hidden:
        #         delete_input()

        #     return self.move_to(area['paths'][direction])
        await self.move_to(to, edit=True)
        return True


    async def show_location(self, location=None):
        if location is None:
            location = self.state.location

        area = areas[location // 100]
        room = ow[location]
        hidden = room['hidden'] if 'hidden' in room else []


        #print(room)

        '''
        if 'secret' in area:
            mark_secret()

        hangars = [TT_FIFTH_DISTRICT, TW_TRAM_COMMON]
        flags = [Flags.HANGAR_TT, Flags.HANGAR_TW]
        if location in hangars:
            i = hangars.index(location)
            if not self.has_flag(flags[i]):
                self.set_flag(flags[i])
                self.save(True)
                #content = json.dumps({'description': '[🛩] You unlocked this world's Gummi Hangar! You can now visit it using `.x gummi`'})
                #client.Messaging.MessageChannel(id=client.context.channelId, format='discord.embed', content=content)
                client.Messaging.MessageChannel(id=client.context.channelId, format='raw', content='[🛩] You unlocked this world's Gummi Hangar! You can now visit it using `.x gummi`')

        raidLocations = [raid[0] for raid in self.raids]
        fastestDirection = None
        raidPortal = None

        if not location in raidLocations:
            shortestDistance = 1000
            w1 = area['world']
            for loc in raidLocations:
                if loc == -1:
                    continue
                w2 = ow[loc]['world']
                if w1 == w2:
                    alternateGoal = None
                else:
                    if w1 == W_TRAVERSE_TOWN:
                        # destination world etc
                        alternateGoal = TT_CENTRAL_STATION
                    elif w1 == W_TWILIGHT_TOWN:
                        alternateGoal = TW_CENTRAL_STATION
                    elif w1 == W_WONDERLAND:
                        alternateGoal = None

                bfsPaths = [bfs_shortest_path(graph, area['paths'][i], loc, alternateGoal) for i in range(4)]
                distances = [len(path) if path else 1000 for path in bfsPaths]

                if min(distances) < shortestDistance or (raidPortal and not alternateGoal):
                    raidPortal = alternateGoal
                    shortestDistance = min(distances)
                    fastestDirection = distances.index(shortestDistance)

        if location == raidPortal:
            fastestDirection = None
        '''

        description = f'''{area['emoji']}{area['name']}\n \n{room['desc']}'''
        if area['name'] == room['name']:
            footer = f'''{area['name']} {pretty_date()}'''
        else:
            footer = f'''{area['name']} • {room['name'].strip(' 🚆')} {pretty_date()}'''

        self.embed = discord.Embed(description=description, title=room['name']) \
                .set_image(url=room['img']).set_footer(text=footer)

        if 'color' in area:
            self.embed.color = area['color']

        paths = []
        for i in range(4):
            to = get_adjacent_location(self.state.location, i, area)
            if to is not None and not i in hidden:
                if to // 100 == self.state.location // 100:
                    paths.append(f'''`{compass[i]}`  {arrows[i]}  _{ow[to]['name']}_''')
                else:
                    toWorld = f'''{areas[to // 100]['emoji']}{areas[to // 100]['name']}'''
                    paths.append(f'''`{compass[i]}`  {arrows[i]}  _{ow[to]['name']}_ {toWorld}''')

        if paths:
            self.embed.add_field(name='Paths', value='\n'.join(paths), inline=True)

        # todo change actions based on state / roomdata
        actions = [] if 'wilds' not in room and 'wilds' not in area else ['`explore` / `ex`']
        if 'actions' in room:
            actions += [f'`{action}`' for action in room['actions']]

        if 'trainers' in room:
            actions.append('  '.join(f'`{trainer}`' for trainer in room['trainers']))

        # if 'unlocked_actions' in room:
        #     unlocked = room['unlocked_actions'](self)
        #     if unlocked: actions += unlocked

        #f'`{action}`' for action in actions

        # wNpcs = self.wandering_npcs_in_location(self.state.world, location)
        # actions += wNpcs

        if actions:
            self.embed.add_field(name='Actions', value='\n'.join(actions), inline=True)

        # if location == raidPortal:
        #     actions[area['portal'].index(w2)] += '[r]'


        # if actions:
        #     actionLines = []
        #     for action in actions:
        #         if action.endswith('[r]'):
        #             if action == 'raid[r]':
        #                 index = raidLocations.index(self.state.location)
        #                 location, raidType, level, drop = self.raids[index]

        #                 actionLines.append('`.x {}`  {}\n_{}_'.format(action[:-3], emojis['raid'], raid.BOSS_NAMES[raidType]))
        #             else:
        #                 actionLines.append('`.x {}`  {}'.format(action[:-3], emojis['raid']))
        #         else:
        #             actionLines.append('`.x {}`'.format(action))

        #     fields.append({
        #         'name': 'Actions',
        #         'value': '\n'.join(actionLines),
        #         'inline': True
        #     })

        if self.message:
            await self.message.edit(embed=self.embed)
        else:
            self.message = await self.ctx.send(f'<@{self.state.uid}>', embed=self.embed)

    async def engage_one(self, pool):
        p = [pkmn[3] / 100 for pkmn in pool]
        i, = np.random.choice(len(pool), 1, p=p)
        name = pool[i][0]
        try:
            rarity = pool[i][4]
        except IndexError:
            rarity = AVERAGE
        lv = random.randint(pool[i][1], pool[i][2])
        await self.bot.explore.engage(self.ctx, self.state.location, name, lv, rarity)
        return True

    async def parse_pkmn_action(self, arg):
        m = re.match(r'([1-6])\b(.+)', arg)
        if not m:
            return None

        slot = int(m.group(1)) - 1
        target = m.group(2)
        deck, party = self.bot.party.load_active_party(self.state.uid)

        if not party[slot]:
            await send_message(self.ctx, RPG_NO_POKEMON, error=True)
            return -1

        return party[slot], party, slot, target

    async def fly(self, arg):
        try:
            location = int(arg)
            if location < 100:
                location *= 100
            await self.move_to(location)
        except ValueError:
            pass

    async def show_dialog(self, name, text, image='default', thumb=True, color=None, footer='', ping=True, tips=False):
        if image == 'default':
            image = 'https://i.imgur.com/FjwhR2T.png'

        if not color:
            #color=0xFFB98A
            color = random.choice(TYPE_COLORS)

        e = discord.Embed(title=name, description=text, color=color) \
            .set_footer(text=footer)

        if image:
            if thumb:
                e.set_thumbnail(url=image)
            else:
                e.set_image(url=image)

        # if thumb
        #.set_image(url=image) \
        message = await self.ctx.send(f'<@{self.state.uid}>' if ping else '', embed=e)

    def dex_entry(self, name):
        return self.bot.dex.pkmn[self.bot.dex.nos[name]]

class RpgFlags(IntFlag):
    CID_SHOP_PRIZE = 1 << 1

def pretty_date():
    clocks = '🕛🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚'
    timestamp = datetime.now(pytz.timezone('US/Eastern'))
    hour = timestamp.strftime('%I %p, %A')
    if hour.startswith('0'):
        hour = hour[1:]

    return '{} {}'.format(clocks[timestamp.hour % 12], hour)

def get_xy(location, m):
    for y, row in enumerate(m):
        if location in row:
            return row.index(location), y

def get_adjacent_location(location, direction, area):

    try:
        if direction in ow[location]['blocked']:
            return None
    except KeyError:
        pass

    try:
        if bridges[location][direction] is not None:
            return bridges[location][direction]
    except KeyError:
        pass

    if 'paths' in ow[location]:
        if ow[location]['paths'][direction] is not None:
            return ow[location]['paths'][direction]

    if 'map' in ow[location]:
        m = ow[location]['map']
    elif 'map' in area:
        m = area['map']
    else:
        return None

    location = get_xy(location, m)
    if location is None:
        return None
    x, y = location
    try:
        if direction == N and y > 0:
            to = m[y-1][x]
        elif direction == S:
            to = m[y+1][x]
        elif direction == E:
            to = m[y][x+1]
        elif direction == W and x > 0:
            to = m[y][x-1]
        else:
            raise IndexError
    except IndexError:
        return None

    return to

class Rpg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = {}

    @commands.command(name='ow', aliases=['x', 'map', 'rpg'])
    async def view_ow(self, ctx, *, arg=''):
        await self.play(ctx)

    @commands.command()
    async def fly(self, ctx, *, arg=''):
        await self.play(ctx, showLocation=False)
        await self.bot.wfm[ctx.author.id]['handler'].fly(arg)

    async def play(self, ctx, showLocation=True):
        if not ctx.author.id in self.cache:
            self.cache[ctx.author.id] = RpgState(ctx.author.id)

        handler = RpgHandler(self.bot, self.cache[ctx.author.id], ctx)
        self.bot.wfm[ctx.author.id] = {
            'handler': handler,
            'channel': ctx.channel,
            'expires': time.time() + 20 * 60
        }
        if showLocation:
            await handler.show_location()

        return handler

    @commands.command()
    async def dexg(self, ctx, *, arg=''):
        log = []
        for location, room in ow.items():
            if 'wilds' in room:
                if room['wilds']:
                    for pkmn in room['wilds']:
                        name = pkmn[0]
                        try:
                            no = self.bot.dex.nos[name]
                        except KeyError:
                            log.append(name)

        for area in areas.values():
            if 'wilds' in area:
                for pkmn in area['wilds']:
                    name = pkmn[0]
                    try:
                        no = self.bot.dex.nos[name]
                    except KeyError:
                        log.append(name)


        await send_message(ctx, 'Missing data for:\n\n' + '\n'.join(set(log)))


def setup(bot):
    rpg = Rpg(bot)
    bot.add_cog(rpg)
    bot.rpg = rpg

def add_bridge(bridges, a, b, direction):
    if not a in bridges:
        bridges[a] = [None, None, None, None]
    if not b in bridges:
        bridges[b] = [None, None, None, None]

    reverse = (direction + 2) % 4
    bridges[a][direction] = b
    bridges[b][reverse] = a

modules = [
    pallet,
    pikipek,
    viridian,
    lotadlake,
    sleepy,
    fairypass,
    thicket,
    swamp,
    lostvillage,
    swamptemple,
    skycity,
    works,

    pewter,
    pewtertrail,
    cubchoo,
    christmas,
    iceshaft,
    shiver,
    mtshaft,
    wishmt,
    sepia,
    clocktower,
    monomines,
    wildwood,
    darkforest,
    city,

    cinnasea,
    seafloor,
    seacrevice,
    coastwalk,
    montmartre,
]

def get_module(id):
    for m in modules:
        if m.ID == id:
            return m

def fmt(text, case=0, prefix=None):
    if not text:
        return 'None'

    s = '' if not prefix else prefix + '_'
    text = text.replace(r'[\.\']', '').replace(' ', '_')

    if not case:
        return s + text
    if case > 0:
        return s + text.upper()
    return s + text.lower()

for m in modules:
    importlib.reload(m) # [DEBUG]
    m.setup(areas, ow)

add_bridge(bridges, pallet.PAL_PALLET_TOWN, pikipek.PIKI_SOUTH, N)
add_bridge(bridges, pikipek.PIKI_NORTH, viridian.VIR_POND, N)
add_bridge(bridges, viridian.VIR_CROSSING, lotadlake.LL_ENTRANCE_EAST, W)
add_bridge(bridges, lotadlake.LL_ENTRANCE_SOUTH, sleepy.SS_PALM_TREES, S)
add_bridge(bridges, lotadlake.LL_WARDENS_HOME, fairypass.FP_FAIRY_BRIDGE, W)
add_bridge(bridges, viridian.VIR_CROSSING, thicket.TT_TRAIL_FORK, N)
add_bridge(bridges, thicket.TT_TRAILS_END, pewter.PC_BOULDER_POINT, N)


add_bridge(bridges, swamp.MS_OFF_THE_BEATEN_PATH, lostvillage.LV_VILLAGE_ENTRANCE, E)
bridges[swamp.MS_BOARDWALK_BOG] = [None, None, thicket.TT_SWAMP_EDGE, None]

# Southern Ocean
add_bridge(bridges, pallet.PAL_PALLET_TOWN, cinnasea.CS_SHORE, S)
add_bridge(bridges, coastwalk.CW_LUSH_TRAIL, montmartre.MM_CITY_OF_DRAGONS, W)


# Northern Hike
add_bridge(bridges, pewter.PC_CITY_OUTSKIRTS, pewtertrail.PT_HIKE_START, E)
add_bridge(bridges, pewtertrail.PT_FIRST_SNOW, cubchoo.CC_PEWTER_ENTRANCE, N)
add_bridge(bridges, cubchoo.CC_CHRISTMAS_ENTRANCE, christmas.NCV_WINTER_PARK, S)
bridges[iceshaft.IS_TITANS_DOMAIN] = [None, None, shiver.SC_SNOWY_PASS, None]
#add_bridge(bridges, iceshaft.IS_TITANS_DOMAIN, shiver.SNP_SNOWY_PASS, S)
add_bridge(bridges, shiver.SC_SNOW_VALLEY, mtshaft.MS_2F, N)
add_bridge(bridges, mtshaft.MS_1F, wishmt.WISH_PEAK, S)
add_bridge(bridges, wishmt.WISH_DESCENT, sepia.SC_WHITEGRASS, S)
add_bridge(bridges, sepia.SC_MINE_ENTRANCE, monomines.MM_WHITEOUT_1F, N)
add_bridge(bridges, monomines.MM_LITWICK_WAXTONE_3F, wildwood.WWP_WILDERNESS, S)
add_bridge(bridges, wildwood.WWP_FEAROW_CAMP, darkforest.DF_FOREST_EDGE, W)


add_bridge(bridges, city.EC_WEST_EXIT, works.MW_CITY_CROSSING, W)
add_bridge(bridges, city.EC_EAST_EXIT, darkforest.DF_CITY_OPENING, E)
add_bridge(bridges, city.EC_SOUTH_EXIT, swamp.MS_CITY_EXIT, S)
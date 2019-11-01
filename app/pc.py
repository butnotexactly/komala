import discord
import random
import math
import gzip
import json
import time
import secrets

import battle

from numpy import interp
from collections import Counter
from common import *

def dump_pcd(badges, compress=True):
    out = json.dumps([p.dump() for p in badges])
    if compress:
        out = gzip.compress(out.encode('utf-8'))
    return out

def load_pcd(pcd, decompress=True):
    inp = gzip.decompress(pcd).decode('utf-8') if decompress else pcd
    return json.loads(inp)

def load_pc_badge(d, dex):
    p = PcEvolution(dex) if 'count' in d else PcPokemon(dex)
    p.__dict__ = d
    p.dex = dex
    return p

class PcBadge(object):
    def __init__(self, dex, no):
        self.no = no
        self.id = None
        self.dex = dex

    def format_name(self, key='name'):
        if hasattr(self, 'nick') and self.nick:
            name = self.nick
        else:
            name = self.dex.pkmn[self.no][key] if self.dex.pkmn[self.no][key] else self.dex.pkmn[self.no]['name']

        if key == 'short':
            name = base_name(name).replace('Alolan ', 'A.')
            name = name[:11]

        # if hasattr(self, 'delta') and self.delta:
        #     name = f'δ{name}' if len(name) < 10 else f'δ {name}'

        return name

    def dex_entry(self):
        return self.dex.pkmn[self.no]

    def dump(self):
        out = copy.copy(self.__dict__)
        del out['dex']
        return out

class PcEvolution(PcBadge):
    def __init__(self, dex, no=None, count=1):
        super(PcEvolution, self).__init__(dex, no)
        self.count = count
        self.ots = None #list

    def __repr__(self):
        name = self.dex.pkmn[self.no]['name']
        return f'{name} #{self.no} [{self.id}] x {self.count}'

class PcPokemon(PcBadge):
    def __init__(self, dex, no=None, lv=5, orbs=0, z=None):
        super(PcPokemon, self).__init__(dex, no)
        # initial values for new pkmn
        self.lv = lv
        self.statLv = lv / 3
        self.exp = 0
        self.z = z
        self.orbs = 5 if self.z else orbs
        self.tm = None
        self.hms = None
        self.tplus = 0
        self.delta = 0
        self.gender = MALE

        # set during capture
        self.ot = None
        self.nature = -1

    def type(self):
        return self.dex.pkmn[self.no]['type']

    def hp(self):
        iv = 0
        ev = 0
        hp = scale_hp(self.statLv, self.dex.pkmn[self.no]['hp'], iv, ev)
        if self.hms:
           hp *= 1 + self.hms.count(HM.HP) * 0.2
        return int(hp)

    def pp(self):
        pp = self.dex.pkmn[self.no]['pp']
        if self.hms:
           pp += self.hms.count(HM.PP) * 2
        return pp

    def attack(self):
        xNature = 1
        iv = 0
        ev = 0
        stat = self.dex.pkmn[self.no]['atk']
        if stat <= 0:
            return 0
        attack = scale_stat(self.statLv, stat, iv, ev, xNature)
        if self.hms:
           attack *= 1 + self.hms.count(HM.ATK) * 0.2
        return int(attack)

    def defense(self):
        xNature = 1
        iv = 0
        ev = 0
        stat = self.dex.pkmn[self.no]['def']
        if stat <= 0:
            return 0
        defense = scale_stat(self.statLv, stat, iv, ev, xNature)
        if self.hms:
           defense *= 1 + self.hms.count(HM.DEF) * 0.2
        return int(defense)

    def crit_rate(self):
        critRate = 0
        if self.hms:
           critRate += self.hms.count(HM.CRIT) * 0.2
        return critRate

    def hm_slots(self):
        if self.no in []:
            return 1
        return [1, 2, 3, 4][self.tier()-1]

    def tier(self):
        return self.dex.pkmn[self.no]['tier'] + self.tplus

    def target(self):
        return self.dex.pkmn[self.no]['target']

    def hms_as_text(self, showBlank=True, addBreak=False):
        slots = self.hm_slots()
        output = ''

        blank = hmBlank if showBlank else ''
        if not self.hms:
            return blank * slots + (' ' if addBreak else '')
        for i in range(slots):
            try:
                output += hmEmoji[self.hms[i]]
            except IndexError:
                output += blank

        return output + (' ' if addBreak else '')

    def is_spare(self):
        return self.tm is None and not self.hms and not self.delta and not self.tplus


    def __repr__(self):
        name = self.dex.pkmn[self.no]['name']
        return f'{name} Lv.{self.lv} #{self.no} [{self.id}] +{self.z}%'

    def offensive_rank(self, slot, slotBoosts, deckBoosts, xSlot=1, vsTotem=False):

        # todo buffs worth double if in deck list

        dexEntry = self.dex.pkmn[self.no]
        if 'fixed_dmg' in dexEntry or self.target() is None:
            return UNRANKED

        xStatus = 1 + sum(dexEntry['status_inflict']) / 3

        xAbility = 1
        if 'condition' in dexEntry:
            tag, value = dexEntry['condition']
            if tag in ['slot', 'moves']:
                if value in ['high', 'more']:
                    xAbility = interp(slot, [0, 4], [dexEntry['x_min'], dexEntry['x_max']])
                elif value in ['low', 'less']:
                    xAbility = interp(slot, [0, 4], [dexEntry['x_max'], dexEntry['x_min']])
                else:
                    xAbility = dexEntry['x_max'] if slot == int(value) - 1 else dexEntry['x_min']
            else:
                xAbility = (dexEntry['x_min'] + dexEntry['x_max']) / 2

        xZ = (1 + self.z/100) if self.z else 1

        boosted = slotBoosts[0] == NORMAL or dexEntry['type'] in slotBoosts
        # extra for buffs
        xSlot = xSlot if boosted else 1
        xSynergy = 1
        if dexEntry['type'] in deckBoosts:
            xSynergy = 1.3

        xBuff = 1
        buffBonus = xDuration = 0
        if 'buff' in dexEntry:
            b = dexEntry['buff']

            buffBonus = battle.TYPE_ATK_BUFFS[max(b.atkBuffs[1:])] * (1.5 if xSynergy > 0 else 1) \
                      + battle.TYPE_ATK_BUFFS[max(b.defDebuffs[1:])] * (1.5 if xSynergy > 0 else 1) \
                      + 0.20 * b.defDebuffs[0] \
                      + 0.20 * b.atkBuffs[0] \

            # print('buffBonus: ', buffBonus,
            #     max(b.atkBuffs[1:]),
            #     max(b.defDebuffs[1:]),
            #     battle.TYPE_ATK_BUFFS[max(b.atkBuffs[1:])] ,
            #     battle.TYPE_ATK_BUFFS[max(b.defDebuffs[1:])] ,
            #     0.20 * b.defDebuffs[0] ,
            #     0.20 * b.atkBuffs[0])

            if all(b.atkBuffs[1:]) or all(b.atkDebuffs[1:]):
                buffBonus *= 1.3

            xDuration = b.duration / 6 if b.duration < 6 else (1.0, 1.5, 1.9, 2.2)[int(b.duration / 6) - 1]
            xBuff = 1 + (buffBonus * xDuration)

        if xBuff > 1:
            xBuff = xBuff * interp(slot, [0, 4], [1.3, 0.8])
        else:
            xBuff = interp(slot, [0, 3], [0.6, 1])

        xTotem = 1
        if vsTotem and self.hms:
            xTotem += self.hms.count(HM.TOTEM) * 0.4

        #x2Multi = 1.25 if AbilityFlag.X2_DMG in abilityFlag else 1



        xTarget = 1.3 if dexEntry['target'] == 1 else 1
        xZBonus = (1 + sum(dexEntry['z_bonus']) / 100) if 'z_bonus' in dexEntry else 1

        # todo HM
        xUses = 1 + (dexEntry['pp'] / dexEntry['pp_cost']) * 0.15



        #total = (self.attack() * xSlot / 4 - 30) * xZ * xAbility * xBuff * xTotem * xStatus * xTarget * xZBonus * xUses # x2Multi
        #total = (self.attack() * xSlot / 4 - 30) * xZ * xAbility * xBuff * xTotem * xStatus * xTarget * xZBonus * xUses # x2Multi

        defense = 50
        base = int((((2 * self.lv/5 + 2) * (battle.ATK_BUFFS[2] * self.attack() * (xSlot * 100) - (defense * 50)) / defense) / 50) +2)

        print(f'''[{dexEntry['name']}] xSlot: {xSlot} Atk: {self.attack()} Base: {base}''')

        print(f'''xZ:{xZ} xAbility:{xAbility} buffBonus:{buffBonus * xDuration} xBuff:{xBuff} xStatus:{xStatus} xZBonus{xZBonus} xTarget{xTarget} xUses{xUses} xSynergy{xSynergy}''')

        return base * xZ * xAbility * xBuff * xTotem * xStatus * xTarget * xZBonus * xUses * xSynergy# x2Multi


        #return total

    def defensive_rank(self):
        dexEntry = self.dex.pkmn[self.no]
        base = (self.hp() + self.defense()) / 2
        xBuff = 1

        if 'buff' in dexEntry:
            b = dexEntry['buff']

            buffBonus = 0.1 * b.defBuffs[0] \
                      + 0.1 * max(sum(b.defBuffs[1:]), 3)


            xDuration = b.duration / 6 if b.duration < 6 else (1.0, 1.5, 1.9, 2.2)[int(b.duration / 6) - 1]
            xBuff = 1 + (buffBonus * xDuration)

        return base * xBuff

    def pp_rank(self, party, slot):
        dexEntry = self.dex.pkmn[self.no]
        if not 'pp+' in dexEntry:
            return -1

        party[slot] = self
        total = sum(battle.get_pp_restores(party, self, dexEntry))
        party[slot] = None
        return total

    def gau_rank(self):
        dexEntry = self.dex.pkmn[self.no]
        if not 'buff' in dexEntry:
            return -1

        b = dexEntry['buff']
        gau = b.atkBuffs[0]
        if not gau:
            return -1

        if b.duration < 6:
            return 0

        uses = min(3, (dexEntry['pp'] / dexEntry['pp_cost']))
        if self.hms and HM.BUFF in self.hms:
            gau += 1

        return gau * (uses / 2)


PER_PAGE = 8

BY_DEX         = 1
BY_TYPE        = 2
BY_ATK         = 3
BY_DEF         = 4
BY_ALPHA       = 5
BY_NEW         = 6
BY_HM          = 7
BY_TIER        = 8
BY_ZMOVE       = 9
BY_LEVEL       = 10

sortLabels = {
    BY_DEX: 'Sorted by Pokedex No.',
    BY_TYPE: 'Sorted by Type',
    BY_ATK: 'Sorted by Strength',
    BY_DEF: 'Sorted by Defense',
    BY_ALPHA: 'Alphabetical Order',
    BY_NEW: 'Sorted by New',
    BY_HM: 'Sorted by Trait',
    BY_TIER: 'Sorted by Tier',
    BY_ZMOVE: 'Sorted by Z-Move',
    BY_LEVEL: 'Sorted by Level'
}

class Pc(commands.Cog):
    def __init__(self, bot):
        # self.db = db
        self.bot = bot
        self.userdb = bot.userdb
        self.cache = {}
        self.imgcache = {}

    def load_db_into_cache(self, uid):
        # todo postgressql

        #badges = [load_pc_badge(d, self.bot.dex) for d in load_pcd(pcd)]

        userPc = self.get_debug_data()

        if userPc['resort']:
            userPc['resort'] = False
            self.sort_badges(userPc['badges'], userPc['sort'], userPc['sort'] < 0)

        userPc['expires'] = time.time() + 5 * 60
        self.cache[uid] = userPc

    def write_cache_to_db(self, uid, badges=True):
        pass


    async def handle_message(self, message):
        if len(message.content) > 20:
            return

        cmd = message.content.lower().strip()
        uid = message.author.id
        if not uid in self.cache:
            del self.bot.wfm[uid]
            return

        userPc = self.cache[uid]
        if cmd == 'z':
            userPc['page'] = max(0, userPc['page'] - 1)
            await self.view_page(message)
            return

        if cmd == 'x':
            userPc['page'] = min(math.ceil(len(userPc['badges']) / PER_PAGE) - 1, userPc['page'] + 1)
            await self.view_page(message)
            return

        if cmd.startswith('sort'):
            await self.sort_pc(message, cmd)
            return

        try:
            pageNo = int(cmd)
            if pageNo < 100:
                userPc['page'] = clamp(pageNo - 1, 0, math.ceil(len(userPc['badges']) / PER_PAGE) - 1)
                await self.view_page(message)
                return
        except ValueError:
            pass


    def get_starters(self, version):
        if version == RED:
            return [self.make_pkmn(name='Charmander', lv=5), self.make_evolve(name='Charmeleon')]
        if version == BLUE:
            return [self.make_pkmn(name='Squirtle', lv=5), self.make_evolve(name='Wartortle')]
        if version == GREEN:
            return [self.make_pkmn(name='Bulbasaur', lv=5), self.make_evolve(name='Ivysaur')]
        if version == YELLOW:
            return [self.make_pkmn(name='Pikachu', lv=5),
                    self.make_pkmn(name='Charmander', lv=5), self.make_evolve(name='Charmeleon'),
                    self.make_pkmn(name='Squirtle', lv=5), self.make_evolve(name='Wartortle'),
                    self.make_pkmn(name='Bulbasaur', lv=5), self.make_evolve(name='Ivysaur')]

    def make_pkmn(self, no=None, name=None, lv=1, orbs=0, z=None):
        if name:
            no = self.bot.dex.nos[name]
        pkmn = PcPokemon(self.bot.dex, no=no, lv=lv, orbs=orbs, z=z)

        #pkmn.n = n if n else self.pokedb.cursor().execute('select no from pkmn where name = ?', [name]).fetchone()[0]
        return pkmn

    def make_evolve(self, no=None, name=None, count=1):
        if name:
            no = self.bot.dex.nos[name]
        evolve = PcEvolution(self.bot.dex, no=no, count=count)
        #evolve.n = n if n else self.pokedb.cursor().execute('select no from pkmn where name = ?', [name]).fetchone()[0]
        return evolve

    # @commands.command()
    # async def pctest(self, ctx, arg=''):
    #     try:
    #         version = ('red', 'blue', 'green', 'yellow').index(arg.lower())
    #     except ValueError:
    #         version = RED
    #     await ctx.send(f'Init: {arg}')
    #     pkmn = self.get_starters(version)

    #     ns = [p.no if type(p) is PcPokemon else -p.no for p in pkmn]
    #     async with ctx.typing():
    #         text = self.page_text(0, pkmn, None)
    #         png = self.bot.render.render_pc(ns)
    #         e = discord.Embed(description=text).set_image(url='attachment://pc.png')
    #         await ctx.send(embed=e, file=discord.File(png, 'pc.png'))


    # @commands.command()
    # async def pcr(self, ctx, arg=''):
    #     pkmn = []

    #     for i in range(random.randint(0, 20)):
    #         if random.choice([True, True, False]):
    #             p = self.make_pkmn(no=self.bot.dex.sample_from_set(1, 1)[0], lv=random.randint(5, 100))
    #             if random.random() <= 0.2:
    #                 p.orbs = random.randint(1, 5)
    #             elif random.random() <= 0.2:
    #                 p.z = random.randint(10, 150)
    #         else:
    #             p = self.make_evolve(no=self.bot.dex.sample_from_set(1, 1, evo=True)[0], count=random.randint(1, 11))
    #         pkmn.append(p)

    #     ns = [p.no if type(p) is PcPokemon else -p.no for p in pkmn]
    #     async with ctx.typing():
    #         text = self.page_text(0, pkmn, 1)
    #         png = self.bot.render.render_pc(ns)
    #         e = discord.Embed(description=text).set_image(url='attachment://pc.png')
    #         await ctx.send(f'<@{ctx.author.id}>', embed=e, file=discord.File(png, 'pc.png'))


    def get_debug_data(self):
        badges = []
        # evos = set()
        # for i in range(90):
        #     if random.randint(0, 3):
        #         p = self.make_pkmn(no=self.bot.dex.sample_from_set(1, 1)[0], lv=50)#random.randint(5, 10))

        #         #p = self.make_pkmn(no=self.bot.dex.sample_from_set(1, 1)[0], lv=50)#random.randint(5, 100))
        #         # if random.random() <= 0.2:
        #         #     p.orbs = random.randint(1, 5)
        #         # elif random.random() <= 0.2:
        #         #     p.z = random.randint(10, 150)
        #         #     p.orbs = 5
        #     else:
        #         no = None
        #         while no is None or no in evos:
        #             no = self.bot.dex.sample_from_set(1, 1, evo=True)[0]
        #         evos.add(no)
        #         p = self.make_evolve(no=no, count=random.randint(1, 11))
        #     p.id = i
        #     badges.append(p)

        for i, no in enumerate(self.bot.dex.nos.values()):
            if self.bot.dex.pkmn[no]['set_no'] == 1:
                p = self.make_pkmn(no, lv=6)#random.randint(20, 30))#random.randint(5, 30))
                p.id = i
                # p.hms = []
                # for j in range(p.hm_slots()):
                #     p.hms.append(random.randint(0, HM_COUNT-1))
                # p.z = random.randint(60, 100)
                badges.append(p)

        page = 0
        sort = BY_DEX

        #dump = dump_pcd(badges)
        return {
            'badges': badges,
            'page': page,
            'sort': sort,
            'resort': True,
        }

    @commands.command()
    async def pcre(self, ctx, arg=''):
        self.load_db_into_cache(ctx.author.id)
        await ctx.send('Refreshed test PC data.')

    @commands.group(invoke_without_command=True)
    async def pc(self, ctx, arg=''):

        uid = ctx.author.id
        self.bot.wfm[uid] = {
            'handler': self,
            'channel': ctx.channel,
            'expires': time.time() + 5 * 60
        }

        if not uid in self.cache:
            self.load_db_into_cache(uid)

        try:
            self.cache[uid]['page'] = clamp(int(arg) - 1, 0, math.ceil(len(self.cache[uid]['badges']) / PER_PAGE) - 1)
        except ValueError:
            pass

        await self.view_page(ctx.message)

    @commands.command()
    async def sort(self, ctx, arg=''):
        await self.sort_pc(ctx.message, arg)

    @commands.command()
    async def fuse(self, ctx, *args):
        await self.fuse_pkmn(ctx, list(args))

    @commands.command()
    async def af(self, ctx, *args):
        await self.fuse_pkmn(ctx, list(args), True)

    async def sort_pc(self, message, arg):
        if any(s in arg for s in ['dex', 'no', 'num', 'default']):
            order = BY_DEX
        elif 'type' in arg:
            order = BY_TYPE
        elif 'atk' in arg or 'attack' in arg:
            order = BY_ATK
        elif 'def' in arg:
            order = BY_DEF
        elif any(s in arg for s in ['name', 'alpha', 'az', 'a-z', 'abc']):
            order = BY_ALPHA
        elif 'new' in arg:
            order = BY_NEW
        elif 'hm' in arg:
            order = BY_HM
        elif 'tier' in arg:
            order = BY_TIER
        elif 'z' in arg:
            order = BY_ZMOVE
        elif 'lv' in arg or 'level' in arg:
            order = BY_LEVEL
        else:
            await send_message(None, 'Invalid sort preference! Try `dex`, `lv`, `type`, `atk`, `def`, `z`, `name`, `new`, `hm` or `tier`, optionally in `reverse` order.', message=message, error=True)
            return

        uid = message.author.id
        if not uid in self.cache:
            self.load_db_into_cache(uid)
        userPc = self.cache[uid]

        if 'reverse' in arg:
            order = -order

        sortLabel = '{}{}'.format(sortLabels[abs(order)], ' (Reverse)' if order < 0 else '')
        if order == userPc['sort']:
            await send_message(None, f'Your PC is already: `{sortLabel}`', message=message, error=True)
            return

        userPc['page'] = 0
        userPc['sort'] = order

        self.sort_badges(userPc['badges'], userPc['sort'], userPc['sort'] < 0)
        self.write_cache_to_db(uid, badges=True)

        await send_message(None, f'Updated PC preference! `{sortLabel}`', message=message)

    async def view_page(self, message, page=None):
        uid = message.author.id
        userPc = self.cache[uid]
        page = page or userPc['page']
        ns, text = self.page_text(page, userPc['badges'], userPc['sort'])

        await message.channel.trigger_typing()
        t = time.time()
        footer = 'Type `z` to go back, `x` to go forward, or a page # such as `4`'

        if not uid in self.imgcache:
            self.imgcache[uid] = {}

        if page in self.imgcache[uid]:
            cacheImg, cacheNs = self.imgcache[uid][page]

            # async with self.bot.session.head(self.imgcache[uid][page]) as resp:
            #     print(resp)

            if ns == cacheNs:
                e = discord.Embed(description=text).set_image(url=cacheImg).set_footer(text=footer)
                await message.channel.send(f'<@{uid}> Took {time.time() - t:.3f} seconds [link]', embed=e)
                return

        png = self.bot.render.render_pc(ns)
        e = discord.Embed(description=text).set_image(url='attachment://pc.png').set_footer(text=footer)
        sent = await message.channel.send(f'<@{uid}> Took {time.time() - t:.3f} seconds', embed=e, file=discord.File(png, 'pc.png'))
        self.imgcache[uid][page] = (sent.embeds[0].image.url, ns)


    # #todo remove
    # @commands.command()
    # async def pcsl(self, ctx, arg=''):
    #     pkmn = []

    #     for i in range(random.randint(0, 20)):
    #         if random.choice([True, True, False]):
    #             p = self.make_pkmn(no=self.bot.dex.sample_from_set(1, 1)[0], lv=random.randint(5, 100))
    #             if random.random() <= 0.2:
    #                 p.orbs = random.randint(1, 3)
    #             elif random.random() <= 0.2:
    #                 p.z = random.randint(10, 150)
    #         else:
    #             p = self.make_evolve(no=self.bot.dex.sample_from_set(1, 1, evo=True)[0], count=random.randint(1, 11))
    #         pkmn.append(p)

    #     dump = dump_pcd(pkmn)
    #     print('Dumped: ', str(dump))
    #     loaded = load_pcd(dump)
    #     print('Loaded: ', str(loaded))

    #     newPkmn = []
    #     for d in loaded:
    #         p = load_pc_badge(d, self.bot.dex)
    #         newPkmn.append(p)

    #     print('Unpacked:', newPkmn)

    #     #ns = [p.no if type(p) is PcPokemon else -p.no for p in newPkmn]
    #     ns, text = self.page_text(0, newPkmn, None)
    #     async with ctx.typing():
    #         png = self.bot.render.render_pc(ns)
    #         e = discord.Embed(description=text).set_image(url='attachment://pc.png')
    #         await ctx.send(f'<@{ctx.author.id}>', embed=e, file=discord.File(png, 'pc.png'))


    # sort inventory


    def page_text(self, page, badges, order, filter=None):

        start = page * PER_PAGE
        end  = start + PER_PAGE

        if filter:
            filtered = [p for p in badges if filter.test(p)]
            pageBadges = filtered[start:end]
        else:
            pageBadges = badges[start:end]

        sortLabel = '{}{}'.format(sortLabels[abs(order)], ' (Reverse)' if order < 0 else '')
        pages = math.ceil(len(filtered) / PER_PAGE) if filter else math.ceil(len(badges) / PER_PAGE)
        lines = [f'{sortLabel}  •  Page **{page + 1}**  /  {pages}\n ']

        padding = len(str(len(pageBadges)))
        for i, badge in enumerate(pageBadges):
            d = self.bot.dex.pkmn[badge.no]

            if filter:
                index = '{n: <{padding}}'.format(n=badges.index(badge) + 1, padding=padding)
            else:
                index = '{n: <{padding}}'.format(n=i + 1 + start, padding=padding)

            if type(badge) is PcEvolution:
                ''' Evolution Badge '''
                #lines.append('{} `{} {}`  _x **{}**_ '.format(d['emoji'], index, '{}'.format('+ {}'.format(badge.format_name(key='short'))), badge.count))
                #lines.append(f'{d["emoji"]} `{index} + {badge.format_name(key="short")}`  _x **{badge.count}**_ ')
                ##lines.append(f'{d["emoji"]} `{index} [+] {badge.format_name(key="short")}`  _x **{badge.count}**_ ')
                lines.append(f'{d["emoji"]} `{index} [+]` _{badge.format_name(key="short")}_  x **{badge.count}** ')
                #lines.append(f'{d["emoji"]} `{index} [+] {badge.format_name(key="short")}`  x **{badge.count}** ')

            else:
                ''' Standard Pokemon '''
                if badge.z:
                    stat1 = f'{badge.z}%'
                elif badge.orbs > 0:
                    stat1 = '•' * badge.orbs
                else:
                    stat1 = 'Lv{: >3}'.format(badge.lv)

                stat2 = '-' if badge.tm is None else tmKeys[badge.tm]
                name = badge.format_name(key='short')

                lines.append('{} `{} {} {} {}` {} '.format(
                    d['emoji'],
                    index,
                    '{: <11}'.format(name),
                    '{: >5}'.format(stat1),
                    '{: >3}'.format(stat2),
                    badge.hms_as_text(showBlank=False, addBreak=True)))

        if filter:
            lines.append(f''' 
🔍 Filter: _{filter.as_label()}_
`.pc filter` to toggle on/off
`.pc clear` to remove
`.pc help` to list additional options''')

        ns = [p.no if isinstance(p, PcPokemon) else -p.no for p in pageBadges]

        #description = resizePcToFit(description)
        return ns, '\n'.join(lines)



        # attempt to load off cache
        # try:
        #     with open('khux/inventory_cache/{}_{}{}_{}.png'.format(client.context.userId, SortOrder(order).name, 'r' if reverse else '', page), 'rb') as f:
        #         img = MIMEImage(f.read())
        # except FileNotFoundError:

    def sort_badges(self, badges, order, reverse):
        pkmn = self.bot.dex.pkmn

        list.sort(badges, key=lambda p: 0 if isinstance(p, PcPokemon) else 1)

        if order == BY_DEX:
            list.sort(badges, key=lambda p: p.no, reverse=reverse)
            list.sort(badges, key=lambda p: p.type() if isinstance(p, PcPokemon) else pkmn[p.no]['type'], reverse=reverse)
            list.sort(badges, key=lambda p: pkmn[p.no]['pokedex_no'], reverse=reverse)

        elif order == BY_TYPE:
            list.sort(badges, key=lambda p: p.no, reverse=reverse)
            list.sort(badges, key=lambda p: pkmn[p.no]['pokedex_no'], reverse=reverse)
            list.sort(badges, key=lambda p: p.type() if isinstance(p, PcPokemon) else pkmn[p.no]['type'], reverse=reverse)

        elif order == BY_ATK:
            list.sort(badges, key=lambda p: p.attack() if isinstance(p, PcPokemon) else 0, reverse=not reverse)

        elif order == BY_DEF:
            list.sort(badges, key=lambda p: p.defense() if isinstance(p, PcPokemon) else 0, reverse=not reverse)

        elif order == BY_ALPHA:
            list.sort(badges, key=lambda p: pkmn[p.no]['name'].lower(), reverse=reverse)

        elif order == BY_NEW:
            list.sort(badges, key=lambda p: p.id, reverse=not reverse)

        elif order == BY_TIER:
            list.sort(badges, key=lambda p: p.tier() if isinstance(p, PcPokemon) else pkmn[p.no]['tier'], reverse=reverse)

        elif order == BY_HM:
            list.sort(badges, key=lambda p: p.hms[1] if p.hms and len(p.hms) >= 2 else 12, reverse=reverse)
            list.sort(badges, key=lambda p: p.hms[0] if p.hms else 12, reverse=reverse)

        elif order == BY_ZMOVE:
            list.sort(badges, key=lambda p: p.z if isinstance(p, PcPokemon) and p.z else 0, reverse=not reverse)

        elif order == BY_LEVEL:
            list.sort(badges, key=lambda p: p.lv if isinstance(p, PcPokemon) else 0, reverse=not reverse)


    async def fuse_pkmn(self, ctx, args, af=False):

        pkmn = self.bot.dex.pkmn

        # 'evo' into
        burnNs = []
        try:
            if af:
                baseN = int(args[0]) - 1
            else:
                baseN = int(args.pop()) - 1
                if args.pop() != 'into':
                    raise ValueError
                burnNs = [int(n) - 1 for n in args]

        except (ValueError, IndexError) as e:
            await send_message(ctx, f'Invalid Syntax! Try `{ctx.prefix}{ctx.command} help`.', error=True)
            return

        if baseN in burnNs:
            await send_message(ctx, 'You can\'t fuse a Pokémon into itself.', error=True)
            return

        duplicates = [k for k,v in Counter(burnNs).items() if v>1 and k is not None]
        if len(duplicates) > 0:
            await send_message(ctx, f'You cannot fuse the same Pokémon twice: {[d+1 for d in duplicates]}', error=True)
            return

        uid = ctx.author.id
        if not uid in self.cache:
            self.load_db_into_cache(uid)
        userPc = self.cache[uid]

        try: base = userPc['badges'][baseN]
        except IndexError:
            await send_message(ctx, f'Pokémon `{baseN+1}` does not exist in your PC!', error=True)
            return

        if isinstance(base, PcEvolution):
            await send_message(ctx, f'You cannot fuse Pokémon into an evolution badge.', error=True)
            return

        name = pkmn[base.no]['name']

        burns = []
        burnEvos = 0
        for n in burnNs:
            try:
                p = userPc['badges'][n]
                if p.no != base.no:
                    await send_message(ctx, f'''You cannot fuse a {pkmn[p.no]['name']} (`{n+1}`) into a {name}''', error=True)
                    return
                if isinstance(p, PcEvolution):
                    await send_message(ctx, f'To fuse an evolution (`{n+1}`), instead use `{ctx.prefix}fuse 3 evo into {baseN+1}` where `3` is the number of evolutions to fuse. Alternatively, you can use `{ctx.prefix}af {baseN+1}` which will automatically fuse evolutions first, along with spare Pokémon.', error=True)
                    return
                burns.append(p)
            except IndexError:
                await send_message(ctx, f'Pokémon `{n+1}` does not exist in your PC!', error=True)
                return

        if af:
            targetOrbs = 6 - base.orbs
            evo = None
            spares = []
            for p in userPc['badges']:
                if p != base and p.no == base.no:
                    if isinstance(p, PcEvolution):
                        evo = p
                    elif p.is_spare():
                        spares.append(p)

            burnOrbs = 0
            if evo:
                burnEvos = burnOrbs = min(targetOrbs, evo.count)
                evo.count -= burnOrbs
                if evo.count == 0:
                    userPc['badges'].remove(evo)

            if spares and burnOrbs < targetOrbs:
                list.sort(spares, key=lambda p: p.lv)
                for p in spares:
                    burns.append(p)
                    burnOrbs += p.orbs + 1
                    if burnOrbs >= targetOrbs:
                        break

            if burnOrbs == 0:
                await send_message(ctx, 'Could not find any suitable fusion Pokémon :(', error=True)
                return

        userPc['badges'] = [p for p in userPc['badges'] if p not in burns]

        ob = copy.copy(base)
        zRolls = 0
        hmRolls = 0
        hmQueue = []
        slots = base.hm_slots()

        # Fusion

        for i in range(burnEvos):
            hmRolls += 1
            base.orbs += 1
            if base.orbs > 5:
                zRolls += 1
                base.orbs = 5

        for p in burns:
            hmRolls += 1
            #base.lv = min(MAX_LV, base.lv + 1)
            base.lv = max(base.lv, p.lv)
            base.orbs += p.orbs + 1
            if p.hms:
                if not base.hms:
                    base.hms = []

                for i, hm in enumerate(p.hms):
                    if len(base.hms) < slots:
                        base.hms.append(hm)
                    else:
                        hmQueue += p.hms[i:]
                        break

            if base.orbs > 5:
                zRolls += 1
                base.orbs = 5

        base.lv = min(MAX_LV, base.lv + len(burns))

        for i in range(hmRolls):
            roll = secrets.randbelow(HM_COUNT)
            if not base.hms or len(base.hms) < slots:
                if not base.hms:
                    base.hms = [roll]
                else:
                    base.hms.append(roll)
            else:
                hmQueue.append(roll)

        # Fields

        e = discord.Embed(title='Z-Move Unlocked!' if zRolls > 0 else 'Pokémon Fusion!', color=TYPE_COLORS[base.type()])

        e.add_field(name=f'⚔ Attack', value=f'{ob.attack()} -> **{base.attack()}**', inline=True)
        e.add_field(name=f'🛡 Defense', value=f'{ob.defense()} -> **{base.defense()}**', inline=True)

        parts = []
        if zRolls > 0:
            zMin, zMax = zRanges[base.tier() - 1]
            zBonuses = [secrets.randbelow(zMax-zMin+1) + zMin for roll in range(zRolls)]

            part = 'With a range of {}-{}, you rolled the following Z-Bonus(es): **{}**' \
                .format(zMin, zMax, '** **'.join(str(n) for n in zBonuses))

            maxRoll = max(zBonuses)
            if base.z is None or maxRoll > base.z:
                base.z = maxRoll
                e.add_field(name=f'{tierEmoji[base.tier()]} Z-Move',
                    value='{}% -> **{}%**'.format(0 if ob.z is None else ob.z, base.z), inline=True)
            else:
                part += f'\nUnfortunately, your Z-Move remains unchanged at **{base.z}**%.'

            parts.append(part)


        #if base.lv > ob.lv:
        lvText = f'Lv. {ob.lv} -> **{base.lv}**'
        orbText = '{} -> {}'.format('•' * ob.orbs if ob.orbs else 'Unorbed', '•' * base.orbs)

        e.add_field(name=f'✨ Level Up!', value=f'{lvText}\n{orbText}', inline=True)



        # HMs
        if base.hms:
            newHms = [hm for hm in base.hms if not ob.hms or hm not in ob.hms]
            if newHms:
                hmText = '  '.join([f'{hmEmoji[hm]} {hmLabels[hm]}' for hm in newHms])
                if len(newHms) == 1:
                    parts.append(f'''_{name} learned a new HM!_\n{hmText}''')
                else:
                    parts.append(f'''_{name} learned **{len(newHms)}** new HMs!_\n{hmText}''')

        if hmQueue:
            parts.append(f'You now have **{len(hmQueue)}** additional HM choice(s). Type `{ctx.prefix}hms` to manage them.')


        # todo pokedex update

        # Output

        burnNames = [pkmn[p.no]['name'] for p in burns]
        tallies = [(name, burnNames.count(name)) for name in set(burnNames)]
        if burnEvos:
            tallies.append((f'''[+] {name}''', burnEvos))
        footer = 'Pokémon Removed! {}'.format(', '.join(f'{t[0]} x {t[1]}' for t in tallies))

        if not parts:
            parts = [f'''_{name}_''']

        if random.random() <= 1/3:# and len(parts) < 2:
            parts.append(f'Tip: Automatically fuse and clean your PC using `{ctx.prefix}pc clean`')

        e.description = DBL_BREAK.join(parts)
        e.set_thumbnail(url=pkmn[base.no]['gif']) \
         .set_footer(text=footer, icon_url=pkmn[base.no]['sprite'])

        await ctx.send(f'<@{ctx.author.id}>', embed=e)




def setup(bot):
    pc = Pc(bot)
    bot.add_cog(pc)
    bot.pc = pc

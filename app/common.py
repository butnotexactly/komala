import asyncio
import re
import discord
import copy

from numpy import interp
from discord.ext import commands


idPattern = re.compile(r'<@!?(\d+?)>')

ST, AOE, RAND = 0, 1, 2

N, E, S, W = 0, 1, 2, 3
RED, BLUE, GREEN, YELLOW = 0, 1, 2, 3
ICON_ATTACK = '⚔'
ICON_CLOSE = '❌'
#SKIP = ''
ERROR_RED = 0xD32F2F #0xB50000
INFO_BLUE = 0x3579f0

DBL_BREAK = '\n \n'
FIELD_BREAK = '\n\u200b'

MALE, FEMALE = 1, 2
FEATHER, LIGHT, MID, HEAVY, TITAN = 0, 1, 2, 3, 4

COMMON, AVERAGE, UNCOMMON, RARE, SECRET = 0, 1, 2, 3, 4


UNRANKED = -10000

async def send_message(ctx, text, message=None, ping=True, error=False, color=None, expires=None):

    message = message or ctx.message

    e = discord.Embed(description=text)
    if color or error:
        e.color = color if color else ERROR_RED
    if expires is None and error:
        expires = 10

    #header = '{}{}'.format('<@{}>'.format(ctx.author.id) if ping else '', ': {}'.format(CLOSE) if ping and error else '')
    #header = '{}{}'.format('{} '.format(CLOSE) if ping and error else '', '<@{}>'.format(ctx.author.id) if ping else '')
    header = '<@{}>'.format(message.author.id) if ping else ''
    sent = await message.channel.send(header, embed=e, delete_after=expires)
    return sent

def enquote(text):
    return f'“{text}”'

E_PKMN_ENCOUNTER = 0
E_TRAINER_BATTLE = 1
E_GYM_BATTLE     = 2
E_PVP_BATTLE     = 3

noEmoji = (':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:')

NORMAL      = 0
FIRE        = 1
WATER       = 2
NATURE      = 3
EARTH       = 4
ELECTRIC    = 5
ICE         = 6
PSYCHIC     = 7
FAIRY       = 8
DARK        = 9
DRAGON      = 10


X = 2
O = 0.5

typeChart = [
    #No Fr Wa Na Ea El Ic Ps Fy Dk Dg
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # Normal
    [1, O, O, X, 1, 1, X, 1, 1, 1, O], # Fire
    [1, X, O, O, X, 1, 1, 1, 1, 1, O], # Water
    [1, O, X, O, X, 1, 1, 1, X, 1, O], # Nature
    [1, X, 1, O, 1, X, X, O, 1, 1, 1], # Earth
    [1, 1, X, 1, O, O, X, 1, 1, 1, O], # Electric
    [1, O, O, X, X, 1, O, 1, 1, 1, X], # Ice
    [1, 1, 1, X, X, 1, 1, O, 1, O, 1], # Psychic
    [1, O, 1, 1, 1, 1, 1, 1, O, X, X], # Fairy
    [1, 1, 1, 1, 1, 1, 1, X, O, O, 1], # Dark
    [1, 1, 1, 1, 1, 1, 1, 1, O, 1, X], # Dragon
]

TYPE_COLORS = (
    0xFFFFFF,
    0xE88158,
    0x57AADE,
    0x7FBF78,
    0x9C6E5A,
    0xF2CB6F,
    0x9DD1F2,
    0xAD70D5,
    0xF0A1C1,
    0x222222, #0x6B6B6B,
    0x646EAB
)

typeNames = (
    'Normal',
    'Fire',
    'Water',
    'Nature',
    'Earth',
    'Electric',
    'Ice',
    'Psychic',
    'Fairy',
    'Dark',
    'Dragon',
)

typeSuffixes = [f' ({t})' for t in typeNames]

typeKeys = ('no', 'fr', 'wa', 'na', 'ea', 'el', 'ic', 'ps', 'fy', 'dk', 'dg')
typeEmoji = ('<:tn:416740418231861273>',
            '<:tfr:416740338284232715>',
            '<:tw:416740466080481280>',
            '<:tna:416740390293471232>',
            '<:te:416740271095545858>',
            '<:tel:416740295011729429>',
            '<:ti:416740363580211206>',
            '<:tp:416740443674378241>',
            '<:tf:416740317174300672>',
            '<:td:416740157400547349>',
            '<:tdr:416740237247643648>',
            '<:tra:426142386830311425>')

def get_type_resistances(defTypes, low=0.4, high=2.8):
    multis = []
    for atkType in range(11):
        x = 1.0
        for defType in defTypes:
            #x *= typeChart[atkType][defType]
            if typeChart[atkType][defType] == X:
                x += 0.5
            elif typeChart[atkType][defType] == O:
                x -= 0.5
        x = clamp(x, low, high)
        multis.append(x)
    return multis

def type_resistances_as_text(multis):
    weaknesses = []
    resists = []
    for atkType, x in enumerate(multis):
        if x < 1:
            resists.append(atkType)
        elif x > 1:
            weaknesses.append(atkType)

    text = []
    if weaknesses:
        text.append('_Weakness:_ {}'.format(''.join(typeEmoji[t] for t in weaknesses)))
    if resists:
        text.append('_Resistance:_ {}'.format(''.join(typeEmoji[t] for t in resists)))
    return '\n'.join(text)

MAX_LV = 100


deckShorts = ('cb', 'cer', 'cel', 'bw', 'ma', 'riv', 'xy', 'cat', 'tr', 'bt')
deckKeys = ('cinnabar', 'cerulean', 'celadon', 'bw', 'mahogany', 'river', 'xy', 'cataclysm', 'rocket', 'blackthorn')
deckNames = (
    'Cinnabar Deck',
    'Cerulean Deck',
    'Celadon Deck',
    'BW Deck',
    'Mahogany Deck',
    'River Deck',
    'XY Deck',
    'Cataclysm Deck',
    'Team Rocket Deck',
    'Blackthorn Deck'
)

deckMultis = {}
deckBoosts = {
    'cinnabar':   ([EARTH], [NORMAL], [EARTH, FIRE], [FIRE], [EARTH, FIRE]),
    'cerulean':   ([ICE], [WATER], [ICE, WATER], [NORMAL], [ICE, WATER]),
    'celadon':    ([PSYCHIC], [PSYCHIC, NATURE], [NORMAL], [FAIRY, PSYCHIC, NATURE], [FAIRY, NATURE]),
    'bw':         ([FIRE, DARK], [FIRE, ELECTRIC], [ELECTRIC], [NORMAL], [FIRE, ELECTRIC]),
    'mahogany':   ([PSYCHIC, ICE], [NORMAL], [ICE], [PSYCHIC, ICE], [PSYCHIC]),
    'river':      ([NATURE, WATER], [NORMAL], [NATURE], [WATER], [NATURE, WATER]),
    'xy':         ([FAIRY, DARK], [NORMAL], [DARK], [FAIRY], [FAIRY, DARK]),
    'cataclysm':  ([EARTH, FIRE], [WATER, DRAGON], [NORMAL], [EARTH, FIRE, WATER], [DRAGON]),
    'rocket':     ([EARTH, DARK], [EARTH, NATURE, DARK], [NORMAL], [EARTH, NATURE, DARK], [DARK]),
    'blackthorn': ([ELECTRIC, DRAGON], [NORMAL], [ELECTRIC, DRAGON], [DRAGON], [ELECTRIC, DRAGON]),

}

zRanges = (
    (35, 80),
    (55, 100),
    (75, 120),
    (90, 140),
    (120, 180),
    (145, 200)
)

tierEmoji = (
    '<:tier1:331798497969831936>',
    '<:tier2:331798498024488960>',
    '<:tier3:336791576103747585>',
    '<:tier4:336791575931781133>',
    '<:tier5:351611042918301697>',
    '<:tier6:413194665974562816>'
)



HM_COUNT = 10

class HM(object):
    PP = 0
    HP = 1
    ATK = 2
    DEF = 3
    BUFF = 4 #todo
    EXP = 5 #todo
    RESIST = 6 #todo
    CRIT = 7
    TOTEM = 8 #todo
    PIERCE = 9
    #ELEMENT = 10

hmLabels = (
    'PP+',
    'HP+',
    'Atk+',
    'Def+',
    'Buff+',
    'Exp+',
    'Status Resist+',
    'Crit+',
    'Totem+',
    'Pierce+',
    #'Element+',
)


hmEmoji = (
    '<:t_sp:339974525737500673>',
    '<:t_hp:339974526022582273>',
    '<:t_str:339974528392495105>',
    '<:t_def:339974524001058816>',
    '<:t_el:461988077653721099>',
    '<:t_xp:461988077615710255>',
    '<:t_psn:339974527285198849>',
    '<:t_g:339974525062086656>',
    '<:t_rd:339974523531165696>',
    '<:t_pr:461988077980745749>',
    #    '<:t_bf:406146452067450900>',
)

hmBlank = '<:t_:339978695722795018>'
hmSpacer = '<:t_spc:340368121435127808>'

pokeballUrl = 'http://play.pokemonshowdown.com/sprites/itemicons/poke-ball.png'

#hmKeys = ('dc', 'str', 'def', 'sp', 'sleep', 'poison', 'para', 'raid', 'hp', 'ground', 'air', 'buff')
#hmLabels = ('Extra Attack', 'STR +1000', 'DEF +{}'.format(DEF_BONUS), 'Max Gauges +2', 'Sleep Resist +60%', 'Poison Resist +60%', 'Paralysis Resist +60%', 'Raid Damage +40%', 'HP +800', 'Ground DEF Down -45%', 'Aerial DEF Down -45%', 'Buff+')
# hmEmoji = {
#     'dc': '<:t_dc:339974524554706954>',
#     'atk': '<:t_str:339974528392495105>',
#     'def': '<:t_def:339974524001058816>',
#     'pp': '<:t_sp:339974525737500673>',
#     'resist': '<:t_psn:339974527285198849>',
#     'hp': '<:t_hp:339974526022582273>',
#     'totem': '<:t_rd:339974523531165696>',
#     'buff': '<:t_bf:406146452067450900>',

#     'exp': '<:t_:339978695722795018>',
#     'crit': '<:t_:339978695722795018>',
#     'element': '<:t_:339978695722795018>',
#     'find': '<:t_:339978695722795018>',

#     # 'sleep': '<:t_slp:339974527838846989>',
#     # 'para': '<:t_para:339974526828019712>',
#     # 'ground': '<:t_g:339974525062086656>',
#     # 'air': '<:t_a:339974522927316994>',

#     'blank': '<:t_:339978695722795018>',
#     'spacer': '<:t_spc:340368121435127808>',
# }


tmKeys = []



# PP+
# HP+
# ATK+
# DEF+
# Buff+
# EXP+
# Resist+
# Crit+
# Element+ (raises buff cap by 1 for given element, max 3, does not stack per pokemon)
# Find+ (Drops from raid)
# Totem Damage
# Pierce (def down)

PSN, SEED, BURN, PARA, FLINCH, SLP, CONFUSE, CHARM = 0, 1, 2, 3, 4, 5, 6, 7
statusEmoji = (
    '🍄',
    '🌱',
    '🔥',
    '⚡',
    '💥',
    '💤',
    '💫',
    '💕'
)
statusNames = (
    'Poison',
    'Leech Seed',
    'Burn',
    'Paralyze',
    'Flinch',
    'Sleep',
    'Confusion',
    'Charm',
)

pokemoji = {
    'pkmn_spacer': '<:ps:455461834414358578>',
    'hail': '❄',
    'sand': '🌪',

    'pokeball': '<:pb:413869699890413578>',
    'greatball': '<:pb:413869699395485707>',
    'skip': '<:sk:442765391576694784>',
    'pb_small': '<:pbs:443274498360213515>',

}

# def init_emoji(bot):
#    # global skip

#     pokemoji['pokeball'] = bot.get_emoji(413869699890413578)
#     pokemoji['greatball'] = bot.get_emoji(413869699395485707)
#     pokemoji['skip'] = bot.get_emoji(442765391576694784)
#     pokemoji['pb_small'] = bot.get_emoji(443274498360213515)

#     pokemoji['pkmn_spacer'] = '<:ps:455461834414358578>'
#     pokemoji['hail'] = '❄'
#     pokemoji['sand'] = '🌪'

#     # skip = pokemoji['skip']
#     # print(skip)


def base_name(name, remove=None):
    for suffix in typeSuffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    if remove:
        name = re.sub(r'[' + remove + ']', '', name)
    return name

def ordinal(num, bold=False):
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
    return "**{}**{}".format(num, suffix) if bold else str(num) + suffix

def scale_stat(lv, base, iv, ev, xNature):
    #base = interp(base, [40, 130], [60, 100])
    return int(int((2 * base + iv + ev) * lv / 100 + 5) * xNature)

def scale_hp(lv, base, iv, ev):
    return int(int((2 * base + iv + ev) * lv / 100 + lv + 10))

def clamp(n, lo, hi):
    return max(min(n, hi), lo)

def group_rainbow_buff(buffGroups):
    if not len(buffGroups):
        return

    tiers = list(buffGroups.keys())
    samesign = not (min(tiers) < 0 < max(tiers))

    if samesign and sum(len(types) for types in buffGroups.values()) == 11:
        lsBuff = min(tiers) if tiers[0] > 0 else max(tiers)
        buffGroups[lsBuff] = [NORMAL, -1] if NORMAL in buffGroups[lsBuff] else [-1]

class Buff(object):
    def __init__(self, duration=255):
        self.duration = duration
        self.atkBuffs = [0] * 11
        self.defBuffs = [0] * 11
        self.atkDebuffs = [0] * 11
        self.defDebuffs = [0] * 11
        self.reflect = 0
        #todo fix reflect

    def __repr__(self):
        return self.as_text()

    def add(self, other):
        for i in range(11):
            self.atkBuffs[i] += other.atkBuffs[i]
            self.defBuffs[i] += other.defBuffs[i]
            self.atkDebuffs[i] += other.atkDebuffs[i]
            self.defDebuffs[i] += other.defDebuffs[i]

    def balance(self):
        for i in range(11):
            if self.atkBuffs[i] == self.atkDebuffs[i]:
                self.atkBuffs[i] = self.atkDebuffs[i] = 0
            if self.defBuffs[i] == self.defDebuffs[i]:
                self.defBuffs[i] = self.defDebuffs[i] = 0

    def cap(self, a, b, c, d):
        for i in range(11):
            self.atkBuffs[i] = clamp(self.atkBuffs[i], -a, a)
            self.defBuffs[i] = clamp(self.defBuffs[i], -b, b)
            self.atkDebuffs[i] = clamp(self.atkDebuffs[i], -c, c)
            self.defDebuffs[i] = clamp(self.defDebuffs[i], -d, d)

    def is_zero(self):
        return all(b == 0 for b in self.atkBuffs) and \
               all(b == 0 for b in self.defBuffs) and \
               all(b == 0 for b in self.atkDebuffs) and \
               all(b == 0 for b in self.defDebuffs)

    def is_defensive(self):
        return any(b > 0 for b in self.defBuffs)

    def as_self_buff(self, duration=None):
        buff = Buff()
        buff.duration = duration or self.duration
        buff.atkBuffs = self.atkBuffs[:]
        buff.defBuffs = self.defBuffs[:]
        return buff

    def as_target_buff(self, duration=None, x=1):
        buff = Buff()
        buff.duration = duration or self.duration
        for i in range(11):
            buff.atkDebuffs[i] = self.atkDebuffs[i] * x
            buff.defDebuffs[i] = self.defDebuffs[i] * x
        return buff

    def clone(self):
        clone = Buff()
        clone.duration = self.duration
        clone.atkBuffs = self.atkBuffs[:]
        clone.defBuffs = self.defBuffs[:]
        clone.atkDebuffs = self.atkDebuffs[:]
        clone.defDebuffs = self.defDebuffs[:]
        return clone

    # def as_text(self, bold=False):

    #     atkGroups = {}
    #     defGroups = {}
    #     for i in range(0, 11):
    #         atkTiers = self.atkBuffs[i] - self.atkDebuffs[i]
    #         defTiers = self.defBuffs[i] - self.defDebuffs[i]

    #         if atkTiers != 0:
    #             if atkTiers in atkGroups:
    #                 atkGroups[atkTiers].append(i)
    #             else:
    #                 atkGroups[atkTiers] = [i]

    #         if defTiers != 0:
    #             if defTiers in defGroups:
    #                 defGroups[defTiers].append(i)
    #             else:
    #                 defGroups[defTiers] = [i]

    #     for tiers in atkGroups:
    #         if sum(atkGroups[tiers]) == 55:
    #             atkGroups[tiers] = [0, -1] if 0 in atkGroups[tiers] else [-1]
    #     for tiers in defGroups:
    #         if sum(defGroups[tiers]) == 55:
    #             defGroups[tiers] = [0, -1] if 0 in defGroups[tiers] else [-1]

    #     atkList = sorted(atkGroups.items(), key=lambda g: 100 if 0 in g[1] else g[0], reverse=True)
    #     defList = sorted(defGroups.items(), key=lambda g: 100 if 0 in g[1] else g[0], reverse=True)

    #     lines = []
    #     if atkList:
    #         parts = ['Atk:']
    #         for g in atkList:
    #             parts.append('[{}] {}{}'.format(
    #                 ''.join(typeEmoji[t] for t in g[1]),
    #                 '+' if g[0] > 0 else '',
    #                 f'**{g[0]}**' if bold else g[0]))
    #         lines.append(' '.join(parts))

    #     if defList:
    #         parts = ['Def:']
    #         for g in defList:
    #             parts.append('[{}] {}{}'.format(
    #                 ''.join(typeEmoji[t] for t in g[1]),
    #                 '+' if g[0] > 0 else '',
    #                 f'**{g[0]}**' if bold else g[0]))
    #         lines.append(' '.join(parts))

    #     if len(atkList) + len(defList) > 2:
    #         return '\n'.join(lines)
    #     return '   '.join(lines)

    def as_text(self, bold=False):

        atkGroups = {}
        defGroups = {}
        for i in range(0, 11):
            atkTiers = self.atkBuffs[i] - self.atkDebuffs[i]
            defTiers = self.defBuffs[i] - self.defDebuffs[i]

            if atkTiers != 0:
                if atkTiers in atkGroups:
                    atkGroups[atkTiers].append(i)
                else:
                    atkGroups[atkTiers] = [i]

            if defTiers != 0:
                if defTiers in defGroups:
                    defGroups[defTiers].append(i)
                else:
                    defGroups[defTiers] = [i]

        group_rainbow_buff(atkGroups)
        group_rainbow_buff(defGroups)


        # for tiers in atkGroups:
        #     if sum(atkGroups[tiers]) == 55:
        #         atkGroups[tiers] = [0, -1] if 0 in atkGroups[tiers] else [-1]
        # for tiers in defGroups:
        #     if sum(defGroups[tiers]) == 55:
        #         defGroups[tiers] = [0, -1] if 0 in defGroups[tiers] else [-1]

        atkList = sorted(atkGroups.items(), key=lambda g: 100 if 0 in g[1] else g[0], reverse=True)
        defList = sorted(defGroups.items(), key=lambda g: 100 if 0 in g[1] else g[0], reverse=True)

        lines = []
        if atkList:
            parts = ['Atk:']
            for g in atkList:
                parts.append('[{}] {}{}'.format(
                    ''.join(typeEmoji[t] for t in g[1]),
                    '+' if g[0] > 0 else '-',
                    f'**{abs(g[0])}**' if bold else abs(g[0])))
            lines.append(' '.join(parts))

        if defList:
            parts = ['Def:']
            for g in defList:
                parts.append('[{}] {}{}'.format(
                    ''.join(typeEmoji[t] for t in g[1]),
                    '+' if g[0] > 0 else '-',
                    f'**{abs(g[0])}**' if bold else abs(g[0])))
            lines.append(' '.join(parts))

        if len(atkList) + len(defList) > 2:
            return '\n'.join(lines)
        return '   '.join(lines)


def buff_inline_text(dexEntry):
    selfs = []
    targets = []

    if 'buff' in dexEntry:
        buff = dexEntry['buff']
        if any(b > 0 for b in buff.atkBuffs):
            selfs.append('Atk')
        if any(b > 0 for b in buff.defBuffs):
            selfs.append('Def')
        if any(b > 0 for b in buff.atkDebuffs):
            targets.append('Atk')
        if any(b > 0 for b in buff.defDebuffs):
            targets.append('Def')

    if dexEntry['acc_buff']:
        selfs.append('Accuracy')
    if dexEntry['evade_buff']:
        selfs.append('Evasion')
    if dexEntry['acc_debuff']:
        targets.append('Accuracy')
    if dexEntry['evade_debuff']:
        targets.append('Evasion')
    if 'crit+' in dexEntry:
        selfs.append('Crit. Rate')

    return f" [**+**{'/'.join(selfs)}]" if selfs else '', f" [**-**{'/'.join(targets)}]" if targets else ''

def can_breed(a, b):
    return a.gender == MALE and b.gender == FEMALE or \
           a.gender == FEMALE and b.gender == MALE


def shrink_emojis_to_fit(text, limit=1024):
    if len(text) > limit:
        text = text.replace(typeEmoji[FIRE], '🔥')
    if len(text) > limit:
        text = text.replace(typeEmoji[WATER], '💧')
    if len(text) > limit:
        text = text.replace(typeEmoji[ICE], '❄')
    if len(text) > limit:
        text = text.replace(typeEmoji[ELECTRIC], '⚡')
    if len(text) > limit:
        text = text.replace(typeEmoji[NATURE], '🍃')
    if len(text) > limit:
        text = text.replace(typeEmoji[DARK], '⚫')
    if len(text) > limit:
        text = text.replace(typeEmoji[FAIRY], '🌸')
    if len(text) > limit:
        text = text.replace(typeEmoji[DRAGON], '🦎')

    return text


NPCS = {
    'tr_grunt_m': 'https://i.imgur.com/1haiFDu.png',
    'tr_grunt_f': 'https://i.imgur.com/3JXDloK.png',
    'oak': 'https://i.imgur.com/lqOy8Bn.png',
    'roxie': 'https://i.imgur.com/UKaNIgp.png',
    'gary': 'https://i.imgur.com/5HcaRPk.png',
    'breeder_m': 'https://i.imgur.com/H4Mmm50.png',
    'breeder_f': 'https://i.imgur.com/b51tfX4.png',

}

def setup(bot):
    pass





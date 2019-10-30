import random
import secrets
import random
import math
import copy
import importlib
import sys
import traceback
import sqlite3
import re

from battle import *
from common import *

import explore

'''
Best of x Rounds
Coin flip

x's Turn

y's Turn



'''

class FakeBot(object):
    def __init__(self):
        self.extensions = {}
        self.render = None
        self.dex = None
        self.pc = None
        self.party = None
        self.battle = None
        self.explore = None
        self.rpg = None
        self.gym = None

        self.userdb = sqlite3.connect('data/users.db')

        self.wfr = {}
        self.wfm = {}

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    def load_extension(self, name):
        if name in self.extensions:
            return

        lib = importlib.import_module(name)
        if not hasattr(lib, 'setup'):
            del lib
            del sys.modules[name]
            raise ValueError('extension does not have a setup function')

        lib.setup(self)
        self.extensions[name] = lib

    def add_cog(self, cog):
        pass

def printc(text):
    #text = re.sub(r'<(:.*?:)[0-9]*>', r'\1', text)
    text = re.sub(r'<:t([a-z]{1,2}):[0-9]*>', r'<\1>'.upper(), text)
    text = re.sub(r'<(:.*?:)[0-9]*>', r'\1', text)
    #text = re.sub(r'<(:.*?:)[0-9]*>', ' ', text)
    text = re.sub(r'[`*_]', '', text)
    print(text)



initial_extensions = (
    #'admin',
    #'error',
    #'render',
    'pokedex',
    'pc',
    'party',
    'battle',
    'explore',
    'gym',
    #'rpg',
)



fakebot = FakeBot()
dex = fakebot.dex


xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
boosts = deckBoosts[deckKeys[random.randint(0, 9)]]

pkmn = []
nos = dex.sample_from_set(6, 1)
for no in nos:
    p = fakebot.pc.make_pkmn(no=no, lv=20)
    #p = fakebot.pc.make_pkmn(name='Fletchinder', lv=20)
    pkmn.append(p)
party = to_battle_pkmn(pkmn, boosts, xSlots)
p1 = TrainerState(party, pvp=True)


pkmn = []
nos = dex.sample_from_set(6, 1)
for no in nos:
    p = fakebot.pc.make_pkmn(no=no, lv=20)
    #p = fakebot.pc.make_pkmn(name='Fletchinder', lv=20)
    pkmn.append(p)
party = to_battle_pkmn(pkmn, boosts, xSlots)
p2 = TrainerState(party, pvp=True)



print(p1.typeResists)
print(p2.typeResists)

quest = Quest(fakebot, 0, 0, p1)
quest.engagedParty = [p2]

print('\n'.join([p.name for p in party]))
printc(quest.trainer.as_text(dex) + '\n\n')

for i in range(5):
    print(f'-- Attack {i+1} / Turn {quest.trainer.turnsElapsed} --')
    result = quest.battle_step(ATTACK, 0)
    p = quest.trainer.activePkmn
    summary = f'''{typeEmoji[p.type]}{p.name} used _{p.move}_!'''
    if result['log'] and result['log'][0][0] == ENEMY_DAMAGED:
        _, e, hits, dmg, hpTaken, xType, *rest = result['log'][0]
        summary = f"{typeEmoji[p.type]}{p.name}'s _{p.move}_ deals **{dmg}** dmg!"


    printc(quest.trainer.as_text(dex, result['trainer_buff_snapshot']))
    print(quest.trainer.buffs)
    printc('\n' + summary)

    # for e in quest.enemyParty:
    #     printc(f'[E] {e.as_text()}\n\n')

    print('Enemy:')
    printc(quest.engagedParty[0].as_text(dex, result['enemy_buffs_snapshot'][0]))
    print(quest.engagedParty[0].buffs)
    print('\n\n')

    #printc(quest.enemy_party_as_text(result['enemy_buffs_snapshot']) + '\n\n')


print('\n\n**** Player 2\'s Turn\n\n\n')


quest = Quest(fakebot, 0, 0, p2)
quest.engagedParty = [p1]

print('\n'.join([p.name for p in party]))
printc(quest.trainer.as_text(dex) + '\n\n')

for i in range(5):
    print(f'-- Attack {i+1} / Turn {quest.trainer.turnsElapsed} --')
    result = quest.battle_step(ATTACK, 0)
    p = quest.trainer.activePkmn
    summary = f'''{typeEmoji[p.type]}{p.name} used _{p.move}_!'''
    if result['log'] and result['log'][0][0] == ENEMY_DAMAGED:
        _, e, hits, dmg, hpTaken, xType, *rest = result['log'][0]
        summary = f"{typeEmoji[p.type]}{p.name}'s _{p.move}_ deals **{dmg}** dmg!"


    printc(quest.trainer.as_text(dex, result['trainer_buff_snapshot']))
    print(quest.trainer.buffs)
    printc('\n' + summary)

    # for e in quest.enemyParty:
    #     printc(f'[E] {e.as_text()}\n\n')

    print('Enemy:')
    printc(quest.engagedParty[0].as_text(dex, result['enemy_buffs_snapshot'][0]))
    print(quest.engagedParty[0].buffs)
    print('\n\n')

    #printc(quest.enemy_party_as_text(result['enemy_buffs_snapshot']) + '\n\n')




# no = random.choice([1, 2, 5, 6, 10, 11, 14])
# wp = WildPokemon(no, 5, self.bot.dex.pkmn[no])
# location = 0
# quest = PokemonEncounter(self.bot, ctx.author.id, trainer, wp, location)
# await quest.build_and_send_message(ctx)
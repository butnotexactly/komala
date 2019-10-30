import importlib
import sys
import traceback
import sqlite3
import re

from battle import *
from common import *

import explore

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
    #text = re.sub(r'<(:.*?:)[0-9]*>', r'\1', text)
    text = re.sub(r'<(:.*?:)[0-9]*>', ' ', text)
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


boosts = deckBoosts[deckKeys[0]]
multis = (1.1, 1.2, 1.3, 1.4, 1.5)


pkmn = []
nos = dex.sample_from_set(6, 1)
for no in nos:
    #p = fakebot.pc.make_pkmn(no=no, lv=20)
    p = fakebot.pc.make_pkmn(name='Fletchinder', lv=20)
    pkmn.append(p)

#pkmn[0] = fakebot.pc.make_pkmn(name='Fletchinder', lv=20)
pkmn[3] = fakebot.pc.make_pkmn(name='Fletchinder', lv=20)

party = to_battle_pkmn(pkmn, boosts, multis)
trainer = TrainerState(party)

quest = Quest(fakebot, 0, 0, trainer)
quest.enemyParty = []
for i in range(1):
    no, = dex.sample_from_set(1)
    e = explore.WildPokemon(no, 45, dex.pkmn[no])
    #e.hpMax = e.hp = 50000
    quest.enemyParty.append(e)

print('\n'.join([p.name for p in party]))
printc(quest.trainer.as_text(dex) + '\n\n')

for i in range(6):
    print(f'-- Attack {i+1} / Turn {trainer.turnsElapsed} --')
    result = quest.battle_step(ATTACK, 0)
    p = quest.trainer.activePkmn
    dmg = result['log'][0][-2]
    summary = f"{typeEmoji[p.type]}{p.name}'s _{p.move}_ deals **{dmg}** dmg!"
    printc(quest.trainer.as_text(dex))
    printc('\n' + summary)

    # for e in quest.enemyParty:
    #     printc(f'[E] {e.as_text()}\n\n')

    printc(quest.enemy_party_as_text(result['enemy_buffs_snapshot']) + '\n\n')


# no = random.choice([1, 2, 5, 6, 10, 11, 14])
# wp = WildPokemon(no, 5, self.bot.dex.pkmn[no])
# location = 0
# quest = PokemonEncounter(self.bot, ctx.author.id, trainer, wp, location)
# await quest.build_and_send_message(ctx)
import random
import secrets
import discord
import random
import math
import copy

from numpy import interp

from pokedex import *
from common import *

ATK_BUFFS = (1, 1.18, 1.33, 1.47, 1.57, 1.67, 1.77, 1.87)
DEF_BUFFS = (1, 1.18, 1.33, 1.47, 1.57, 1.67, 1.77, 1.87)
DEF_DEBUFFS = (1, 0.8, 0.65, 0.5, 0.4, 0.3, 0.2, 0.1)
TYPE_ATK_BUFFS = (0, 0.25, 0.55, 0.9, 1.1, 1.3, 1.5, 1.7)
TYPE_DEF_BUFFS = (1, 0.88, 0.76, 0.64, 0.52, 0.4, 0.35, 0.3)
ACCURACY_STAGES = (9/3, 8/3, 7/3, 6/3, 5/3, 4/3, 3/3,
                   3/4, 3/5, 3/6, 3/7, 3/8, 3/9)

# PSM_TYPE_BONUS = (0.5, 0, -0.333333)

TYPE_RESISTANT = 0.5
TYPE_EFFECTIVE = 2

# CRIT_RATE = 0.06
CRIT_MULTI = 1.5
MIN_RAND, MAX_RAND = 0.97, 1.03

# CAP_AB = 5
# CAP_DB = 5
# CAP_TAB = 5
# CAP_TDB = 5


BAR_SIZE = 8

SKIP = 0
ATTACK = 1

PLAYER_TURN         = 0
PLAYER_TURN_END     = 1
ENEMY_TURN_END      = 2
PARTY_DEAD          = 3
PARTY_FLED          = 4
QUEST_COMPLETE      = 5
QUEST_FAILED        = 6

# Errors
ALREADY_DESTROYED   = 1
INVALID_TARGET      = 2

ERROR_TEXT = {
    ALREADY_DESTROYED: 'That Pokémon has already fainted.',
    INVALID_TARGET: 'There are no Pokémon with that number label! As an example, type `1` for the Pokémon labelled `[1]`.',
}


POISONED    = PSN
SEEDED      = SEED
BURNED      = BURN
PARALYZED   = PARA
FLINCHED    = FLINCH
SLEEPING    = SLP
WOKE        = -SLP
CONFUSED    = CONFUSE
SNAPPED     = -CONFUSE
CHARMED     = CHARM
DECHARMED   = -CHARM
KILLED      = 20

X2_STATUS   = 100

SKIP_PKMN         = 0
NO_PP             = 1
USE_PKMN          = 2
ENEMY_DAMAGED     = 3
ONE_TURN_TRIUMPH  = 4
PP_RESTORE        = 5
TM_PROC           = 6

MISSED = 1


def hp_bar(hp, hpMax, hpPerBar=BAR_SIZE, bars=None):
    if bars:
        hpPerBar = int(hpMax / bars)
    else:
        bars = int(hpMax / hpPerBar)
        if bars < 3:
            bars = 3
            hpPerBar = int(hpMax / bars)
        # elif bars > 7:
        #     bars = 7
        #     hpPerBar = int(hpMax / bars)
        # elif bars > 12:
        #     bars = 12
        #     hpPerBar = int(hpMax / bars)

    if hp == hpMax:
        barFilled = bars
    elif hp == 0:
        barFilled = 0
    else:
        barFilled = max(1, int(hp / hpPerBar))
    return ''.join(['▰' if i < barFilled else '▱' for i in range(bars)])

def shake_check(catchRate, hp, hpMax, xBall=1, xStatus=1):
    # a
    modifiedCatchRate = xStatus * (((3 * hpMax - 2 * hp) * catchRate * xBall) /
                                        (3 * hpMax))
    if modifiedCatchRate >= 255:
        return 1

    # b (probability)
    b = (65536 / (255 / modifiedCatchRate)**0.1875) / 65536

    return secrets.randbelow(10000) < b * 10000

def update_buffs(buffs, steps=1, hasDefended=False):
    for buff in buffs:
        buff.duration -= steps
    buffs[:] = [buff for buff in buffs if buff.duration > 0 or (buff.is_defensive() and not hasDefended)]

def get_flat_buff(buffs):
    flat = Buff()
    for b in buffs:
        flat.add(b)
    flat.balance()
    flat.cap(5, 5, 5, 5)
    return flat

def status_as_text(statuses):
    if statuses:
        return f'''  {''.join([statusEmoji[s] for s in statuses.keys()])}'''
    return ''

def status_log_as_text(log, e=None):
    texts = []
    for event in log:
        if event[0] == BURN:
            if e: texts.append(f'{statusEmoji[BURN]} It was hurt by its burn! [-**{event[1]}** HP]')
            else: texts.append(f'{statusEmoji[BURN]} Your party was hurt by burn damage. [-**{event[1]}** HP]')
        elif event[0] == PSN:
            if e: texts.append(f'{statusEmoji[PSN]} It was hurt by poison! [-**{event[1]}** HP]')
            else: texts.append(f'{statusEmoji[PSN]} Your party was hurt by poison. [-**{event[1]}** HP]')
        elif event[0] == SEED:
            texts.append(f'{statusEmoji[SEED]} **{event[1]}** HP was sapped by Leech Seed!')
    return '\n'.join(texts)

def ability_notations_as_text(p):
    texts = []


    # if multi is not None:
    #     if multi != medal.multiHigh:
    #         notations.append('Weakened multiplier!')# {} {}'.format(medal.castedMulti, medal.multiHigh))
    #     elif multi != medal.multiLow and multi == medal.multiHigh:
    #         notations.append('Perfect multiplier!')# {} {} {}'.format(medal.castedMulti, medal.multiLow, medal.multiHigh))

    # if AbilityFlag.CURE in medal.abilityFlag:
    #     notations.append('Slightly recovered HP.')
    # elif AbilityFlag.CURA in medal.abilityFlag:
    #     notations.append('Moderately recovered HP.')
    # elif AbilityFlag.CURAGA in medal.abilityFlag:
    #     notations.append('Greatly recovered HP!')
    # elif AbilityFlag.CURAJA in medal.abilityFlag:
    #     notations.append('Significantly recovered HP!')

    # if AbilityFlag.MIRROR in medal.abilityFlag:
    #     notations.append('Mirrored the target enemy\'s buffs!')
    # elif AbilityFlag.DISPEL in medal.abilityFlag:
    #     notations.append('Dispelled the target enemies\' buffs!')

    # if medal.spRestore:
    #     notations.append('Restored {} SP!'.format(medal.spRestore))

    if texts:
        return '\n{}'.format(' '.join(texts))

    return ''

def get_pp_restores(party, caster, dexEntry):
    ppp = dexEntry['pp+']

    restores = [0] * len(party)
    for i, p in enumerate(party):
        if p:
            restores[i] += ppp['all']

    for t, pp in enumerate(ppp['type']):
        if pp:
            for i, p in enumerate(party):
                if not p: continue
                pt = p.type if isinstance(p, BattlePokemon) else p.type()
                if pt == t:
                    restores[i] += pp

    for slot, _ in enumerate(party):
        if party[slot]:
            pp = ppp['slot'][slot]
            restores[slot] += pp

    if 'notself' in ppp:
        restores[party.index(caster)] = 0
    elif 'self' in ppp:
        restores[party.index(caster)] += ppp['self']

    return restores

def apply_pp_restores(party, caster):
    restores = get_pp_restores(party, caster, caster.dexEntry)
    for i, pp in enumerate(restores):
        if party[i]:
            party[i].restore_pp(pp)

    return restores

def pp_restores_as_text(party, restores):
    return '💛 _PP Restored!_ ' + ''.join([f"{party[i].dexEntry['emoji']}+**{pp}**" for i, pp in enumerate(restores) if pp])


def pre_attack_status_check(attacker, defender, sleeptalk):
    results = []
    if SLEEPING in attacker.statuses:
        # komala check todo cleanup
        if not hasattr(attacker, 'no') or attacker.no not in [14]:
            attacker.statuses[SLEEPING] -= 1
            if attacker.statuses[SLEEPING] > 0 and not sleeptalk:
                results.append(SLEEPING)
                return results
            else:
                del attacker.statuses[SLEEPING]
                results.append(WOKE)

    if PARALYZED in attacker.statuses:
        if random.random() < 0.25:
            results.append(PARALYZED)
            return results

    if CHARMED in attacker.statuses:
        if attacker.statuses[CHARMED] > 0:
            attacker.statuses[CHARMED] -= 1
            if random.random() < 0.5:
                results.append(CHARMED)
                return results
        else:
            del attacker.statuses[CHARMED]
            results.append(DECHARMED)

    if FLINCH in attacker.statuses:
        results.append(FLINCHED)
        return results

    if CONFUSED in attacker.statuses:
        if attacker.statuses[CONFUSED] > 0:
            attacker.statuses[CONFUSED] -= 1
            if random.random() < 1/3:
                confuseDmg = min(attacker.hp, int(attacker.hpMax / 8))
                attacker.hp -= confuseDmg
                results.append(CONFUSED)
                return results
        else:
            del attacker.statuses[CONFUSED]
            results.append(SNAPPED)

    # todo make work for player vs enemy
    if defender and defender.blocks:
        block = defender.blocks[0]
        block[0] -= 1
        if block[0] <= 0:
            del defender.blocks[0]
        results.append(block[1])
        return results

    return results


def post_attack_status_update(attacker):
    attacker.statuses.pop(FLINCH, None)
    log = []
    remove = []
    for status, data in attacker.statuses.items():
        if status == BURN:
            burnDmg = min(attacker.hp, int(0.0625 * attacker.hpMax))
            attacker.hp -= burnDmg
            log.append([BURN, burnDmg])

        elif status == PSN:
            psnDmg = min(attacker.hp, int(attacker.hpMax/18))
            attacker.hp -= psnDmg
            log.append([PSN, psnDmg])

        elif status == SEED:
            seeder = data
            if seeder.hp > 0:
                seedDmg = min(attacker.hp, int(0.125 * attacker.hpMax))
                attacker.hp -= seedDmg
                seeder.restore_hp(seedDmg)
                log.append([SEED, seedDmg, seeder])
            else:
                remove.append(status)

    for status in remove:
        attacker.statuses.pop(status, None)

    return log


class TrainerState(object):
    def __init__(self, party, pvp=False):
        self.hpMax = 0
        self.buffs = []
        self.flatBuff = None

        self.statuses = {}
        # self.statuses = {
        #     PSN: True,
        #     BURN: True,
        #     PARA: True,
        #     FLINCH: True,
        #     SLP: 4,
        #     CONFUSE: 4,
        #     CHARM: 4
        #     #SEED:
        # }

        self.attackNo = 0
        self.movesUsed = 0
        self.turnsElapsed = 0
        self.killCount = 0

        self.activePkmn = None
        #self.currentBattle = None
        #self.practiceSession = False
        # self.meta = None

        self.party = party
        partyTypes = [p.type for p in self.party if p]

        self.pvp = pvp
        if pvp:
            self.typeResists = get_type_resistances(partyTypes, low=0.25, high=2.8)
        else:
            self.typeResists = get_type_resistances(partyTypes, low=0.4, high=2.8)
        self.typeCounts = [partyTypes.count(t) for t in range(11)]

        # status resist
        self.attacksPerTurn = len(party)
        self.dropChance = 0
        self.applyTotemBonus = False

        self.evasionStage = 0
        self.accuracyStage = 0
        self.critBonus = 0
        self.defense = 0
        self.blocks = []

        zBonus = [0] * 11
        for p in self.party:
            if not p:
                continue
            self.hpMax += p.hp
            self.defense += p.defense

            # todo move
            if 'passive_buff' in p.dexEntry:
                b = p.dexEntry['passive_buff'].as_self_buff()
                if not b.is_zero():
                    self.buffs.append(b)

                # b = p.dexEntry['passive_buff'].as_target_buff()
                # if not b.is_zero():
                #     for e in self.engagedParty:
                #     self.buffs.append(b)

            if 'z_bonus' in p.dexEntry:
                zBonus = [zBonus[i] + zb for i, zb in enumerate(p.dexEntry['z_bonus'])]

            if 'block' in p.dexEntry:
                self.blocks.append(copy.copy(p.dexEntry['block']))

        if any(zBonus):
            for p in self.party:
                if p:
                    p.z += zBonus[p.type]
                    p.xZ = 1 + p.z/100

        self.defense /= len(self.party)

        if self.buffs:
            self.refresh_flat_buff()

        # for m in medals:
        #     #Guzma / Ava
        #     if m.n in common.PROMO:
        #        player.practiceGame = True

        #     if m.traits:
        #         # player.paraResist += m.traits.count(common.Trait.PARA.value) * 0.6
        #         # player.poisonResist += m.traits.count(common.Trait.POISON.value) * 0.6
        #         # player.sleepResist += m.traits.count(common.Trait.SLEEP.value) * 0.6
        #         player.paraResist += m.traits.count(common.Trait.STATUS.value) * 0.5
        #         player.poisonResist += m.traits.count(common.Trait.STATUS.value) * 0.5
        #         player.sleepResist += m.traits.count(common.Trait.STATUS.value) * 0.5
        #         player.burnResist += m.traits.count(common.Trait.STATUS.value) * 0.5
        #         player.frozenResist += m.traits.count(common.Trait.STATUS.value) * 0.5

        #         player.hpMax += m.traits.count(common.Trait.HP.value) * 800
        #         player.maxSp += m.traits.count(common.Trait.SP.value) * 2
        #         player.dropChance += m.traits.count(common.Trait.RAID.value)
        #         if common.Trait.DC.value in m.traits:
        #             player.attacksPerTurn += 1

        self.hp = self.hpMax

    def refresh_flat_buff(self):
        self.flatBuff = get_flat_buff(self.buffs)
        return self.flatBuff

    def update_current_pkmn(self):
        self.activePkmn = self.party[self.attackNo % self.attacksPerTurn]

    def exit_battle(self):
        self.turnsElapsed = self.movesUsed = self.attackNo = 0
        #self.para = self.poison = self.sleep = 0
        self.buffs = []
        #self.statuses = {}
        self.evasionStage = 0
        self.accuracyStage = 0

    def restore_hp(self, hp):
        self.hp = min(self.hpMax, self.hp + hp)

    def as_text(self, dex, buff=None, showParty=True, showHp=True, boldBuffs=False):
        buff = buff or self.flatBuff
        miniParty = []
        parts = []

        singlePkmn = len(self.party) - self.party.count(None) == 1

        if showParty:
            if singlePkmn:
                p = next(p for p in self.party if p is not None)
                mini = dex.emoji(p.no)
                pp = p.pp
                ppMax = p.ppMax
                #⚠
                #parts.append(f'{mini}`{pp}/{ppMax}` {typeEmoji[p.type]}{p.name} [Lv. **{p.lv}**]')
                #parts.append(f'[Lv. **{p.lv}**]{mini}{p.name}  PP:  {pp} / {ppMax}')
                hpBar = f'HP:  `{hp_bar(self.hp, self.hpMax)}`  {self.hp}  /  {self.hpMax}'
                ppWarning = ' ⚠' if p.pp < p.ppCost else ''
                parts.append(f'{mini}{p.name}   PP:  `{pp} / {ppMax}`{ppWarning}\n{typeEmoji[p.type]}Lv. **{p.lv}**  ♂   {hpBar}')


            else:
                for i, p in enumerate(self.party):
                    if p:
                        mini = dex.emoji(p.no)
                        pp = p.pp
                        ppMax = p.ppMax
                        part = f'{mini}`{pp}/{ppMax}`'
                        if p == self.activePkmn:
                            part = f'[{part}]'
                    else:
                        part = f'''{pokemoji['pkmn_spacer']}`-/-`'''

                    if i == 2:
                        part += '\n'

                    miniParty.append(part)
                parts.append(''.join(miniParty))

        if showHp and not singlePkmn:
            parts.append(f'HP:  `{hp_bar(self.hp, self.hpMax, bars=9)}`  {self.hp}  /  {self.hpMax}')
        status = status_as_text(self.statuses)
        if status:
            parts.append(status)
        if buff and not buff.is_zero():
            parts.append(buff.as_text(boldBuffs))

        return '\n'.join(parts) + '\n' + hmSpacer#'\n\u200bf'#+ FIELD_BREAK

    def apply_damage(self, dmg):
        dmg = int(dmg)
        startHp = self.hp
        self.hp = max(0, self.hp - dmg)
        hpTaken = startHp - self.hp
        # self.hp = startHp
        # todo remove invuln for pvp?
        return dmg, hpTaken


class BattlePokemon(object):
    def __init__(self, pcPkmn, slotPosition, xSlot):

        self.dexEntry = pcPkmn.dex.pkmn[pcPkmn.no]
        self.no = pcPkmn.no
        self.name = base_name(pcPkmn.format_name(key='name'))
        self.emoji = self.dexEntry['emoji']
        self.slot = slotPosition
        self.xSlot = xSlot

        self.lv = pcPkmn.lv
        self.statLv = pcPkmn.statLv
        self.move = self.dexEntry['move']
        self.tm = pcPkmn.tm
        self.hms = pcPkmn.hms if pcPkmn.hms else []
        self.attack = pcPkmn.attack()
        self.defense = pcPkmn.defense()
        self.type = pcPkmn.type()
        self.target = self.dexEntry['target']
        self.tier = self.dexEntry['tier'] + pcPkmn.tplus
        self.ppCost = self.dexEntry['pp_cost']
        self.gender = self.dexEntry['gender']
        self.wtClass = self.dexEntry['wt_class']

        self.hp = pcPkmn.hp()
        self.pp = self.ppMax = pcPkmn.pp()
        self.critRate = pcPkmn.crit_rate()
        self.xMin = self.dexEntry['x_min']
        self.xMax = self.dexEntry['x_max']

        self.z = pcPkmn.z if pcPkmn.z else 0
        self.xZ = 1 + self.z/100

        self.charge = 0
        self.recharge = 0
        self.sleeptalk = self.dexEntry['sleeptalk'] if 'sleeptalk' in self.dexEntry else False

        # if pcPkmn.delta and pcPkmn.z:
        #     self.xZ += 0.45

        # self.tier = medalData['tier'] + invMedal.tplus


        #self.counterIncrement = medalData['counterIncrement']
        #self.addAttribute = medalData['addAttribute']

        # if medalData['buffDuration'] > 0:
        #     self.baseDuration = medalData['buffDuration']
        #     self.buff = Buff()
        #     self.buff.gau = medalData['buffGau']
        #     self.buff.pBuff = medalData['buffP']
        #     self.buff.sBuff = medalData['buffS']
        #     self.buff.mBuff = medalData['buffM']

        #     self.buff.pdBuff = medalData['buffPd']
        #     self.buff.sdBuff = medalData['buffSd']
        #     self.buff.mdBuff = medalData['buffMd']

        #     self.buff.gdd = medalData['debuffGdd']
        #     self.buff.pdDebuff = medalData['debuffP']
        #     self.buff.sdDebuff = medalData['debuffS']
        #     self.buff.mdDebuff = medalData['debuffM']

        #     if medalData['buffGd']:
        #         self.buff.pdBuff = medalData['buffGd']
        #         self.buff.sdBuff = medalData['buffGd']
        #         self.buff.mdBuff = medalData['buffGd']

        #     self.apply_buff_trait()
        # else:
        #     self.baseDuration = None
        #     self.buff = None

    def type(self):
        return self.type

    def restore_pp(self, pp):
        self.pp = min(self.ppMax, self.pp + pp)

    # def apply_buff_trait(self):

    #     psmUpBuffs = ['pBuff', 'sBuff', 'mBuff']
    #     psmDownBuffs = ['pdDebuff', 'sdDebuff', 'mdDebuff']
    #     psmDefBuffs = ['pdBuff', 'sdBuff', 'mdBuff']

    #     if common.Trait.BUFF.value in self.traits and not common.Trait.DC.value in self.traits:
    #         self.originalBuff = copy.copy(self.buff)
    #         buffTypes = [self.buff.gau,
    #             max([getattr(self.buff, key) for key in psmDefBuffs]),
    #             max([getattr(self.buff, key) for key in psmUpBuffs]),
    #             max([getattr(self.buff, key) for key in psmDownBuffs]),
    #             self.buff.gdd]

    #         # Least Significant Buff
    #         lsbType = None
    #         lsbValue = 100
    #         for i, value in enumerate(buffTypes):
    #             if value > 0 and value < lsbValue:
    #                 lsbType = i
    #                 lsbValue = value

    #         if lsbType is not None:

    #             if lsbType == 0:
    #                 self.buff.gau += 1

    #             elif lsbType == 1:
    #                 if len(set([getattr(self.buff, key) for key in psmDefBuffs])) == 1:
    #                     for b in psmDefBuffs:
    #                         self.buff.__dict__[b] += 1
    #                 else:
    #                     random.shuffle(psmDefBuffs)
    #                     for b in psmDefBuffs:
    #                         if self.buff.__dict__[b] > 0:
    #                             self.buff.__dict__[b] += 1
    #                             break


    #             elif lsbType == 2:
    #                 if len(set([getattr(self.buff, key) for key in psmUpBuffs])) == 1:
    #                     for b in psmUpBuffs:
    #                         self.buff.__dict__[b] += 1
    #                 else:
    #                     random.shuffle(psmUpBuffs)
    #                     for b in psmUpBuffs:
    #                         if self.buff.__dict__[b] > 0:
    #                             self.buff.__dict__[b] += 1
    #                             break

    #             elif lsbType == 3:
    #                 if len(set([getattr(self.buff, key) for key in psmDownBuffs])) == 1:
    #                     for b in psmDownBuffs:
    #                         self.buff.__dict__[b] += 1
    #                 else:
    #                     random.shuffle(psmDownBuffs)
    #                     for b in psmDownBuffs:
    #                         if self.buff.__dict__[b] > 0:
    #                             self.buff.__dict__[b] += 1
    #                             break

    #             elif lsbType == 4:
    #                 self.buff.gdd += 1


    def offensive_tm_proc(self):
        return False

    #     if self.skill in [Skill.PARA.value, Skill.POISON.value, Skill.SLEEP.value]:
    #         #return random.random() <= 0.45
    #         return True

    #     if self.skill == Skill.APP.value:
    #         return random.random() <= 0.42 + 0.03

    #     try:
    #         if khux.isJacob:
    #             return -1 <= common.abData[self.skill][1]
    #         return random.random() <= common.abData[self.skill][1] + 0.03
    #     except KeyError:
    #         pass

    #     return False

    def defensive_tm_proc(self):
        return False
    #     try:
    #         return random.random() <= common.dbData[self.skill][1] + 0.03
    #     except KeyError:
    #         return False

    # def get_imbue_buff(self):
    #     buff = Buff()
    #     buff.addAttribute = self.addAttribute
    #     buff.duration = int((self.addAttribute - 1) / 3) + 1
    #     #common.debug_msg(buff.addAttribute, buff.duration)
    #     return buff

def accuracy(accuracyStage, evasionStage):
    stage = clamp(accuracyStage - evasionStage, -6, 6)
    return ACCURACY_STAGES[stage + 6]


class Quest(object):
    def __init__(self, bot, uid, qid, trainer):
        self.bot = bot
        self.uid = uid
        self.qid = qid
        self.trainer = trainer
        #self.parties = parties # class engagedParty()
        #self.engagedParty = None
        self.engagedParty = None
        #self.status = PLAYER_TURN
        self.storms = {}

    async def handle_reaction(self, reaction, user):
        print(f'Handled {reaction} for {user}')

    def skip_blank_steps(self):
        self.trainer.update_current_pkmn()
        while not self.trainer.activePkmn:
            self.battle_step(None, None)
            self.trainer.update_current_pkmn()

    def battle_step(self, action, target, auto=False, simulated=False):
        result = {
            'success': False,
            'status': PLAYER_TURN,
            'error': 0,
            'pkmn': None,
            'log': [],
            'range_quality': None,
            'trainer_buff_snapshot': None,
            'enemy_buffs_snapshot': None,
            #'applied_buff': None
        }

        self.trainer.update_current_pkmn()
        result['pkmn'] = p = self.trainer.activePkmn
        turnAttackNo = self.trainer.attackNo % self.trainer.attacksPerTurn

        # start of turn
        if turnAttackNo == 0:
            self.trainer.movesUsed = 0
            if self.trainer.attackNo > 0:
                self.trainer.turnsElapsed += 1

        # last pkmn before end turn
        if turnAttackNo == self.trainer.attacksPerTurn - 1:
            result['status'] = PLAYER_TURN_END

        tmProc = False
        damageTotal = 0

        if not p:
            pass
        elif action == SKIP:
            p.restore_pp(2)
            result['log'].append([SKIP_PKMN, None])
        elif p.recharge > 0:
            p.recharge -= 1
            result['log'].append([SKIP_PKMN, 'recharge'])
        elif p.pp < p.ppCost:
            p.restore_pp(2)
            result['log'].append([SKIP_PKMN, NO_PP])
        else:
            checkResults = pre_attack_status_check(self.trainer, None, p.sleeptalk)
            if checkResults:
                for r in checkResults:
                    result['log'].append(['pre_check', r])

            if not checkResults or checkResults[-1] in [WOKE, SNAPPED, DECHARMED]:
                targetEnemies = []
                xModifier = xTM = 1.0
                filteredHits = None
                if p.target == ST:
                    try:
                        if auto:
                            while self.engagedParty[target].hp == 0:
                                target += 1
                        targetEnemies = [self.engagedParty[target]]
                        if targetEnemies[0].hp == 0:
                            result['error'] = ALREADY_DESTROYED
                            return result

                    except (TypeError, IndexError) as e:
                        result['error'] = INVALID_TARGET
                        return result
                elif p.target == RAND:
                    liveEnemies = [e for e in self.engagedParty if e.hp > 0]
                    filteredHits = [secrets.choice(liveEnemies) for hit in range(p.dexEntry['hits'])]
                    targetEnemies = self.engagedParty
                elif p.target == AOE:
                    targetEnemies = self.engagedParty

                tmProc = p.offensive_tm_proc()
                if tmProc:
                    result['log'].append(TM_PROC)
                    try:
                        xTM = 1#common.abData[currentMedal.skill][0] TODO Tm
                    except KeyError:
                        pass

                # if result['dc2']:
                #     xModifier = 0.4
                if self.trainer.applyTotemBonus:
                    xModifier *= 1 + p.hms.count(HM.TOTEM) * 0.4

                result['success'] = True
                # if 'buff' in self.bot.dex.pkmn[p.no]:
                #     result['applied_buff'] = self.bot.dex.pkmn[p.no]['buff']

                genericAtk = False
                if SLEEPING in self.trainer.statuses and p.sleeptalk == 2:
                    targetEnemies = self.engagedParty
                    genericAtk = True
                    result['generic'] = 'sleeptalk'

                if genericAtk:
                    damages, rangeQuality = self.process_generic_attack(p, targetEnemies, xTM, xModifier)
                else:
                    damages, rangeQuality = self.process_attack(p, targetEnemies, xTM, xModifier, filteredHits, result['log'])

                result['range_quality'] = rangeQuality

                for i, e in enumerate(targetEnemies):
                    if e.hp == 0:
                        continue

                    dmg, criticalHit = damages[i]
                    hits = 1
                    if p.target == RAND:
                        hits = filteredHits.count(e)
                        dmg = dmg * (hits / p.dexEntry['hits'])
                        #if hits > 0: d = max(1, d)
                    else:
                        hits = 1

                    if not hits:
                        continue

                    x2s = []
                    if not genericAtk and 'x2_status' in p.dexEntry:
                        for status, multi in enumerate(p.dexEntry['x2_status']):
                            if dmg and status in e.statuses:
                                dmg *= multi
                                x2s.append(status * X2_STATUS)

                    # spRestore = restoreFact = 0
                    # if enemy.name == 'Chest':
                    #     enemy.hp = 0
                    # elif enemy.absorbs(currentMedal):
                    #     enemy.hp = min(enemy.hpMax, enemy.hp + damage)
                    # else:

                    dmg, hpTaken, damageNote = e.apply_damage(dmg, self.trainer)
                    damageTotal += dmg

                    # TODO hp / pp restore from hits
                    #     restoreFactor = (startHp - enemy.hp) / enemy.hpMax
                    #     spRestore = round(restoreFactor * 0.5, 2)

                    try:
                        xType = e.typeResists[p.type]
                    except AttributeError:
                        xType = typeChart[p.type][e.type]

                    enemyLog = [ENEMY_DAMAGED, e, hits, dmg, hpTaken, xType, criticalHit, damageNote] + x2s

                    if e.hp == 0:
                        e.on_death()
                        enemyLog.append(KILLED)
                    elif not genericAtk:
                        self.apply_attack_fx(p, e, tmProc, enemyLog)

                    try:
                        if e.timer > 0:
                            e.timer = max(0, e.timer - 1) #hits
                            enemyLog.append('t' + str(e.timer))
                            if e.timer == 0:
                                e.timer = e.timerReset
                                result['status'] = PLAYER_TURN_END
                    except AttributeError:
                        pass

                    # spRestoreTotal += spRestore
                    result['log'].append(enemyLog)

                if not genericAtk and 'status_self' in p.dexEntry:
                    for status, value in enumerate(p.dexEntry['status_self']):
                        if value:
                            if status == SLP:
                                self.trainer.statuses[SLEEPING] = random.randint(1, 4)
                            elif status == CONFUSE:
                                self.trainer.statuses[CONFUSED] = random.randint(1, 4)
                            result['log'].append(['status_self', status])

                        #todo add others

                # if skillActivated and currentMedal.skill in [Skill.APP.value, Skill.AB1APP.value, Skill.AB2APP.value,
                #     Skill.AB3APP.value, Skill.AB4APP.value, Skill.AB5APP.value, Skill.AB6APP.value]:
                #     spRestoreTotal = max(random.uniform(1.8, 2.2), math.log(max(0.1, spRestoreTotal) * 15, 2))

        statusLog = post_attack_status_update(self.trainer)
        if statusLog:
            result['log'].append(status_log_as_text(statusLog))
        self.apply_storms(p, result['log'])

        self.trainer.refresh_flat_buff()
        result['trainer_buff_snapshot'] = self.trainer.flatBuff
        update_buffs(self.trainer.buffs)

        result['enemy_buffs_snapshot'] = []
        for e in self.engagedParty:
            try:
                e.refresh_flat_buff()
                result['enemy_buffs_snapshot'].append(e.flatBuff)
            except AttributeError:
                result['enemy_buffs_snapshot'].append(get_flat_buff(e.buffs))
            update_buffs(e.buffs)

        stillAlive = sum(e.hp > 0 for e in self.engagedParty)
        # if stillAlive == 0 and trainer.turnsElapsed == 0:
        #     spRestoreTotal += 2
        #     result['log'].append(ONE_TURN_TRIUMPH)

        # if spRestoreTotal > 0:
        #     hpRestoreTotal = round(interp(spRestoreTotal, [0, 20], [0, 5000]))
        #     state.sp = min(state.maxSp, round(state.sp + spRestoreTotal, 2))
        #     state.hp = min(state.hpMax, state.hp + hpRestoreTotal)
        #     result['log'].append([SP_RESTORE, hpRestoreTotal, spRestoreTotal])

        if stillAlive == 0:
            if self.trainer.turnsElapsed == 0:
                # for p in self.trainer.party:
                #     if p: p.restore_pp(1)
                result['log'].append([ONE_TURN_TRIUMPH])

            result['status'] = PARTY_DEAD
            self.trainer.exit_battle()
        else:
            # end of attack update
            self.trainer.attackNo += 1
            # if result['status'] == PLAYER_TURN_END:
            #     self.trainer.turnsElapsed += 1

        return result

    def process_attack(self, p, targetEnemies, xTM, xModifier, filteredHits, log):

        trainer = self.trainer
        trainer.movesUsed += 1
        turnAttackNo = trainer.attackNo % trainer.attacksPerTurn

        p.pp = min(p.ppMax, p.pp - p.ppCost)

        trainer.accuracyStage = clamp(trainer.accuracyStage + p.dexEntry['acc_buff'], -6, 6)
        trainer.evasionStage = clamp(trainer.evasionStage + p.dexEntry['evade_buff'], -6, 6)
        if 'crit+' in p.dexEntry:
            trainer.critBonus += p.dexEntry['crit+'] / 100

        b = None
        if 'buff' in p.dexEntry:
            b = p.dexEntry['buff']

            # localize relative duration

            duration = b.duration
            if duration >= 6:
                duration = int((duration / 6) * trainer.attacksPerTurn)

            if duration > trainer.attacksPerTurn:
                duration = duration - trainer.attacksPerTurn + (trainer.attacksPerTurn - turnAttackNo)
            else:
                duration = min(trainer.attacksPerTurn - turnAttackNo, duration)

            trainer.buffs.append(b.as_self_buff(duration))

        for e in targetEnemies:
            if filteredHits:
                hits = filteredHits.count(e)
                if hits > 0 and b:
                    e.buffs.append(b.as_target_buff(duration, min(2, hits)))
            else:
                if b: e.buffs.append(b.as_target_buff(duration))

            if filteredHits is None or hits > 0:
                e.accuracyStage = clamp(e.accuracyStage - p.dexEntry['acc_debuff'], -6, 6)
                e.evasionStage = clamp(e.evasionStage - p.dexEntry['evade_debuff'], -6, 6)

        damages = []
        for e in targetEnemies:
            xAbility = self.get_ability_x(p, e)
            criticalHit = random.random() < p.critRate + self.trainer.critBonus
            damage = self.damage_calc_vs(p, e, xAbility, p.xZ, xTM, criticalHit)
            damages.append([damage * xModifier, criticalHit])


        if 'pp+' in p.dexEntry:
            restores = apply_pp_restores(trainer.party, p)
            if restores:
                log.append(pp_restores_as_text(trainer.party, restores))

        if 'hp+' in p.dexEntry:
            trainer.restore_hp(int(trainer.hpMax * p.dexEntry['hp+']))
            log.append(['hp+', p.dexEntry['hp+']])

        if 'esuna' in p.dexEntry:
            trainer.statuses = {}
            log.append(['esuna'])

        if 'dispel' in p.dexEntry:
            e.accuracyStage = 0
            e.evasionStage = 0
            e.buffs = []
            log.append(['dispel'])

        if 'recoil' in p.dexEntry:
            recoil = p.dexEntry['recoil']
            if recoil == 100:
                dmg, hpTaken = trainer.apply_damage(trainer.hp - 1)
            else:
                dmg, hpTaken = trainer.apply_damage(trainer.hpMax * (recoil / 100))

            log.append(['recoil', hpTaken])

        if 'recharge' in p.dexEntry:
            p.recharge = p.dexEntry['recharge']

        if 'selfdestruct' in p.dexEntry:
            trainer.hp = 0

        # if 'protect' in p.dexEntry:
        #     self.trainer.blocks.append(copy.copy(p.dexEntry['block']))


        # Post Ability Changes TODO
        '''
        if attackType == ABILITY:

            # Lose Def
            if AbilityFlag.LOSE_DEF in medal.abilityFlag:
                defenseDebuff = Buff()
                defenseDebuff.gdd = 3
                defenseDebuff.duration = state.attacksPerTurn + (state.attacksPerTurn - attackNumThisTurn)
                state.buffs.append(defenseDebuff)

            # Lose HP
            if AbilityFlag.LOSE_HP in medal.abilityFlag:
                state.hp = 1
        '''

        rangeQuality = None
        return damages, rangeQuality

    def process_generic_attack(self, p, targetEnemies, xTM, xModifier=1.0, usePp=False):
        trainer = self.trainer
        trainer.movesUsed += 1
        turnAttackNo = trainer.attackNo % trainer.attacksPerTurn

        if usePp:
            p.pp = min(p.ppMax, p.pp - p.ppCost)

        damages = []
        for e in targetEnemies:
            xAbility = 1#self.get_ability_x(p, e)
            damage = self.damage_calc_vs(p, e, xAbility, p.xZ, xTM)
            damages.append([damage * xModifier, False])

        rangeQuality = None
        return damages, rangeQuality

    def get_ability_x(self, p, e):
        x = 1.0

        if 'condition' in p.dexEntry:
            tag, value = p.dexEntry['condition']

            if tag == 'kills':
                if value == 'more':
                    x = interp(self.trainer.killCount, [0, 3], [p.xMin, p.xMax])
                else:
                    x = interp(self.trainer.killCount, [0, 3], [p.xMax, p.xMin])

            elif tag == 'pp':
                if value == 'more':
                    x = interp(self.trainer.killCount, [p.pp + p.ppCost, p.ppMax], [p.xMin, p.xMax])
                else:
                    x = interp(self.trainer.killCount, [p.pp + p.ppCost, p.ppMax], [p.xMax, p.xMin])

            elif tag == 'turns':
                if value == 'more':
                    x = interp(self.trainer.turnsElapsed, [0, 5 if p.xMax > 2 else 3], [p.xMin, p.xMax])
                else:
                    x = interp(self.trainer.turnsElapsed, [0, 3], [p.xMax, p.xMin])

            elif tag == 'moves':
                if value == 'more':
                    x = interp(self.trainer.movesUsed, [1, 5], [p.xMin, p.xMax])
                else:
                    x = interp(self.trainer.movesUsed, [1, 5], [p.xMax, p.xMin])

            elif tag == 'hp':
                if value == 'more':
                    x = interp(self.trainer.hp, [1, self.trainer.hpMax], [p.xMin, p.xMax])
                else:
                    x = interp(self.trainer.hp, [1, self.trainer.hpMax], [p.xMax, p.xMin])

            elif tag == 'slot':
                if value == 'high':
                    x = interp(p.slot, [0, 4], [p.xMin, p.xMax])
                elif value == 'low':
                    x = interp(p.slot, [0, 4], [p.xMax, p.xMin])
                else:
                    slot = int(value)
                    x = p.xMax if p.slot == slot - 1 else p.xMin

            elif tag == 'enemies':
                n = len([e for e in self.trainer.party if e.hp > 0])
                if value == 'more':
                    x = interp(n, [1, 4], [p.xMin, p.xMax])
                elif value == 'less':
                    x = interp(n, [1, 4], [p.xMax, p.xMin])

            elif tag == 'party':
                if value.startswith('more_') or value.startswith('less_'):
                    try:
                        t = typeKeys.index(value[-2:])
                        if value.startswith('more_'):
                            x = interp(self.trainer.typeCounts[t], [0, 5], [p.xMin, p.xMax])
                        else:
                            x = interp(self.trainer.typeCounts[t], [0, 5], [p.xMax, p.xMin])
                    except IndexError:
                        pass

            elif tag == 'weight':
                if value == 'heavy':
                    x = interp(e.wtClass, [FEATHER, TITAN], [p.xMin, p.xMax])
                elif value == 'light':
                    x = interp(e.wtClass, [FEATHER, TITAN], [p.xMax, p.xMin])

        if p.target == ST:
            x *= 1.4

        return x


    def apply_attack_fx(self, p, e, tmProc, log):
        if 'status_inflict' in p.dexEntry:
            for status, chance in enumerate(p.dexEntry['status_inflict']):
                # todo scale flinch with use
                if chance and random.random() <= chance:

                    if status == CHARM:
                        if CHARMED in e.statuses or not can_breed(p, e):
                            continue
                        e.statuses[CHARMED] = random.randint(1, 4)

                    elif status == SLP:
                        if SLEEPING in e.statuses:
                            continue
                        e.statuses[SLEEPING] = random.randint(1, 4)

                    elif status == CONFUSE:
                        if CONFUSED in e.statuses:
                            continue
                        e.statuses[CONFUSED] = random.randint(1, 4)

                    elif status == SEED:
                        e.statuses[SEED] = self.trainer

                    else:
                        e.statuses[status] = True

                    log.append(status)

            #PSN, SEED, BURN, PARA, FLINCH, SLP = 0, 1, 2, 3, 4, 5

    def apply_storms(self, partyMember, log):

        if partyMember:
            if 'storm' in partyMember.dexEntry:
                if random.random() < partyMember.dexEntry['storm']:
                    stormType = 'sand' if partyMember.type == EARTH else 'hail'
                    if stormType in self.storms:
                        self.storms[stormType] += random.randint(3, 7)
                        if partyMember.type == EARTH:
                            log.append('🌪 _The sandstorm intensifies._')
                        else:
                            log.append('❄ _The hail storm intensifies._')
                    else:
                        self.storms[stormType] = random.randint(3, 7)
                        if partyMember.type == EARTH:
                            log.append(f'🌪 _{partyMember.name} started a sandstorm._')
                        else:
                            log.append(f'❄ _{partyMember.name} started a hail storm._')

        if 'hail' in self.storms:
            self.storms['hail'] -= 1

            if self.storms['hail'] == 0:
                del self.storms['hail']
                log.append('❄ _The hail subsides._')

            else:
                text = '❄ The hail rages!'
                if partyMember and partyMember.type == ICE:
                    text += f' {partyMember.name} is unaffected.'
                else:
                    self.trainer.apply_damage(int(self.trainer.hpMax / 16))

                for e in self.engagedParty:
                    if not e.type == ICE:
                        e.apply_damage(int(e.hpMax / 16), self.trainer)

                log.append(f'_{text}_')

        if 'sand' in self.storms:
            self.storms['sand'] -= 1

            if self.storms['sand'] == 0:
                del self.storms['sand']
                log.append('🌪 _The sandstorm subsides._')
            else:
                text = '🌪 The sandstorm rages!'
                if partyMember and partyMember.type == EARTH:
                    text += f' {partyMember.name} is unaffected.'
                else:
                    self.trainer.apply_damage(int(self.trainer.hpMax / 16))

                for e in self.engagedParty:
                    if not e.type == EARTH:
                        e.apply_damage(int(e.hpMax / 16), self.trainer)

                log.append(f'_{text}_')



    def damage_calc_vs(self, p, e, xAbility, xZ, xTM, criticalHit):

        if 'fixed_dmg' in p.dexEntry:
            fixed = p.dexEntry['fixed_dmg']
            if fixed > 0:
                return int(fixed * xAbility * xZ * xTM)

            factor = abs(fixed / 100)
            return int(e.hp * factor)

        tb = self.trainer.refresh_flat_buff()
        eb = get_flat_buff(e.buffs)

        # todo handle negatives
        atkBuff = max(0, tb.atkBuffs[0] - tb.atkDebuffs[0])
        defDebuff = 0
        typeBuff = max(0, tb.atkBuffs[p.type] - tb.atkDebuffs[p.type])
        typeDebuff = 0

        enemyDefBuff = eb.defBuffs[0] - eb.defDebuffs[0]
        if enemyDefBuff < 0:
            defDebuff = abs(enemyDefBuff)
            enemyDefBuff = 0

        enemyTypeDefBuff = eb.defBuffs[p.type] - eb.defDebuffs[p.type]
        if enemyTypeDefBuff < 0:
            typeDebuff = abs(enemyTypeDefBuff)
            enemyTypeDefBuff = 0

        try:
            xType = e.typeResists[p.type]
        except AttributeError:
            xType = typeChart[p.type][e.type]

        if HM.PIERCE in p.hms:
            pierceFactor = 0.75 # 25% Reduction
        else:
            pierceFactor = 1

        xSlot = p.xSlot
        try:
            print(f'\n{p.name} vs {e.name}')
        except AttributeError:
            pass

        damage = new_damage_formula(p.statLv, p.attack, xSlot, atkBuff, defDebuff, enemyDefBuff, e.defense, pierceFactor,
            typeBuff, typeDebuff, enemyTypeDefBuff, xType, xAbility, xZ, xTM, criticalHit, False) #todo turn on variation

        return max(0, damage)

    def enemy_party_as_text(self, buffs=None, hpPerBar=None, init=False):
        # todo clean

        texts = []
        inits = []

        hpSpacer = '  '
        if not hpPerBar:
            maxHp = max([e.hpMax for e in self.engagedParty])
            if maxHp < 140:
                hpPerBar = 8
            elif maxHp < 250:
                hpPerBar = 16
            else:
                hpSpacer = '\n'
                hpPerBar = 18

            # if maxHp / hpPerBar > 8:
            #     hpPerBar = maxHp / 8


            #def hp_bar(hp, hpMax, hpPerBar=BAR_SIZE, bars=None):

            #bars
            #avgHp = sum([e.maxHp for e in self.engagedParty]) / len(self.engagedParty)
            #barsize = int(max([e.hpMax for e in self.engagedParty]) / 6)

        if init:
            for i, e in enumerate(self.engagedParty):
                result = e.on_start(self.trainer)
                if result:
                    inits.append(result)

        for i, e in enumerate(self.engagedParty):
            #text = f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]}Lv. **{e.lv}**  ♂   HP:  `{hp_bar(e.hp, e.hpMax, 8):}`  {e.hp}  /  {e.hpMax}{status_as_text(e.statuses)}'''

            hpText = f'''{hpSpacer} `{hp_bar(e.hp, e.hpMax, hpPerBar):}`  {e.hp} / {e.hpMax}'''
            # if len(hpText) < 22:
            #     text = f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]}Lv. **{e.lv}**  {hpText}{status_as_text(e.statuses)}'''
            # else:
            text = f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]}Lv. **{e.lv}**{hpText}{status_as_text(e.statuses)}'''

            if e.hp > 0:
                buff = buffs[i] if buffs else get_flat_buff(e.buffs)
                if not buff.is_zero():
                    text += '\n' + buff.as_text()
            texts.append(text)

        text = '\n'.join(texts)

        if inits:
            #inits.insert(0, ' ')
            text += DBL_BREAK + '\n'.join(inits)

        if len(text) > 1024:
            print(len(text))
            text = shrink_emojis_to_fit(text, 1024)
            print(len(text))
            print(text)

        return text


def new_damage_formula(statLv, attack, xSlot, atkBuff, defDebuff, enemyDefBuff, enemyDef, pierceFactor,
    typeBuff, typeDebuff, enemyTypeDefBuff, xType, xAbility, xZ, xTM, criticalHit, applyVariation=True):

    defense = enemyDef * DEF_BUFFS[enemyDefBuff] * DEF_DEBUFFS[defDebuff] * pierceFactor
    #defense = enemyDef * DEF_DEBUFFS[defDebuff] * pierceFactor

    #base = int((((2 * lv/5 + 2) * (ATK_BUFFS[atkBuff] * attack * (xSlot * 100) - (defense * 100)) / defense) / 50) +2)
    #base = int((((2 * lv/5 + 2) * (ATK_BUFFS[atkBuff] * attack * (xSlot * 100) - (defense * 50)) / defense) / 50) +2)

    #base = int((((2 * lv/10 + 2) * (ATK_BUFFS[atkBuff] * attack * (xSlot * 100) - (defense * 50)) / defense) / 50) +2)
    #base = int((((2 * lv/10 + 2) * (ATK_BUFFS[atkBuff] * attack * (xSlot * 100)) / defense) / 50) +2)

    power = 100
    base = int((((2 * statLv/10 + 2) * (ATK_BUFFS[atkBuff] * attack * xSlot * power - (defense * 50)) / defense) / 50) +2)


    print(f'base[{base}] statlv:{statLv}, atkBuff:{atkBuff}, attack:{attack}, xSlot:{xSlot}')
    print(f'enemydef:{defense:.2f}')

    # note: alternative would be (1 + psmup + psmdown) * xType
    xTypeFactors = (1 + TYPE_ATK_BUFFS[typeBuff] + TYPE_ATK_BUFFS[typeDebuff] + (xType - 1))
    xBonus = xTypeFactors * xAbility * xZ * TYPE_DEF_BUFFS[enemyTypeDefBuff] * xTM

    damage = base * xBonus * 0.75

    print(f'base:{base}  +psm:{TYPE_ATK_BUFFS[typeBuff]}  -psm:{TYPE_ATK_BUFFS[typeDebuff]}  xType:{xType}  xTypeFactors:{xTypeFactors:.2f}  xBonus:{xBonus:.2f}  xZ:{xZ}')
    # if applyCrit and random.random() < CRIT_RATE:
    #     damage *= CRIT_MULTI
    #

    # if self.critRate and random.random() < self.critRate:
    #     damage *= CRIT_MULTI

    if criticalHit:
        damage *= CRIT_MULTI

    if applyVariation:
        damage = damage * random.uniform(MIN_RAND, MAX_RAND)
    print(f'total: {int(damage)}')
    return int(damage)


def khux_damage_formula(attack, xSlot, atkBuff, defDebuff, enemyDef, pierceFactor,
    typeBuff, typeDebuff, enemyTypeDefBuff, typeBonus, xAbility, xZ, xTM, applyCrit=False, applyVariation=True):

    atkCalc = attack * xSlot * ATK_BUFFS[atkBuff]
    defCalc = enemyDef * DEF_DEBUFFS[defDebuff] * pierceFactor
    xType = (1 + TYPE_ATK_BUFFS[typeBuff] + TYPE_ATK_BUFFS[typeDebuff] + typeBonus)
    #xBonus = xType * xAbility * xZ * TYPE_DEF_BUFFS[enemyTypeDefBuff] * xTM


    #alternatively, ((100 * xSlot) - x) or something, then xAtk
    #     return int(((((((((2 * e.lv/5 + 2) * e.attack * power) / trainer.defense) / 50) +2) * 1.5) * xType) * random.randint(217, 255))/255)


    damage = round(atkCalc - defCalc) * xType * xAbility * xZ * TYPE_DEF_BUFFS[enemyTypeDefBuff] * xTM
    #damage = round(((atkCalc - defCalc / 6) * xSlot) / defCalc) * xType * xAbility * xZ * TYPE_DEF_BUFFS[enemyTypeDefBuff] * xTM

    print(f'Extra Multi', xType * xAbility * xZ * TYPE_DEF_BUFFS[enemyTypeDefBuff] * xTM)

    print(f'xType {xType}: buff[{typeBuff}] {TYPE_ATK_BUFFS[typeBuff]} / debuff[{enemyTypeDefBuff}] {TYPE_ATK_BUFFS[enemyTypeDefBuff]} / typeBonus {typeBonus}')
    print(f'atk: {round(atkCalc)} / def: {round(defCalc)} / dmg: {round(damage)}')
    print('')

    # if applyCrit and random.random() <= CRIT_RATE:
    #     damage *= CRIT_MULTI
    #
    if applyVariation:
        damage = damage * random.uniform(MIN_RAND, MAX_RAND)

    return damage

def pkmn_damage_formula():
    return 0


def to_battle_pkmn(pcParty, boosts, xSlots):
    battleParty = []
    remove = []
    padding = 0
    for slot, p in enumerate(pcParty):
        if p:
            if padding:
                battleParty += [None] * padding
                padding = 0
            boosted = slot == 5 or boosts[slot][0] == NORMAL or p.type in boosts[slot]
            battleParty.append(BattlePokemon(p, slot, xSlots[slot] if boosted else 1))
        else: padding += 1
    return battleParty


class Battle:
    def __init__(self, bot):
        # self.db = db
        self.bot = bot
        self.userdb = bot.userdb
        self.quests = {}

    def add_quest(self, uid, data):
        if uid in self.quests:
            raise ValueError(f'❗ Error P1: Quest already exists for <@{uid}>')
        else:
            pass


def setup(bot):
    battle = Battle(bot)
    bot.add_cog(battle)
    bot.battle = battle
from common import *
from battle import *
import random

classMap = {}

actions = ['used', 'attacks with', 'strikes back using', 'counters with']
dex = None

def setup(bot):
    global dex
    dex = bot.dex

def get_damage(e, trainer, power, xType, pierceFactor=1):
    eb = get_flat_buff(e.buffs)
    tb = trainer.refresh_flat_buff()

    # todo handle negatives
    atkBuff = max(0, eb.atkBuffs[0] - eb.atkDebuffs[0])
    defDebuff = 0
    typeBuff = max(0, eb.atkBuffs[e.type] - eb.atkDebuffs[e.type])
    typeDebuff = 0

    vsDefBuff = tb.defBuffs[0] - tb.defDebuffs[0]
    if vsDefBuff < 0:
        defDebuff = abs(vsDefBuff)
        vsDefBuff = 0

    vsTypeDefBuff = tb.defBuffs[e.type] - tb.defDebuffs[e.type]
    if vsTypeDefBuff < 0:
        typeDebuff = abs(vsTypeDefBuff)
        vsTypeDefBuff = 0

    defense = max(1, trainer.defense * DEF_BUFFS[vsDefBuff] * DEF_DEBUFFS[defDebuff] * pierceFactor)
    damage = int(((((((((2 * e.statLv/10 + 2) * e.attack * power) / defense) / 50) +2) * 1.5) * xType) * random.randint(217, 255))/255)

    return int(damage * (1 + TYPE_ATK_BUFFS[typeBuff] + TYPE_ATK_BUFFS[typeDebuff]) * TYPE_DEF_BUFFS[vsTypeDefBuff])

def miss_result(move, action='used'):
    return {
        'move': move,
        'action': action,
        'failed': MISSED
    }

class Enemy(object):
    def __init__(self, no=None, lv=0, name=''):
        self.n = None
        self.no = no
        self.lv = lv
        self.statLv = lv / 1.5
        self.type = 0
        self.hpMax = 0
        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.evasionStage = 0
        self.accuracyStage = 0
        self.buffs = []
        self.statuses = {}
        self.name = name
        self.move = ''
        self.party = None
        self.gender = MALE
        self.wtClass = None
        self.faintMsg = None
        self.charge = 0
        self.recharge = 0
        self.difficulty = 1
        self.sleeptalk = False

        self.type = None
        self.emoji = None
        self.gif = None

        self.critRate = 0
        self.xCrit = 1

    def set_stats_by_lv(self, hpLv, atkLv, defLv, dexEntry):
        self.hp = self.hpMax = scale_hp(hpLv, dexEntry['hp'], 0, 0)
        self.attack = scale_stat(atkLv, dexEntry['atk'], 0, 0, 1)
        self.defense = scale_stat(defLv, dexEntry['def'], 0, 0, 1)

    def use_move(self, trainer):
        result = {
            'move': self.move,
        }

        moveAccuracy = 1
        if not self.attack_lands(moveAccuracy, trainer):
            result['action'] = 'used'
            result['failed'] = MISSED
            return result

        power = random.uniform(65, 100)
        xType = trainer.typeResists[self.type]
        dmg = get_damage(self, trainer, power, xType)

        if self.critRate and random.random() < self.critRate:
            dmg = int(dmg * self.xCrit)
            result['note'] = ' ⚠_Critical hit!_'

        result['action'] = random.choice(actions)
        result['dmg'] = dmg
        result['x_type'] = xType

        '''
        {
            'move':
            'action': random.choice(['attacks with', 'strikes back using', 'counters with'])
            'attack_text'
            'dmg': dmg
            'x_type': xType
            'failed': MISSED
            'failed_msg': ''
            'note': (text about plusle)
        }
        '''

        return result

    def attack_lands(self, moveAccuracy, trainer):
        return random.random() < moveAccuracy * accuracy(self.accuracyStage, trainer.evasionStage)

    def apply_damage(self, dmg, trainer):
        dmg = int(dmg)
        startHp = self.hp
        self.hp = max(0, self.hp - dmg)
        hpTaken = startHp - self.hp
        return dmg, hpTaken, None

    def restore_hp(self, hp):
        if self.hp <= 0:
            return 0
        startHp = self.hp
        self.hp = min(self.hpMax, self.hp + hp)
        return self.hp - startHp

    def on_start(self, trainer):
        pass

    def on_turn_start(self):
        pass

    def on_unit_turn(self, unit):
        pass

    def on_unit_dies(self, unit):
        pass

    def on_death(self):
        self.buffs = []
        self.statuses = {}

    def clone(self):
        clone = copy.copy(self)
        clone.buffs = []
        return clone

class MeowthFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(MeowthFamily, self).__init__(no, lv, name)
        self.moves = ['Fury Swipes', 'Bandit']

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Fury Swipes':
            power = 18
            moveAccuracy = 0.9
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            roll = random.randint(1, 6)
            if roll <= 2: hits = 2
            elif roll <= 4: hits = 3
            elif roll == 5: hits = 4
            else: hits = 5

            dmg = 0
            for i in range(hits):
                dmg += get_damage(self, trainer, power, xType)

            return {
                'move': move,
                'attack_text': f'used _Fury Swipes_! Hit **{hits}** times for **{dmg}** dmg!',
                'dmg': dmg,
                'x_type': xType
            }

        if move == 'Bandit':

            power = 40
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            dmg = get_damage(self, trainer, power, xType)
            jacobs = random.randint(2, 25)
            # todo remove jacobs

            return {
                'move': move,
                'attack_text': f'{random.choice(actions)} _Pay Day_ for **{dmg}** dmg! **{jacobs}** of your jacobs were swiped!!',
                'dmg': dmg,
                'x_type': xType
            }

for name in ['Meowth', 'Alolan Meowth', 'Persian', 'Alolan Persian']:
    classMap[name] = MeowthFamily


class MimeFamily(Enemy):
    debuff = Buff()
    debuff.defDebuffs = [0] + [1] * 10

    def __init__(self, no=None, lv=0, name=''):
        super(MimeFamily, self).__init__(no, lv, name)

    def use_move(self, trainer):

        if self.type == PSYCHIC:
            moves = ['Barrier', 'Psychic']
        else:
            moves = ['Barrier']

        # todo barrier
        moves = ['Psychic']

        moveAccuracy = 1
        xType = trainer.typeResists[self.type]
        move = random.choice(moves)

        if not self.attack_lands(moveAccuracy, trainer):
            return miss_result(move)

        if move == 'Psychic':
            power = 90
            result = {
                'move': move,
                'x_type': xType
            }

            if random.random() < 0.2:
                trainer.buffs.append(self.debuff.as_target_buff(6))
                trainer.refresh_flat_buff()
                result['note'] = ' Lowered your type defense!' #self.debuff.as_inline_text()[1]

            dmg = get_damage(self, trainer, power, xType)

            result['dmg'] = dmg
            result['attack_text'] = f'{random.choice(actions)} _{move}_ for **{dmg}** dmg!'

            return result

        if move == 'Barrier':
            pass

for name in ['Mime Jr. (Psychic)', 'Mime Jr. (Fairy)', 'Mr. Mime (Psychic)', 'Mr. Mime (Fairy)']:
    classMap[name] = MimeFamily


class RattataFamily(Enemy):
    debuff = Buff()
    debuff.defDebuffs[0] = 1

    def __init__(self, no=None, lv=0, name=''):
        super(RattataFamily, self).__init__(no, lv, name)
        self.moves = ['Tackle', 'Tail Whip']

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Tackle':
            power = 40
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            return {
                'move': move,
                'x_type': xType,
                'action': random.choice(actions),
                'dmg': get_damage(self, trainer, power, xType)
            }

        if move == 'Tail Whip':
            power = 20
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            result = {
                'move': move,
                'x_type': xType
            }

            trainer.buffs.append(self.debuff.as_target_buff(6))
            trainer.refresh_flat_buff()
            dmg = get_damage(self, trainer, power, xType)

            result['dmg'] = dmg
            result['attack_text'] =  f'{random.choice(actions)} _{move}_ for **{dmg}** dmg! Lowered your defense!'

            return result

for name in ['Rattata', 'Raticate', 'Alolan Rattata', 'Alolan Raticate']:
    classMap[name] = RattataFamily


class GyaradosFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(GyaradosFamily, self).__init__(no, lv, name)
        self.moves = ['Dragon Rage']

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Dragon Rage':
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            dmg = int(trainer.hp / 2)
            return {
                'move': move,
                'x_type': 1,
                'dmg': dmg,
                'attack_text': f'{random.choice(actions)} _{move}_ for **{dmg}** dmg! Your party\'s HP was cut in **half**!'
            }

for name in ['Gyarados (Water)', 'Gyarados (Dragon)']:
    classMap[name] = GyaradosFamily


class MagikarpFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(MagikarpFamily, self).__init__(no, lv, name)
        self.moves = ['Tackle', 'Splash']

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Tackle':
            power = 40
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            return {
                'move': move,
                'x_type': xType,
                'action': random.choice(actions),
                'dmg': get_damage(self, trainer, power, xType)
            }

        if move == 'Splash':
            return {
                'move': move,
                'x_type': 1,
                'attack_text': f'used _{move}_, but nothing happened!'
            }

for name in ['Magikarp']:
    classMap[name] = MagikarpFamily


class KomalaFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(KomalaFamily, self).__init__(no, lv, name)
        self.statuses[SLEEPING] = 10000
        self.moves = ['Sleep Talk', 'Yawn']

    def use_move(self, trainer):

        self.restore_hp(int(self.hpMax * (1/8)))
        note = ' It restored a little bit of HP from its nap.'

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Sleep Talk':
            power = 80
            moveAccuracy = 0.75
            if not self.attack_lands(moveAccuracy, trainer):
                return {
                    'move': move,
                    'action': 'used',
                    'failed': MISSED,
                    'note': note
                }

            return {
                'move': move,
                'x_type': xType,
                'action': 'used',
                'dmg': get_damage(self, trainer, power, xType),
                'note': note
            }

        elif move == 'Yawn':
            moveAccuracy = 0.75
            if SLEEPING in trainer.statuses or not self.attack_lands(moveAccuracy, trainer):
                return {
                    'move': move,
                    'action': 'used',
                    'failed': 'but it failed!' if SLEEPING in trainer.statuses else MISSED,
                    'note': note
                }

            trainer.statuses[SLEEPING] = random.randint(1, 4)

            return {
                'move': move,
                'attack_text': f'used _{move}_! Your party became drowzy and **fell asleep**!',
                'note': note
            }

for name in ['Komala']:
    classMap[name] = KomalaFamily


class SandshrewFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(SandshrewFamily, self).__init__(no, lv, name)

    def use_move(self, trainer):

        if self.type == EARTH:
            moves = ['Sand Attack']
        else:
            moves = ['Snow Attack']

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Sand Attack' or move == 'Snow Attack':
            power = 40
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            trainer.accuracyStage = clamp(trainer.accuracyStage - 1, -6, 6)
            return {
                'move': move,
                'x_type': xType,
                'attack_text': f'{random.choice(actions)} _{move}_! Your party\'s accuracy fell!',
                'dmg': get_damage(self, trainer, power, xType)
            }


for name in ['Sandshrew', 'Sandslash', 'Alolan Sandshrew', 'Alolan Sandslash']:
    classMap[name] = SandshrewFamily

class ChanseyFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(ChanseyFamily, self).__init__(no, lv, name)
        self.moves = ['Egg Bomb', 'Half-Boiled']

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Egg Bomb':
            power = 100
            moveAccuracy = 0.75
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            return {
                'move': move,
                'x_type': xType,
                'action': random.choice(actions),
                'dmg': get_damage(self, trainer, power, xType)
            }

        if move == 'Soft-Boiled':
            success = False
            for p in self.party:
                if p is not self and p.hp > 0:
                    p.restore_hp(int(p.hpMax * 0.5))
                    p.statuses = []
                    success = True

            return {
                'move': move,
                'action': random.choice(actions),
                'attack_text': 'healed its party using _{move}_!' if success else f'used _{move}_, but it failed!',
            }


for name in ['Happiny', 'Chansey', 'Blissey']:
    classMap[name] = ChanseyFamily


class VoltorbFamily(Enemy):
    def __init__(self, no=None, lv=0, name='', timer=2):
        super(VoltorbFamily, self).__init__(no, lv, name)
        self.timer = None
        if self.name == 'Electrode':
            buff = Buff()
            buff.defBuffs = [3] * 11
            self.buffs.append(buff)
            self.timer = timer

    def on_start(self, trainer):
        if self.timer is not None:
            return f'{self.emoji}{self.name}\'s timer menacingly displays the number **{self.timer}**.'

    def on_turn_start(self):
        pass

    def use_move(self, trainer):
        if self.timer is not None:
            self.timer -= 1
            if self.timer == 0:
                self.hp = 0
                dmg = get_damage(self, trainer, 200, 1)
                return {
                    'move': 'Self-Destruct',
                    'x_type': 1,
                    'attack_text': f'\'s timer decreases to **0**. It used **Self-Destruct** for **{dmg}** dmg and fainted!',
                    'dmg': dmg,
                }
            else:
                return {
                    'move': None,
                    'attack_text': f'\'s timer decreases to **{self.timer}**.',
                }
        else:
            move = random.choice(['Self-Destruct', 'Volt Tackle'])
            if move == 'Self-Destruct':
                self.hp = 0
                dmg = get_damage(self, trainer, 200, 1)
                return {
                    'move': 'Self-Destruct',
                    'x_type': 1,
                    'attack_text': f'used **Self-Destruct** for **{dmg}** dmg and fainted!',
                    'dmg': dmg
                }

            xType = trainer.typeResists[self.type]
            power = 65
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            return {
                'move': move,
                'x_type': xType,
                'action': random.choice(actions),
                'dmg': get_damage(self, trainer, power, xType)
            }

for name in ['Voltorb', 'Electrode']:
    classMap[name] = VoltorbFamily


class GastlyFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(GastlyFamily, self).__init__(no, lv, name)

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]

        if SLEEPING in trainer.statuses:
            moveAccuracy = 1
            move = 'Dream Eater'
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            power = 100
            dmg = get_damage(self, trainer, power, xType)
            recover = self.restore_hp(max(1, int(dmg / 2)))
            if recover > 0:
                recoverText = f'It restored **{recover}** HP from your sleeping party\'s dream.'
            else:
                recoverText = f'Its already at full health!'

            return {
                'move': move,
                'x_type': xType,
                'attack_text': f'used _{move}_ for **{dmg}** dmg! {recoverText}',
                'dmg': dmg,
            }

        move = random.choice(['Poison Gas', 'Hypnosis'])
        if self.difficulty > 0:
            if move == 'Poison Gas' and POISONED in trainer.statuses and not SLEEPING in trainer.statuses:
                move = 'Hypnosis'
            elif move == 'Hypnosis' and SLEEPING in trainer.statuses and not POISONED in trainer.statuses:
                move = 'Poison Gas'

        if move == 'Poison Gas':
            moveAccuracy = 0.9
            if POISONED in trainer.statuses or not self.attack_lands(moveAccuracy, trainer):
                return {
                    'move': move,
                    'action': 'used',
                    'failed': 'but it failed!' if POISONED in trainer.statuses else MISSED,
                }

            trainer.statuses[POISONED] = True
            return {
                'move': move,
                'attack_text': f'{random.choice(actions)} _{move}_! Your party was **poisoned**!',
            }

        if move == 'Hypnosis':
            moveAccuracy = 0.6
            if SLEEPING in trainer.statuses or not self.attack_lands(moveAccuracy, trainer):
                return {
                    'move': move,
                    'action': 'used',
                    'failed': 'but it failed!' if SLEEPING in trainer.statuses else MISSED,
                }

            trainer.statuses[SLEEPING] = random.randint(2, trainer.attacksPerTurn)
            return {
                'move': move,
                'attack_text': f'used _{move}_! Your party fell into a **deep sleep**!',
            }

for name in ['Gastly', 'Haunter', 'Gengar']:
    classMap[name] = GastlyFamily



class BulbasaurFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(BulbasaurFamily, self).__init__(no, lv, name)
        if self.name in ['Bulbasaur']:
            self.moves = ['Vine Whip', 'Leech Seed']

        elif self.name in ['Ivysaur']:
            self.moves = ['Razor Leaf', 'Leech Seed', 'Mega Drain']

        elif self.name in ['Venusaur', 'Bellossom']:
            self.moves = ['Solar Beam', 'Giga Drain']

        elif self.name in ['Oddish']:
            self.moves = ['Absorb']
            self.difficulty = 0

        elif self.name in ['Gloom', 'Vileplume']:
            self.moves = ['Poison Powder', 'Sleep Powder', 'Stun Spore', 'Giga Drain']

    def use_move(self, trainer):

        if self.recharge > 0:
            self.recharge -= 1
            return { 'attack_text': 'is recharging!' }

        xType = trainer.typeResists[self.type]

        if self.charge == 1:
            move = 'Solar Beam'
        else:
            if self.difficulty == 0:
                move = random.choice(self.moves)
            else:
                skip = []
                for m in self.moves:
                    if m in ['Absorb', 'Mega Drain', 'Giga Drain'] and self.hp == self.hpMax:
                        skip.append(m)

                    if m == 'Leech Seed' and SEEDED in trainer.statuses:
                        skip.append(m)

                    if m == 'Sleep Powder' and SLEEPING in trainer.statuses:
                        skip.append(m)

                    if m == 'Poison Powder' and POISONED in trainer.statuses:
                        skip.append(m)

                    if m == 'Stun Spore' and PARALYZED in trainer.statuses:
                        skip.append(m)



                move = random.choice([m for m in self.moves if m not in skip])

        if move == 'Leech Seed':
            moveAccuracy = 0.9
            if SEEDED in trainer.statuses or not self.attack_lands(moveAccuracy, trainer):
                return {
                    'move': move,
                    'action': 'used',
                    'failed': 'but it failed!' if SEEDED in trainer.statuses else MISSED,
                }

            trainer.statuses[SEEDED] = self
            return {
                'move': move,
                'attack_text': f'{random.choice(actions)} _{move}_! Your party was **seeded**!',
            }

        if move in ['Absorb', 'Mega Drain', 'Giga Drain']:
            moveAccuracy = 1
            power = [20, 40, 75][['Absorb', 'Mega Drain', 'Giga Drain'].index(move)]
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            dmg = get_damage(self, trainer, power, xType)
            recover = self.restore_hp(max(1, int(dmg / 2)))
            if recover > 0:
                recoverText = f'It restored **{recover}** HP!'
            else:
                recoverText = f'Its already at full health!'

            return {
                'move': move,
                'x_type': xType,
                'attack_text': f'used _{move}_ for **{dmg}** dmg! {recoverText}',
                'dmg': dmg,
            }

        if move == 'Solar Beam':
            b = get_flat_buff(self.buffs)
            if not b.atkBuffs[FIRE] and not self.charge:
                self.charge += 1
                return { 'attack_text': 'took in sunlight.' }

            self.charge = 0
            power = 120
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            dmg = get_damage(self, trainer, power, xType)
            if b.atkBuffs[FIRE]:
                text = f'unleashes a firey _{move}_ for **{dmg}** dmg!'
            else:
                text = f'unleashes _{move}_ for **{dmg}** dmg!'

            return {
                'move': move,
                'x_type': xType,
                'attack_text': text,
                'dmg': dmg
            }

        if move in ['Poison Powder', 'Sleep Powder', 'Stun Spore']:
            n = ['Poison Powder', 'Sleep Powder', 'Stun Spore'].index(move)
            status = [POISONED, SLEEPING, PARALYZED][n]
            moveAccuracy = 0.75
            if status in trainer.statuses or not self.attack_lands(moveAccuracy, trainer):
                return {
                    'move': move,
                    'action': 'used',
                    'failed': 'but it failed!' if status in trainer.statuses else MISSED,
                }
            if status == POISONED:
                trainer.statuses[status] = True
            else:
                trainer.statuses[status] = random.randint(2, trainer.attacksPerTurn)
            return {
                'move': move,
                'attack_text': f'''{random.choice(actions)} _{move}_! Your party {['was **poisoned**', '**fell asleep**', 'was **paralyzed**'][n]}!''',
            }


        n = ['Vine Whip', 'Razor Leaf'].index(move)
        power = [45, 55][n]
        moveAccuracy = [1, 0.5][n]
        if not self.attack_lands(moveAccuracy, trainer):
            return miss_result(move)

        return {
            'move': move,
            'x_type': xType,
            'action': random.choice(actions),
            'dmg': get_damage(self, trainer, power, xType)
        }

for name in ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Oddish', 'Gloom', 'Vileplume', 'Bellossom']:
    classMap[name] = BulbasaurFamily


class CastformFamily(Enemy):
    def __init__(self, no=None, lv=0, name='', timer=2):
        super(CastformFamily, self).__init__(no, lv, name)

    def on_start(self, trainer):
        weatherBuff = Buff()

        if self.type == FIRE:
            weatherBuff.atkBuffs[FIRE] = 2
            text = f'{dex.emoji(88)}**Castform** used _Sunny Day_ and transformed! The sunlight is strong.'
        elif self.type == WATER:
            weatherBuff.atkBuffs[WATER] = 2
            text = f'{dex.emoji(88)}**Castform** used _Rain Dance_ and transformed! It started to rain!'
        elif self.type == ICE:
            weatherBuff.atkBuffs[ICE] = 2
            text = f'{dex.emoji(88)}**Castform** used _Snowy Day_ and transformed! The snow falls lightly.'

        for p in self.party:
            p.buffs.append(weatherBuff.as_self_buff())

        return text

    def use_move(self, trainer):
        xType = trainer.typeResists[self.type]
        move = 'Weather Ball'
        power = 50
        moveAccuracy = 1
        if not self.attack_lands(moveAccuracy, trainer):
            return miss_result(move)

        return {
            'move': move,
            'x_type': xType,
            'action': random.choice(actions),
            'dmg': get_damage(self, trainer, power, xType)
        }

for name in ['Castform (Sunny)', 'Castform (Rainy)', 'Castform (Snowy)']:
    classMap[name] = CastformFamily



class AbsolFamily(Enemy):

    debuff = Buff()
    debuff.defDebuffs[NORMAL] = 1
    debuff.defDebuffs[DARK] = 1

    def __init__(self, no=None, lv=0, name=''):
        super(AbsolFamily, self).__init__(no, lv, name)
        self.moves = ['Pursuit', 'Destiny Bond']
        self.destinyBond = False

    def apply_damage(self, dmg, trainer):
        dmg = int(dmg)
        startHp = self.hp
        self.hp = max(0, self.hp - dmg)
        hpTaken = startHp - self.hp

        text = None

        if self.destinyBond:
            self.destinyBond = False
            if self.hp == 0 and trainer.hp > 0:
                trainer.hp = 0
                text = '_It took you down with it!_'

        return dmg, hpTaken, text

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Pursuit':
            power = 70
            moveAccuracy = 0.9
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            trainer.buffs.append(self.debuff.as_target_buff(6))
            trainer.refresh_flat_buff()
            note = ' Lowered your type defense!' #self.debuff.as_inline_text()[1]

            dmg = get_damage(self, trainer, power, xType)
            return {
                'move': move,
                'dmg': dmg,
                'action': random.choice(actions),
                'x_type': xType,
                'note': self.debuff.as_inline_text()[1]
            }

        if move == 'Destiny Bond':

            self.destinyBond = True
            return {
                'move': move,
                'attack_text': f'readies its _{move}_.',
            }

for name in ['Absol']:
    classMap[name] = AbsolFamily


class PhantumpFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(PhantumpFamily, self).__init__(no, lv, name)
        self.moves = ['Hide', 'Leech Seed']

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]
        if self.difficulty == 0:
            move = random.choice(self.moves)
        else:
            skip = []
            for m in self.moves:
                if m == 'Leech Seed' and SEEDED in trainer.statuses:
                    skip.append(m)

            move = random.choice([m for m in self.moves if m not in skip])

        if move == 'Hide':
            self.evasionStage = clamp(self.evasionStage + 2, -6, 6)
            return {
                'move': move,
                'attack_text': f'used _{move}_! [**+**Evasion]',
            }

        if move == 'Leech Seed':
            moveAccuracy = 0.9
            if SEEDED in trainer.statuses or not self.attack_lands(moveAccuracy, trainer):
                return {
                    'move': move,
                    'action': 'used',
                    'failed': 'but it failed!' if SEEDED in trainer.statuses else MISSED,
                }

            trainer.statuses[SEEDED] = self
            return {
                'move': move,
                'attack_text': f'{random.choice(actions)} _{move}_! Your party was **seeded**!',
            }

for name in ['Phantump (Psychic)', 'Phantump (Nature)', 'Trevenant (Psychic)', 'Trevenant (Nature)']:
    classMap[name] = PhantumpFamily

class ChatotFamily(Enemy):

    def __init__(self, no=None, lv=0, name=''):
        super(ChatotFamily, self).__init__(no, lv, name)
        self.moves = ['Peck', 'Chatter']

    def use_move(self, trainer):

        move = random.choice(self.moves)
        if self.difficulty > 0:
            if CONFUSED in trainer.statuses:
                move = 'Peck'

        if move == 'Chatter':
            if CONFUSED in trainer.statuses:
                return {
                    'move': move,
                    'action': 'used',
                    'failed': 'but it failed!',
                }

            trainer.statuses[CONFUSED] = random.randint(1, 4)
            return {
                'move': move,
                'attack_text': f'{random.choice(actions)} _{move}_! Your party became **confused**!',
            }

        if move == 'Peck':
            power = 40
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            return {
                'move': move,
                'x_type': 1,
                'action': random.choice(actions),
                'dmg': get_damage(self, trainer, power, 1)
            }

for name in ['Chatot']:
    classMap[name] = ChatotFamily


class ScytherFamily(Enemy):
    def __init__(self, no=None, lv=0, name=''):
        super(ScytherFamily, self).__init__(no, lv, name)
        self.critRate = 0.5
        self.xCrit = 1.5

for name in ['Scyther', 'Scizor', 'Elekid', 'Electabuzz', 'Smoochum', 'Jynx', 'Magby', 'Magmar']:
    classMap[name] = ScytherFamily


class SalanditFamily(Enemy):
    def __init__(self, no=None, lv=0, name=''):
        super(SalanditFamily, self).__init__(no, lv, name)

    def apply_damage(self, dmg, trainer):
        dmg = int(dmg)
        startHp = self.hp
        self.hp = max(0, self.hp - dmg)
        hpTaken = startHp - self.hp

        text = None
        if POISONED not in trainer.statuses:
            trainer.statuses[POISONED] = True
            text = '_Your party was **poisoned** on contact!_'

        return dmg, hpTaken, text

for name in ['Salandit (Nature)', 'Salandit (Fire)', 'Salazzle (Nature)', 'Salazzle (Fire)']:
    classMap[name] = SalanditFamily


class NidoranFamily(Enemy):
    def __init__(self, no=None, lv=0, name=''):
        super(NidoranFamily, self).__init__(no, lv, name)
        self.moves = ['Earthquake']

    def use_move(self, trainer):

        xType = trainer.typeResists[self.type]
        move = random.choice(self.moves)

        if move == 'Earthquake':
            power = 100
            moveAccuracy = 1
            if not self.attack_lands(moveAccuracy, trainer):
                return miss_result(move)

            dmg = get_damage(self, trainer, power, xType, pierceFactor=0.5)
            return {
                'move': move,
                'dmg': dmg,
                'action': random.choice(actions),
                'x_type': xType,
                'note': ' It pierced your defense!'
            }


for name in ['Nidoking', 'Nidoqueen']:
    classMap[name] = NidoranFamily
from discord.ext import commands
from common import *

import random
import sqlite3
import difflib

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fractions import Fraction

from pprint import pprint, pformat

class Pokedex:
    def __init__(self, bot):
        self.bot = bot
        self.pkmn = {}
        self.nos = {}
        self.load_dex()

    def load_dex(self):
        pokedb = sqlite3.connect('data/pokedex.db')
        c = pokedb.cursor()
        rows = c.execute('select * from pkmn').fetchall()
        fields = list(map(lambda d: d[0], c.description))
        pokedb.close()

        self.pkmn = {}
        for row in rows:
            data = {}
            no, name = row[0], row[3]
            for i, value in enumerate(row):
                if i == 0: continue
                # if isinstance(value, str):
                #     value = value.strip()
                data[fields[i]] = value

            data['key'] = name.lower().replace('.', '')
            data['type'] = ('Normal', 'Fire', 'Water', 'Nature', 'Earth', 'Electric', 'Ice', 'Psychic', 'Fairy', 'Dark', 'Dragon').index(data['type'])
            self.pkmn[no] = data
            self.nos[name] = no

            data['emoji'] = data['emoji'].strip()
            data['gif'] = 'https://play.pokemonshowdown.com/sprites/xyani/{}.gif' \
                .format(data['gif'] if data['gif'] else base_name(data['name'], remove='().').replace(' ', '-').lower())

            data['sprite'] = 'https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/{}.png' \
                .format(data['sprite'] if data['sprite'] else base_name(data['name'], remove='().').replace(' ', '-').lower())

            # Actives (Range Conditions, Burn Rate % etc)

            statuses = ['psn', 'seed', 'burn', 'para', 'flinch', 'slp', 'confuse', 'charm']
            data['status_inflict'] = [0] * len(statuses)
            if data['type'] == FIRE:
                data['status_inflict'][BURN] = 0.05
            elif data['type'] == PSYCHIC:
                data['status_inflict'][CONFUSE] = 0.03
            elif data['type'] == ELECTRIC:
                data['status_inflict'][PARA] = 0.05
            elif data['type'] == ICE:
                data['storm'] = 0.05
            elif data['type'] == EARTH:
                data['storm'] = 0.05
            elif data['type'] == FAIRY:
                data['status_inflict'][CHARM] = 0.03

            if data['mass_kg'] <= 5:
                data['wt_class'] = FEATHER
            elif data['mass_kg'] <= 100:
                data['wt_class'] = LIGHT
            elif data['mass_kg'] <= 200:
                data['wt_class'] = MID
            elif data['mass_kg'] <= 300:
                data['wt_class'] = HEAVY
            else:
                data['wt_class'] = TITAN

            data['acc_buff'] = 0
            data['evade_buff'] = 0
            data['acc_debuff'] = 0
            data['evade_debuff'] = 0

            flags = data['ability_flag'].split(' ') if data['ability_flag'] else []

            for f in flags:
                tag = None
                try:
                    tag, value = f.split(':', 1)
                except ValueError:
                    tag = f

                if tag == 'fixed':
                    if value == 'half':
                        data['fixed_dmg'] = -50
                    elif value.endswith('%'):
                        data['fixed_dmg'] = -int(value[:-1])
                    else:
                        data['fixed_dmg'] = int(value)

                if tag == 'accuracy':
                    data['acc_buff'] = int(value)

                elif tag == 'evade':
                    data['evade_buff'] = int(value)

                elif tag == 'accuracydebuff':
                    data['acc_debuff'] = int(value)

                elif tag == 'evadedebuff':
                    data['evade_debuff'] = int(value)

                elif tag == 'crit+':
                    data['crit+'] = int(value)

                elif tag in ['kills', 'pp', 'slot', 'turns', 'hp', 'moves', 'enemies', 'party', 'weight']:
                    try: value = int(value)
                    except ValueError: pass
                    data['condition'] = (tag, value)

                elif tag == 'recoil':
                    data['recoil'] = int(value)

                elif tag == 'recharge':
                    data['recharge'] = int(value)

                elif tag == 'selfdestruct':
                    data['selfdestruct'] = True

                elif tag == 'copy':
                    if value == 'before':
                        data['copy'] = -1
                    elif value == 'after':
                        data['copy'] = 1
                    else:
                        data['copy'] = int(value)

                elif tag in statuses:
                    data['status_inflict'][statuses.index(tag)] += int(value) / 100

                elif tag == 'self':
                    if not 'status_self' in data:
                        data['status_self'] = [0] * len(statuses)
                    data['status_self'][statuses.index(value)] = True

                elif tag == 'pp+':
                    if not 'pp+' in data:
                        data['pp+'] = {
                            'type': [0] * 11,
                            'slot': [0] * 6,
                            'all': 0,
                            'self': 0
                        }

                    if value == 'notself':
                        data['pp+']['notself'] = True
                    else:
                        target, pp = value.split(',')
                        pp = int(pp)
                        if target in typeKeys:
                            data['pp+']['type'][typeKeys.index(target)] += pp
                        elif target == 'all':
                            data['pp+']['all'] += pp
                        else:
                            try:
                                target = int(target)
                                if 1 <= target <= 6:
                                    data['pp+']['slot'][target - 1] += pp
                                elif target == 0:
                                    data['pp+']['self'] += pp
                            except ValueError:
                                pass

                elif tag.startswith('x2'):
                    for status, name in enumerate(statuses):
                        if name in tag:
                            if not 'x2_status' in data:
                                data['x2_status'] = [0] * len(statuses)
                            data['x2_status'][status] = float(value)

                elif tag == 'cure':
                    data['hp+'] = 0.3
                elif tag == 'cura':
                    data['hp+'] = 0.4
                elif tag == 'curaga':
                    data['hp+'] = 2/3
                elif tag == 'hp+':
                    if value == 'all':
                        data['hp+'] = 1
                    else:
                        data['hp+'] = int(value) if int(value) > 1 else float(value)

                elif tag == 'esuna':
                    data['esuna'] = True

                elif tag == 'dispel':
                    data['dispel'] = True

                elif tag == 'storm':
                    if not 'storm' in data:
                        data['storm'] = int(value) / 100
                    data['storm'] += int(value) / 100

            # Buffs

            if data['buff_duration']:
                b = Buff()
                b.duration = data['buff_duration']

                # Buffs
                if data['buff_atk']:
                    b.atkBuffs[0] = data['buff_atk']
                if data['buff_def']:
                    b.defBuffs[0] = data['buff_def']

                if data['buff_type_atk']:
                    b.atkBuffs[data['type']] = data['buff_type_atk']
                if data['buff_type_def']:
                    b.defBuffs[data['type']] = data['buff_type_def']

                # Debuffs
                if data['debuff_atk']:
                    b.atkDebuffs[0] = data['debuff_atk']
                if data['debuff_def']:
                    b.defDebuffs[0] = data['debuff_def']

                if data['debuff_type_atk']:
                    b.atkDebuffs[data['type']] = data['debuff_type_atk']
                if data['debuff_type_def']:
                    b.defDebuffs[data['type']] = data['debuff_type_def']

                if data['buff_re']:
                    b.reflect = data['buff_re']

                extras = data['extra_buff'].split(' ') if data['extra_buff'] else []
                for extra in extras:
                    tag, value = extra.split(':', 1)
                    value = int(value)
                    t = None
                    if tag.startswith('all'):
                        t = -1
                    else:
                        for i, key in enumerate(typeKeys):
                            if tag.startswith(key):
                                t = i

                    if t is None:
                        raise ValueError(f'Invalid extra_buff type for {name} using {extra}')

                    if '+d' in tag:
                        buffSet = b.defBuffs
                    elif '-d' in tag:
                        buffSet = b.defDebuffs
                    elif '-a' in tag:
                        buffSet = b.atkDebuffs
                    else:
                        buffSet = b.atkBuffs

                    if t == -1:
                        for i in range(1, 11):
                            buffSet[i] = value
                    else:
                        buffSet[t] = value

                data['buff'] = b


            # Passives (Z Bonus)

            passives = data['passive'].split(' ') if data['passive'] else []
            passiveBuff = Buff()
            for passive in passives:
                tag, value = passive.split(':', 1)

                if tag == 'sleeptalk':
                    data['sleeptalk'] = int(value)

                elif tag == 'block':
                    n, text = value.split(',')
                    data['block'] = [int(n), text.replace('_', ' ')]

                elif tag == 'hits':
                    data['hits'] = int(value)

                elif tag == 'alpha':
                    data['alpha'] = int(value)

                elif tag == 'has':
                    data['passive_has_pkmn'] = int(value)

                else:
                    t = None
                    if tag.startswith('all'):
                        t = -1
                    else:
                        for i, key in enumerate(typeKeys):
                            if tag.startswith(key):
                                t = i
                    if t is not None:

                        # Z-Bonus
                        if '+z' in tag:
                            if 'z_bonus' not in data:
                                data['z_bonus'] = [0] * 11
                            if t == -1:
                                for i in range(1, 11):
                                    data['z_bonus'][i] += int(value)
                            else:
                                data['z_bonus'][t] += int(value)

                        # Innate Buff
                        else:
                            tiers, duration = value.split(',')
                            passiveBuff.duration = int(duration)

                            if '+d' in tag:
                                buffSet = passiveBuff.defBuffs
                            elif '-d' in tag:
                                buffSet = passiveBuff.defDebuffs
                            elif '-a' in tag:
                                buffSet = passiveBuff.atkDebuffs
                            else:
                                buffSet = passiveBuff.atkBuffs

                            if t == -1:
                                for i in range(1, 11):
                                    buffSet[i] = int(tiers)
                            else:
                                buffSet[t] = int(tiers)

            if not passiveBuff.is_zero():
                data['passive_buff'] = passiveBuff


    def emoji(self, no):
        return self.pkmn[no]['emoji']

    def sample_from_set(self, n, setNo=1, evo=False):
        nos = []
        pool = list(self.pkmn.keys())
        while len(nos) < n:
            no = random.choice(pool)
            if evo and self.pkmn[no]['stage'] == 1:
                continue
            if self.pkmn[no]['set_no'] == setNo:
                nos.append(no)
        return nos

    @commands.command(name='type', aliases=['chart', 'types', 'typechart'])
    async def type_chart(self, ctx, *, arg=''):

        allTypes = ''.join(typeEmoji[1:-1])

        text = f'''{typeEmoji[0]} represents **neutral**, which is typeless. Neutral buffs ({typeEmoji[0]}+Atk) and debuffs ({typeEmoji[0]}-Def) modify the **general** attack/defense of **all** Pokémon. Neutral slots in your `.party` apply bonuses to **all** Pokémon. It's like a wildcard!

{typeEmoji[-1]} is just a short way of indicating all non-neutral types ({allTypes}) to save space. It's not the same as {typeEmoji[0]}!'''

        e = discord.Embed(description=text).set_image(url='https://i.imgur.com/c4EWkq7.png')
        await ctx.send('', embed=e)



        # lines = ['___' + ''.join(typeEmoji[t] for t in range(11))]
        # for atkType, row in enumerate(typeChart):
        #     line = typeEmoji[atkType] + '`'
        #     marks = []
        #     for value in row:
        #         if value == X:
        #             marks.append('**2**')
        #         elif value == O:
        #             marks.append('½')
        #         else:
        #             marks.append('--')

        #     line += ' '.join(marks) + '`'
        #     lines.append(line)

        # await send_message(ctx, '\n'.join(lines))

    @commands.command(name='dex', aliases=['p', 'pokedex'])
    async def lookup(self, ctx, *, arg=''):
        if not arg:
            no, = self.sample_from_set(1)
        else:
            matches = process.extractBests(re.sub(r'[\(\)\.\- ]', '', arg.replace('é', 'e')), self.nos.keys(), limit=15, score_cutoff=50, processor=lambda x: re.sub(r'[\(\)\.\- ]', '', x.replace('é', 'e')))
            topMatches = [match for match in matches if match[1] > 85]# and self.pkmn[self.nos[match[0]]]['set_no'] is not None]
            if topMatches and (len(topMatches) == 1 or topMatches[0][1] > 98):
                no = self.nos[topMatches[0][0]]
            else:
                matches = '\n'.join([f'_{match[0]}_' for match in matches])
                await send_message(ctx, f'No results! Did you mean:{DBL_BREAK}{matches}', error=True, expires=15)
                return

        await self.view_entry(ctx, no)

    async def view_entry(self, ctx, no, caught=False, returnEmbed=False):

        d = self.pkmn[no]

        title = d['name'] if not caught else f'''New Pokédex Data for {d['name']}!'''

        missing = d['set_no'] is None

        efx = typeChart[d['type']]
        strongVs = ''.join([typeEmoji[t] for t, x in enumerate(efx) if x == X])
        weakVs = ''.join([typeEmoji[t] for t, x in enumerate(efx) if x == O])

        if 'x2_status' in d:
            x2s = []
            for status, multi in enumerate(d['x2_status']):
                if multi:
                    x2s.append(f'''**{['Poisoned', 'Seeded', 'Burned', 'Paralyzed', 'Flinched', 'Sleeping', 'Confused'][status]}** Pokémon''')
            strongVs += ' ' + ', '.join(x2s)

        description = f'''{typeEmoji[d['type']]}{typeNames[d['type']]} Type'''
        if strongVs:
            description += f'\n_Strong Against:_ {strongVs}'
        if weakVs:
            description += f'\n_Weak Against:_ {weakVs}'
        description += f'''{DBL_BREAK}{d['pokedex_entry']}'''
        if d['notes']:
            description += f''' {d['notes']}'''


        wt = ('Feather', 'Light', 'Mid', 'Heavy', 'Titan')[d['wt_class']]

        if missing:
            statText = f'''**HP**:  ?   **PP**:  ?   **Wt**: {wt}
**Atk**:  ?   **Def**:  ?'''

            e = discord.Embed(title=title, description=description, color=TYPE_COLORS[d['type']]) \
            .set_image(url=d['image']).set_thumbnail(url=d['gif']) \
            .add_field(name='⚔ Stats', value=statText, inline=True) \
            .add_field(name='🗺 Habitats', value='???', inline=True) \
            .add_field(name=f'''💥 ???''', value='???', inline=True) \

        else:
            statText = f'''**HP**:  {d['hp']}   **PP**:  {d['pp']}   **Wt**: {wt}
**Atk**:  {d['atk']}   **Def**:  {d['def']}'''

            if d['target'] is None:
                target = ''
            elif d['target'] == 2:
                #target = ' • **{} Random** Target{}'.format(d['hits'], 's' if d['hits'] > 1 else '')
                target = ' 「{} Random Target{}」'.format(d['hits'], 's' if d['hits'] > 1 else '')

            else:
                #target = f''' • **{('Single', 'AoE', 'Random', 'Dual')[d['target']]}** Target''' if d['target'] is not None else ''

                #target = f''' 「{('Single', 'AoE', 'Random', 'Dual')[d['target']]} Target」''' if d['target'] is not None else ''

                target = f''' 「{('Single Target', '**AoE**', 'Random', 'Dual Target')[d['target']]}」''' if d['target'] is not None else ''


            zRange = zRanges[d['tier'] - 1]
            moveText = f'''**{d['pp_cost']}** PP{target}'''

            if d['target'] is not None:

                if 'fixed_dmg' in d:
                    if d['fixed_dmg'] < 0:
                        moveText += f'''\nFixed Damage: **{-d['fixed_dmg']}**% of Remaining HP'''
                    else:
                        moveText += f'''**{d['fixed_dmg']}** Fixed Damage'''

                x = [1.4, 1.0, 1.0][d['target']]

                if 'condition' in d:
#                     moveText += f'''\nMultiplier: x**{round(d['x_min'] * x, 2)}** ~ **{round(d['x_max'] * x, 2)}**
# _{range_text(d['condition'])}_'''
                    moveText += f'''\nMulti:  x**{round(d['x_min'] * x, 2)}** ~ **{round(d['x_max'] * x, 2)}**'''
                    moveText += f'''\nZ-Move:  x**{1 + zRange[1]/100}**  [+{zRange[1]}%]'''
                    moveText += f'''\n_{range_text(d['condition'])}_'''

                else:
                    moveText += f'''\nMulti:  x**{x}**'''
                    moveText += f'''\nZ-Move:  x**{1 + zRange[1]/100}**  [+{zRange[1]}%]'''


            if 'copy' in d:
                if d['copy'] == 1:
                    moveText += f'''\nCopies the Pokémon after this one.'''
                elif d['copy'] == -1:
                    moveText += f'''\nCopies the Pokémon before this one.'''

            if 'status_self' in d:
                for status, value in enumerate(d['status_self']):
                    if value:
                        if status == SLP:
                            moveText += f'\nPuts your party to sleep {statusEmoji[SLP]}'
                        elif status == CONFUSE:
                            moveText += f'\nConfuses your party {statusEmoji[CONFUSE]}'

            if 'recoil' in d:
                if d['recoil'] == 100:
                    moveText += f'\n**Recoil!** Lose all but **1** HP'
                else:
                    moveText += f'''\n**Recoil!** Lose **{d['recoil']}**% of max HP'''

            if 'recharge' in d:
                moveText += f'''\n⏱ Recharge: **{d['recharge']}** Turn'''

            if 'selfdestruct' in d:
                moveText += f'''\n💣 Faint after damage'''

            extras = []
            if d['target'] is not None:
                for status, chance in enumerate(d['status_inflict']):
                    if chance:
                        extras.append(f'**{int(chance*100)}**% {statusEmoji[status]} {statusNames[status]} Infliction')

            if 'storm' in d:
                if d['type'] == EARTH:
                    extras.append(f'''**{int(d['storm']*100)}**% {pokemoji['sand']} Sandstorm''')
                else:
                    extras.append(f'''**{int(d['storm']*100)}**% {pokemoji['hail']} Hail''')

            if d['acc_buff']:
                extras.append(f'''🎯 +**{d['acc_buff']}** Accuracy''')
            if d['evade_buff']:
                extras.append(f'''👥 +**{d['evade_buff']}** Evasion''')
            if d['acc_debuff']:
                extras.append(f'''🎯 -**{d['acc_debuff']}** Enemy Accuracy''')
            if d['evade_debuff']:
                extras.append(f'''👥 -**{d['evade_debuff']}** Enemy Evasion''')

            if 'crit+' in d:
                extras.append(f'''⚠ +**{d['crit+']}**% Critical Hit Rate''')

            if 'dispel' in d:
                extras.append(f'''💬 Dispel Enemy Buffs''')

            if extras:
                moveText += '\n' + '\n'.join(extras)

            setName = 'Unreleased'
            if d['set_no'] and d['set_no'] > 0:
                setName = f'''Base Set {d['set_no']}'''
            footer = f'''Tier {d['tier']} • [{zRange[0]}-{zRange[1]}%] • No. {d['pokedex_no']} / {setName}'''


            habitatsText = '''Pallet Town'''# if no in [1, 4, 7] else '???'

            e = discord.Embed(title=title, description=description, color=TYPE_COLORS[d['type']]) \
                .set_image(url=d['image']).set_thumbnail(url=d['gif']).set_footer(text=footer, icon_url=d['sprite']) \
                .add_field(name='⚔ Stats', value=statText, inline=True) \
                .add_field(name='🗺 Habitats', value=habitatsText, inline=True) \
                .add_field(name=f'''💥 {d['move']}''', value=moveText, inline=True) \

            if 'buff' in d:
                b = d['buff']
                if b.duration >= 6:
                    title = f'{noEmoji[int(b.duration / 6)]} Turn Buff'
                else:
                    title = f'{noEmoji[b.duration]} Attack Buff'

                e.add_field(name=title, value=buff_text(b), inline=True)


            if any(key in d for key in ['z_bonus', 'alpha', 'passive_buff', 'sleeptalk', 'block']):
                passives = []
                if 'passive_has_pkmn' in d:
                    has = self.pkmn[d['passive_has_pkmn']]
                    passives.append(f'''With{has['emoji']}**{has['name']}** in Party:''')

                if 'passive_buff' in d:
                    b = d['passive_buff']
                    if b.duration > 50:
                        title = 'Permanent'
                    elif b.duration >= 6:
                        title = f'{int(b.duration / 6)} Turn'
                    else:
                        title = f'{b.duration} Attack'
                    passives.append(f'{title}: {buff_text(b)}')
                if 'z_bonus' in d:
                    for t in range(11):
                        if d['z_bonus'][t]:
                            passives.append( f'''+**{d['z_bonus'][t]}**% Z-Move for all{typeEmoji[t]}''')
                if 'alpha' in d:
                    passives.append( f'''+**{d['alpha']}**% Z-Move for all Pokémon starting with its letter''')

                    #for letter, bonus in d['alpha']:
                    #    passives.append( f'''+**{bonus}**% Z-Move for Pokémon starting with **'{letter}'**''')

                if 'sleeptalk' in d:
                    passives.append(f'{statusEmoji[SLP]} Sleep Talk\n_Can attack while sleeping._')
                if 'block' in d:
                    passives.append('_Blocks **{}** move{} damage entirely._'.format(d['block'][0], "'s" if d['block'][0] == 1 else "s'"))
                e.add_field(name='✨ Passive', value='\n'.join(passives), inline=True)

            if 'pp+' in d:
                e.add_field(name='💛 PP Restore', value=pp_restore_text(d), inline=True)

            if 'hp+' in d or 'esuna' in d:
                heals = []
                if 'hp+' in d:
                    if d['hp+'] == 1:
                        heals.append(f'''Restores **all** Party HP''')
                    elif d['hp+'] > 1:
                        heals.append(f'''Restores **{d['hp+']}** Party HP''')
                    else:
                        fraction = Fraction(d['hp+']).limit_denominator()
                        if fraction.denominator < 6:
                            heals.append(f'''Restores **{str(fraction)}** of Party HP''')
                        else:
                            heals.append(f'''Restores **{int(d['hp+'] * 100)}**% of Party HP''')
                if 'esuna' in d:
                    heals.append(f'_Cures all status ailments_')

                e.add_field(name='❤ Heal', value='\n'.join(heals), inline=True)

        if returnEmbed:
            return e

        try:
            await ctx.send(f'<@{ctx.author.id}>', embed=e)
        except discord.errors.HTTPException as err:
            details = f'''{d['name']}

{err}
Body: {e.description}

Fields: {pprint(e.fields)}

Gif: {d['gif']}

Sprite: {d['sprite']}

Image: {d['image']}'''
            print(details)
            await send_message(ctx, f'''Error: Pokédex data missing for {d['name']}!\n_This is expected for most entries at the moment._''', error=True)


def range_text(condition):
    tag, value = condition

    if tag == 'kills':
        if value == 'more':
            return 'Increases Per Knockout'
        else:
            return 'Decreases Per Knockout'

    if tag == 'pp':
        if value == 'more':
            return 'Increases with Higher PP'
        else:
            return 'Increases with Lower PP'

    if tag == 'turns':
        if value == 'more':
            return 'Increases Each Turn'
        else:
            return 'Decreases Each Turn'

    if tag == 'moves':
        if value == 'more':
            return 'Increases w/ More Moves\nUsed This Turn'
        else:
            return 'Decreases w/ More Moves\nUsed This Turn'

    if tag == 'hp':
        if value == 'more':
            return 'Increases with Higher HP'
        else:
            return 'Increases with Lower HP'

    if tag == 'slot':
        if value == 'high':
            return 'Increases with Later Slot'
        elif value == 'low':
            return 'Increases with Earlier Slot'
        else:
            return f'Strongest in Slot **{value}**'

    if tag == 'enemies':
        if value == 'more':
            return 'Increases with More Enemies'
        elif value == 'less':
            return 'Increases with Fewer Enemies'

    if tag == 'party':
        if value.startswith('more_') or value.startswith('less_'):
            adj = 'More' if value.startswith('more_') else 'Fewer'
            try:
                t = typeKeys.index(value[-2:])
                return f'Increases with {adj}\n{typeEmoji[t]}{typeNames[t]} Types in Party'
            except IndexError:
                pass

    if tag == 'weight':
        if value == 'heavy':
            return 'Stronger against heavy foes'
        elif value == 'light':
            return 'Stronger against lighter foes'

def pp_restore_text(dexEntry):
    lines = []
    a = dexEntry['pp+']['all']

    if dexEntry['pp+']['self']:
        lines.append(f'''_Self:_ +**{a + dexEntry['pp+']['self']}** PP''')

    if a:
        lines.append(f'{typeEmoji[-1]}+**{a}** PP')

    for t, pp in enumerate(dexEntry['pp+']['type']):
        if pp:
            lines.append(f'{typeEmoji[t]}+**{a + pp}** PP')

    for slot, pp in enumerate(dexEntry['pp+']['slot']):
        if pp:
            lines.append(f'_Slot {slot+1}:_ +**{a + pp}** PP')

    if 'notself' in dexEntry['pp+']:
        lines.append('_Does Not Target Self_')

    return '\n'.join(lines)

def buff_text(b):
    lines = []
    for i, buffSet in enumerate([b.atkBuffs, b.defBuffs, b.atkDebuffs, b.defDebuffs]):
        groups = {}
        for t in range(0, 11):
            if buffSet[t] != 0:
                if buffSet[t] in groups:
                    groups[buffSet[t]].append(t)
                else:
                    groups[buffSet[t]] = [t]

        for tiers in groups:
            if sum(groups[tiers]) == 55:
                groups[tiers] = [0, -1] if 0 in groups[tiers] else [-1]

        buffList = sorted(groups.items(), key=lambda g: 100 if 0 in g[1] else g[0], reverse=True)
        label = ['Atk', 'Def', 'Enemy Atk', 'Enemy Def'][i]
        for g in buffList:
            if i > 1:
                sign = '-'
            else:
                sign = '+' if g[0] > 0 else ''

            lines.append('{} {} {}**{}**'.format(''.join(typeEmoji[t] for t in g[1]), label, sign, g[0]))

    if b.reflect:
        lines.append(f'Reflect +**{b.reflect}**')

    return '\n'.join(lines)


def setup(bot):
    dex = Pokedex(bot)
    bot.add_cog(dex)
    bot.dex = dex
import discord
import random
import math

import sys
import pc
import difflib

from fuzzywuzzy import process
from common import *

class Party:
    def __init__(self, bot):
        # self.db = db
        self.bot = bot
        self.userdb = bot.userdb
        self.cache = {}

        self.debugUsers = {}
        self.debugDecks = {}
        # in real cache, store equipped deck only, no ids?
        # update d

    def make_test_party(self, lo=5, hi=5, count=6):
        pkmn = []
        nos = self.bot.dex.sample_from_set(count, 1)
        nos[0] = 49
        for no in nos:
            p = self.bot.pc.make_pkmn(no=no, lv=random.randint(lo, hi))
            if random.random() <= 0.2:
                p.orbs = random.randint(1, 3)
            elif random.random() <= 0.2:
                p.z = random.randint(10, 150)
            pkmn.append(p)

        return pkmn

    @commands.command(aliases=['deck'])
    async def party(self, ctx, *, args=None):
        if not args:
            await self.view_party(ctx)
            return

        helpMsg = '''TODO help menu'''
        uid = ctx.author.id

        # todo nickname

        if 'help' in args:
            await send_message(ctx, helpMsg, expires=10, color=INFO_BLUE)
            return

        if 'auto' in args:
            self.auto_equip(uid, args)
            await self.view_party(ctx)
            return

        lo = 0
        if ' proud' in args:
            name = args.rsplit(' ', 1)[0]
            lo = 3
        else:
            m = re.match(r'([A-Za-z\'\s]+?)([1-9])', args)
            if m:
                name = m.group(1)
                lo = int(m.group(2)) - 1
                if lo > 3:
                    await send_message(ctx, 'There are currently **4** loadouts per deck! Try a lower number.', error=True)
                    return
            else:
                name = args

        showTip = False
        name = name.lower().strip()
        try:
            deckNo = deckShorts.index(name)
        except ValueError:
            deckNo = resolve_deck(name)
            showTip = True

        if deckNo != -1:
            self.save_active_deck_no(uid, deckNo, lo)
            await self.view_party(ctx)
            if showTip:
                await send_message(ctx, f'Tip: You can also type `{ctx.prefix}{ctx.command} {deckShorts[deckNo]}` as a shortcut. For a full list, see `.decks`', ping=False, color=INFO_BLUE)
            return

        mention = self.bot.resolve_tag(ctx.message.guild, args)
        if mention:
            #todo
            await send_message(ctx, f'TODO: show {mention.name}\'s deck.')
            return

        await send_message(ctx, f'''Couldn\'t find that user or that deck name!{DBL_BREAK}{helpMsg}''', error=True)
        return


    async def view_party(self, ctx, uid=None):
        uid = uid or ctx.author.id

        await ctx.trigger_typing()

        if not uid in self.bot.pc.cache:
            self.bot.pc.load_db_into_cache(uid)
        userPc = self.bot.pc.cache[uid]
        deckType, lo = self.load_active_deck_no(uid)
        deck = self.load_deck(uid, deckType, lo)

        party = [None] * 5
        for p in userPc['badges']:
            try:
                party[deck['ids'].index(p.id)] = p
            except ValueError:
                pass

        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)

        boosts = deckBoosts[deckKeys[deck['deck']]]

        #pool = [p for p in userPc['badges'] if p.id in deck['ids']]
        #party = [pool[pool.index(p)] if p else None for p in deck['ids']]
        #for i, pid in enumerate(deck['ids']):

        # nos = self.bot.dex.sample_from_set(6, 1)
        # for no in nos:
        #     p = self.bot.pc.make_pkmn(no=no, lv=random.randint(5, 100))
        #     if random.random() <= 0.2:
        #         p.orbs = random.randint(1, 5)
        #     elif random.random() <= 0.2:
        #         p.z = random.randint(10, 150)
        #         p.orbs = 5
        #     party.append(p)

        # load all the shit

        # pkmn = blah
        # shared pkmn too if loadout != PROUD


        # end load

        allBoosts = list(set(boost for slotBoosts in boosts for boost in slotBoosts))
        if deck['nick']:
            pass
            #title = '{} {} +{} [ #{} ]'.format(kbTitles[kbid][0],nickname, level, loadoutIndex + 1)
            #title = '{} {} +{} [ #{} ]'.format(kbTitles[kbid][0],nickname, level, loadoutIndex + 1)
        else:
            #name = '{}{} • Lo. {}'.format(deckNames[deckType], ' +{}'.format(deckLv) if deckLv else '', partyNo + 1)

            types = ''.join(typeEmoji[t] for t in allBoosts if t is not NORMAL)
            name = '{}{} • Party {}{}'.format(deckNames[deck['deck']], ' +{}'.format(deck['lv']) if deck['lv'] else '', deck['party_no'] + 1, types)

            #name = f'{deckNames[deckType]}{{' +{deckLv}' if deckLv else ''}} • Party {partyNo + 1} {types}'

        lines = []
        for slot, p in enumerate(party):
            multiLabel = ''
            multi = xSlots[slot]
            if p:
                '''Equipped Slot'''
                d = self.bot.dex.pkmn[p.no]
                boosted = slot == 5 or boosts[slot][0] == NORMAL or d['type'] in boosts[slot]

                if boosted:
                    multiLabel = f''' {typeEmoji[d['type']]}x **{multi:.2f}**'''

                if p.z:
                    stat1 = f'{p.z}%'
                elif p.orbs > 0:
                    stat1 = '•' * p.orbs
                else:
                    stat1 = 'L.'+'{: >3}'.format(p.lv)

                stat2 = '-' if p.tm is None else tmKeys[p.tm]
                #name = badge.get_name(d, key='short')
                lines.append(f'''`{slot+1}` {d['emoji']} `{stat1: <5} {stat2}` {p.hms_as_text()}{multiLabel}''')

            else:
                '''Blank Slot'''
                lines.append(f'''`{slot+1}` {''.join(typeEmoji[t] for t in boosts[slot])}x **{multi:.2f}**''')

        typeResists = get_type_resistances([p.type() for p in party if p])
        resistText = type_resistances_as_text(typeResists)
        if resistText:
            lines.append(resistText)

        description = '\n'.join(lines)
        if deck['cached_img']:
            e = discord.Embed(title=name, description=description).set_image(url=deck['cached_img'])
            await ctx.send(f'<@{uid}>', embed=e)
            return

        ns = [p.no if p else None for p in party]
        png = self.bot.render.render_deck(deck['deck'], ns)
        e = discord.Embed(title=name, description=description).set_image(url='attachment://party.png')
        sent = await ctx.send(f'<@{uid}>', embed=e, file=discord.File(png.getvalue(), 'party.png'))
        deck['cached_img'] = sent.embeds[0].image.url
        self.save_deck(uid, deck)


    def set_deck_nickname(self):
        pass

    def load_active_deck(self, uid):
        deckType, lo = self.load_active_deck_no(uid)
        return self.load_deck(uid, deckType, lo)

    def load_active_deck_no(self, uid):
        if not uid in self.debugUsers:
            self.save_active_deck_no(uid, random.randint(0, 9), 0)
        return (self.debugUsers[uid]['deck'], self.debugUsers[uid]['lo'])

    def save_active_deck_no(self, uid, deckType, lo):
        if not uid in self.debugUsers:
            self.debugUsers[uid] = {
                'deck': deckType,
                'lo': lo
            }
        else:
            self.debugUsers[uid]['deck'] = deckType
            self.debugUsers[uid]['lo'] = lo

    def load_deck(self, uid, deck, lo):
        try:
            return copy.copy(self.debugDecks[uid][deck][lo])
        except KeyError:
            return {
                'deck': deck,
                'lv': 0,
                'ids': [None] * 5,
                'party_no': lo,
                'nick': '',
                'cached_img': None,
            }

    def save_deck(self, uid, data):
        deckType, lo = data['deck'], data['party_no']
        if not uid in self.debugDecks:
            self.debugDecks[uid] = {
                deckType: {
                    lo: data
                }
            }
        else:
            if not deckType in self.debugDecks[uid]:
                self.debugDecks[uid][deckType] = {lo: data}
            else:
                self.debugDecks[uid][deckType][lo] = data

    def load_active_party(self, uid, debug=False):
        # todo remove
        if debug:
            party = []
            nos = self.bot.dex.sample_from_set(6, 1)
            for no in nos:
                p = self.bot.pc.make_pkmn(no=no, lv=50)
                party.append(p)
            deck = self.bot.party.load_active_deck(uid)
            return deck, party

        if not uid in self.bot.pc.cache:
            self.bot.pc.load_db_into_cache(uid)
        userPc = self.bot.pc.cache[uid]
        deck = self.bot.party.load_active_deck(uid)

        party = [None] * 5
        for p in userPc['badges']:
            try:
                party[deck['ids'].index(p.id)] = p
            except ValueError:
                pass

        return deck, party

    @commands.command(aliases=['eq'])
    async def equip(self, ctx, *, args):
        # if arg is None or arg == '' or arg == 'help':
        #     print('Equip specific medal slots by using `.equip <slot> <medal> <slot> <medal>` like `.equip 1=55 3=23` or `.equip 1 55`. The `=` is optional!\nThe numbers refer to the order you see in your `.inventory`\n \nEquip a shared medal by using `.equip @user` from `.share list`\n \nTip: You can also automatically fill out a keyblade using `.equip auto`!\nRe-arrange equipped medals by using `.equip swap`')
        #     return True

        uid = ctx.author.id
        if 'auto' in args:
            self.auto_equip(uid, args)
            await self.view_party(ctx)
            return



        if not uid in self.bot.pc.cache:
            self.bot.pc.load_db_into_cache(uid)
        userPc = self.bot.pc.cache[uid]


        # if not all(arg.isdigit() or '=' in arg for arg in args):
        #     # tag user
        #     pass

        left = []
        right = []
        errors = []
        slotThenPkmn = False
        updates = 0
        for m in re.finditer('([0-9]+)[:= ]([0-9]+)', args):
            left.append(int(m.group(1)) - 1)
            right.append(int(m.group(2)) - 1)

        if not left:
            # tag user
            pass
            return

        # if left and max(left) > 4:
        #     slotThenPkmn = False

        if max(right) > 4:
            slotThenPkmn = True

        deckType, lo = self.load_active_deck_no(uid)
        deck = self.load_deck(uid, deckType, lo)
        # deck['ids'][0] = userPc['badges'][0].id
        # self.save_deck(uid, deck)

        # todo copy.copy old ids and compare

        before = copy.copy(deck['ids'])
        for i, _ in enumerate(left):
            try:
                if slotThenPkmn:
                    slot, index = left[i], right[i]
                else:
                    slot, index = right[i], left[i]

                p = userPc['badges'][index]
                if isinstance(p, pc.PcEvolution):
                    await send_message(ctx, f'You cannot equip an evolution badge directly! These are meant to be fused into real Pokémon.', error=True)
                    return

                if p.id in deck['ids']:
                    deck['ids'][deck['ids'].index(p.id)] = deck['ids'][slot]
                deck['ids'][slot] = p.id
                updates += 1
            except IndexError:
                errors.append(f'{left[i]+1}={right[i]+1}')

        if errors:
            await send_message(ctx, 'Unknown Slot/Pokémon pair(s): `{}`, try `.party help`'.format('` `'.join(errors)), error=True)
            return

        if not updates:
            await send_message(ctx, 'No changes were made! Try `.party help`', error=True)
            return

        if deck['ids'] != before:
            deck['cached_img'] = None
        self.save_deck(uid, deck)
        await send_message(ctx, f'Updated **Party {lo+1}** of your **{deckNames[deckType]}**! Type `.party` to see it.', color=INFO_BLUE)

        #await self.view_party(ctx)


    def auto_equip(self, uid, args):
        if not uid in self.bot.pc.cache:
            self.bot.pc.load_db_into_cache(uid)
        userPc = self.bot.pc.cache[uid]
        deckType, lo = self.load_active_deck_no(uid)
        deck = self.load_deck(uid, deckType, lo)

        replace = not 'empty' in args
        onlyAoe = 'aoe' in args
        onlySt = 'st' in args
        useTotems = 'totem' in args
        addPp = not 'no pp' in args
        addDispel = 'dispel' in args

        # todo filter

        pkmn = [p for p in userPc['badges'] if isinstance(p, pc.PcPokemon)]

        # sp = max(inventory, key=lambda m: m.restore_rank(data[m.n]))
        # dispel = max(inventory, key=lambda m: m.dispel_rank(data[m.n]))
        # if not dispel.dispel_rank(data[dispel.n]):
        #     dispel = None

        before = copy.copy(deck['ids'])
        if replace:
            deck['ids'] = [None] * 5

        xSlots = (1.3, 1.4, 1.5, 1.6, 1.7)
        boosts = deckBoosts[deckKeys[deck['deck']]]
        allBoosts = list(set(boost for slotBoosts in boosts for boost in slotBoosts))

        gauSlot = 0
        ppSlot = min(range(1, 5), key=lambda i: xSlots[i]) if addPp else None
        party = [None] * 6 #todo shared

        for slot, _ in enumerate(deck['ids']):
            if slot in (gauSlot, ppSlot) or (deck['ids'][slot] and not replace):
                continue

            # if gau and gau.id not in deck['ids']:
            #     deck['ids'][slot] = gau.id
            #     gau = None
            #     continue

            # elif dispel and addDispel and (not deck['ids'][slot] or replace) and not dispel.id in loadoutIds:
            #     deck['ids'][slot] = dispel.id
            #     dispel = None

            offRanks = {}
            offRankMin = sys.maxsize
            for p in pkmn:
                rank = p.offensive_rank(slot, boosts[slot], allBoosts, xSlots[slot], useTotems)
                offRanks[p.id] = rank
                if rank < offRankMin: offRankMin = rank

            # todo sort according to average of offrank/defrank
            print(slot, f'\n\n----- SLOT {slot} -----')
            print('\n\n')

            list.sort(pkmn, key=lambda p: offRanks[p.id], reverse=True)

            # print(f'**************** Min: {offRankMin}  /  Max: {pkmn[0].offensive_rank(slot, boosts[slot], xSlots[slot], useTotems)}')

            for p in pkmn:
                 print(p, '\n ', int(p.offensive_rank(slot, boosts[slot], allBoosts, xSlots[slot], useTotems)), '\n')

            for p in pkmn:
                if (onlyAoe and p.target() != AOE) or (onlySt and p.target() != ST):
                    continue
                if not p.id in deck['ids']:
                    deck['ids'][slot] = p.id
                    party[slot] = p
                    break


        # GAU Pokemon

        list.sort(pkmn, key=lambda p: p.gau_rank(), reverse=True)
        for p in pkmn:
            if not p.id in deck['ids']:
                if p.gau_rank() > -1:
                    deck['ids'][gauSlot] = p.id
                    party[gauSlot] = p
                break


        # ppPkmn = max(pkmn, key=lambda p:)
        # deck['ids'][ppSlot] = ppPkmn.id

        if ppSlot is not None:
            list.sort(pkmn, key=lambda p: p.pp_rank(party, ppSlot), reverse=True)
            for p in pkmn:
                if not p.id in deck['ids']:
                    deck['ids'][ppSlot] = p.id
                    party[ppSlot] = p
                    break

                # todo fill in empty spot again if necessary

        if deck['ids'] != before:
            deck['cached_img'] = None
        self.save_deck(uid, deck)

    @commands.command()
    async def decks(self, ctx, *, arg=''):

        decks = {}
        for deck, name in enumerate(deckNames):
            xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
            #xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)

            boosts = deckBoosts[deckKeys[deck]]
            #allBoosts = list(set(boost for slotBoosts in boosts for boost in slotBoosts))

            #slots = []
            slotText = ''
            for slot in range(5):
                if slot < 5:
                    types = ''.join(typeEmoji[t] for t in boosts[slot])
                else:
                    types = typeEmoji[NORMAL]

                #slots.append(('\n' if slot == 3 else '') + f'[ `{slot+1}` {types}]')

                slotText += f'[ `{slot+1}` {types}]'
                if slot == 2:
                    slotText += '\n'
                elif slot < 4:
                    slotText += '  '
                #slots.append(f'`{slot+1}` {types}')


           # decks[deck] = '_{}_   {}'.format(name.replace(' Deck', ''), '  '.join(slots))
            #decks[deck] = '_{}_\n{}'.format(name.replace(' Deck', ''), '  '.join(slots))

            #decks[deck] = '{}  _{}_'.format('  '.join(slots), name.replace(' Deck', ''))
            decks[deck] = '{}  _{}_'.format(slotText, name.replace(' Deck', ''))


            #decks.append('_{}:_   {}'.format(name.replace(' Deck', ''), ' /  '.join(slots)))
            #decks.append('_{}_   {}'.format(name, ' /  '.join(slots)))

        # e = discord.Embed(title='') \
        #     .add_field(name=f'Starter Decks', value='\n'.join(text for text in [decks[0], decks[1], decks[2]]), inline=False) \
        #     .add_field(name=f'Bonus Decks', value='\n'.join(text for text in [decks[4], decks[5], decks[8], decks[9]]), inline=False) \
        #     .add_field(name=f'Specialty Decks', value='\n'.join(text for text in [decks[3], decks[6], decks[7]]), inline=False)

        e = discord.Embed(title='') \
            .add_field(name=f'Starter Decks', value=DBL_BREAK.join(text for text in [decks[0], decks[1], decks[2]]), inline=False) \
            .add_field(name=f'Bonus Decks', value=DBL_BREAK.join(text for text in [decks[4], decks[5], decks[8], decks[9]]), inline=False) \
            .add_field(name=f'Specialty Decks', value=DBL_BREAK.join(text for text in [decks[3], decks[6], decks[7]]), inline=False)



        #e = discord.Embed(title='', description='\n'.join(decks)[:2048])
        await ctx.send(f'<@{ctx.author.id}>', embed=e)




        #await ctx.send(f'You tagged <@{self.bot.resolve_tag(ctx.message.guild, arg).id}>')

    @commands.command()
    async def tagtest(self, ctx, *, arg=''):
        await ctx.send(f'You tagged <@{self.bot.resolve_tag(ctx.message.guild, arg).id}>')


def resolve_deck(name):
    # matches = process.extractBests(re.sub(r'[\.\- ]', '', arg), self.nos.keys(), limit=15, score_cutoff=50, processor=lambda x: re.sub(r'[\.\- ]', '', x))

    matches = process.extractBests(name, deckNames, limit=1)
    #matches = difflib.get_close_matches(name, deckNames, n=1)
    if not matches:
        return -1
    return deckNames.index(matches[0][0])

def setup(bot):
    party = Party(bot)
    bot.add_cog(party)
    bot.party = party
import time

from battle import *
from common import *

P1, P2 = 0, 1

class PvpManager(object):
    def __init__(self, bot, ctx, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.players = [p1, p2]
        self.parties = [None, None]
        self.quests  = [None, None]
        self.points  = [0, 0]

        self.round  = 0
        self.rounds = 1
        self.turns  = 3

        self.accepted = False
        self.ready = [False, False]

        bot.pvp.openbattles[p1.id] = self
        bot.pvp.openbattles[p2.id] = self

        self.bot = bot
        self.ctx = ctx
        self.expires = time.time() + 30 * 60

    async def handle_message(self, message):
        if len(message.content) > 20:
            return

        n = P1 if message.author == self.p1 else P2
        cmd = message.content.lower().strip()
        if not self.accepted:# and n == P2
            if cmd == 'a':
                self.accepted = True
                await self.show_vs(init=True)
                return

            if cmd == 'no':
                await self.bot.pvp.declined(self)
                return
        else:
            if cmd == 'ready':
                self.refresh_parties()
                for n, data in enumerate(self.parties):
                    if not any(data[1]):
                        await send_message(self.ctx, f'{self.players[n].name} has no active Pokémon in their `.party`! Try using `.equip` or `.equip auto`.', error=True)
                        return False

                self.parties[P1]
                self.ready[n] = not self.ready[n]
                if True:#all(self.ready):
                    #await self.ctx.send('Starting...')
                    self.quests = [self.make_quest(self.p1), self.make_quest(self.p2)]
                    self.quests[P1].attach(self.quests[P2].trainer)
                    self.quests[P2].attach(self.quests[P1].trainer)

                    await self.quests[P1].start_turn(self.ctx, first=True)
                    return

                await self.show_vs()

    def make_quest(self, user):
        n = P1 if user == self.p1 else P2
        deck, party = self.parties[n]
        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        boosts = deckBoosts[deckKeys[deck['deck']]]
        #party.append(self.bot.pc.make_pkmn(no=self.bot.dex.sample_from_set(1, 1)[0], lv=50))
        party = to_battle_pkmn(party, boosts, xSlots)
        trainer = TrainerState(party, pvp=True)
        return PvpQuest(self.bot, user.id, self, trainer, n, P2 if n == P1 else P1)

    def refresh_parties(self):
        self.parties[P1] = self.bot.party.load_active_party(self.p1.id, debug=self.p1.id == self.bot.user.id)
        self.parties[P2] = self.bot.party.load_active_party(self.p2.id, debug=self.p2.id == self.bot.user.id)

    async def show_vs(self, init=False):
        description = '''Switch to the party you'd like to fight with using `.party` and type `ready`. Type `ready` a second time to undo marking yourself as ready.'''

        if init:
            description =  f'_**{self.p1.name}** has won the coin toss and will go first_' + DBL_BREAK + description
            self.refresh_parties()

        e = discord.Embed(description=description) \
            .add_field(name='{}{}'.format(self.p1.name, ' [Ready]' if self.ready[P1] else ''),
                value=self.party_preview_as_text(*self.parties[P1]), inline=True) \
            .add_field(name='{}{}'.format(self.p2.name, ' [Ready]' if self.ready[P2] else ''),
                value=self.party_preview_as_text(*self.parties[P2]), inline=True) \
            .set_author(name=f'A battle is starting!', icon_url=pokeballUrl) \

        await self.ctx.send('', embed=e)

    async def turn_end(self, n):
        self.quests[n].trainer.activePkmn = None
        self.bot.wfm.pop(self.players[n].id, None)
        # todo something about turn tracker / who went first also end
        diff = self.points[P1] - self.points[P2]

        if n == P2 and self.quests[n].trainer.turnsElapsed > self.turns:
            if diff > 0:
                text = f'{self.p1.name} has **won** by **{diff:,}** damage points! Rankings will go here soon.'
            elif diff < 0:
                text = f'{self.p2.name} has **won** by **{-diff:,}** damage points! Rankings will go here soon.'
            else:
                text = f'The score is exactly tied with **{self.points[P1]:,}** damage points! Your ranks remain **unchanged**.'

            e = discord.Embed(description=text, color=0xFCCD00) \
                .set_author(name=f'Battle Finished!', icon_url=pokeballUrl)
            await self.ctx.send('', embed=e)
            return



        if diff > 0:
            text = f'{self.p1.name} is winning by **{diff:,}** damage points!'
        elif diff < 0:
            text = f'{self.p2.name} is winning by **{-diff:,}** damage points!'
        else:
            text = f'The score is exactly tied with **{self.points[P1]:,}** damage points!'

        e = discord.Embed(description=text, color=INFO_BLUE) \
            .set_author(name=f'Turn Finished!', icon_url=pokeballUrl)
        await self.ctx.send('', embed=e)
        nextPlayer = P2 if n == P1 else P1
        await self.quests[nextPlayer].start_turn(self.ctx, delay=2)


    def party_preview_as_text(self, deck, party):

        # boosts = deckBoosts[deckKeys[deck['deck']]]
        # allBoosts = list(set(boost for slotBoosts in boosts for boost in slotBoosts))
        # types = ''.join(typeEmoji[t] for t in allBoosts if t is not NORMAL)

        text = '_{}{}_\n'.format(deckNames[deck['deck']], ' +{}'.format(deck['lv']) if deck['lv'] else '')
        for i, p in enumerate(party):
            text += self.bot.dex.emoji(p.no) if p else ''
            if i == 2: text += '\n'

        texts = [text]
        typeResists = get_type_resistances([p.type() for p in party if p])
        resistText = type_resistances_as_text(typeResists)
        if resistText:
            texts.append(resistText)

        return '\n'.join(texts)



    '''

    .pvp 1 @user
    type y to accept



    Both trainers: switch to the party you'd like to fight with using `.party` and type `ready` when ready. Type `ready` a second time to mark yourself as unready.


    if round == 1

        Both trainers: select your party of choice using `.party`, then type `ready` when ready. If your opponent changes their party _after_ you've said `ready`, you'll have a chance to change yours as well and type `ready` again.

    Switch to the party you'd like to fight with using `.party` and type `ready` when ready.



    .pvp 1

    type the name (and optionally number) of a 2nd keyblade
    then type ready when ready

    left / right
    jacob / komala
    Ready  Not Ready
    `1` cinnabar
    `2`


    be sure to show title or whatever

    show
    Round 1
    blah

    vs

    blah

    .switch

    '''

class PvpQuest(Quest):
    def __init__(self, bot, uid, battle, trainer, nPlayer, nOpponent):
        super(PvpQuest, self).__init__(bot, uid, E_TRAINER_BATTLE, trainer)
        self.battle = battle
        self.nPlayer = nPlayer
        self.nOpponent = nOpponent
        self.opponent = None
        self.showHelp = True
        self.ctx = None
        self.img = None

    def attach(self, opponent):
        self.opponent = opponent
        self.engagedParty = [opponent]

    def points_as_text(self, playerPov):
        if playerPov:
            diff = self.battle.points[self.nPlayer] - self.battle.points[self.nOpponent]
            text = f'''{pokemoji['pb_small']} Damage:   **{self.battle.points[self.nPlayer]:,}**'''
        else:
            diff = self.battle.points[self.nOpponent] - self.battle.points[self.nPlayer]
            text = f'''{pokemoji['pb_small']} Damage:   **{self.battle.points[self.nOpponent]:,}**'''

        if diff == 0:
            text += '  _Tied_'
        else:
            if diff > 0:
                text += f'  [ **+**{abs(diff)} ] _Winning!_'
            else:
                text += f'  [ **-**{abs(diff)} ] _Losing!_'
        return text



    async def handle_message(self, message):
        if len(message.content) > 20:
            return
        inputs = message.content.lower().strip()
        if inputs in ['x', 'auto']:
            await self.do_actions([(ATTACK, 1, True)] * 6)
            return

        if inputs == 'sx':
            await self.do_actions([SKIP] * 6)
            return

        chain = []
        for cmd in inputs.split():
            if cmd == 'a' or 'cmd' == '1':
                chain.append((ATTACK, 1, True))
            elif cmd == 's':
                chain.append(SKIP)
            elif cmd == 'r':
                # immediately run todo
                break
            else:
                return

        if chain:
            await self.do_actions(chain)

        #await message.delete()

    async def do_actions(self, actions):

        results, error = self.process_actions(actions)
        if results:
            e = self.make_updated_embed(results)
            await self.ctx.send(f'<@{self.uid}>', embed=e)
        if error:
            await send_message(self.ctx, error, error=True)
        else:
            status = results[-1]['status']
            if status == PLAYER_TURN_END:
                await self.battle.turn_end(self.nPlayer)

    async def start_turn(self, ctx, first=False, delay=0):

        self.ctx = ctx
        description = f'{self.battle.players[self.nPlayer].name}\'s Turn **{self.trainer.turnsElapsed + 1}**  /  {self.battle.turns}  •  Round {self.battle.round + 1}{DBL_BREAK}'

        if self.showHelp:
            commands = f'''- Type `a` to use your Pokémon's ability
- Type `s` to skip a Pokémon and restore 1 PP
- Type `r` to run
- Type `x` or `auto` to automate fighting{DBL_BREAK}Or quickly chain multiple commands such as: `1 s 1 2`'''
            description += commands
            self.showHelp = False

        deck, party = self.battle.parties[self.nPlayer]
        if deck['cached_img']:
            self.img = deck['cached_img']
            e = discord.Embed(description=description).set_image(url=self.img)
        else:
            ns = [p.no if p else None for p in party]
            png = self.bot.render.render_deck(deck['deck'], ns)
            e = discord.Embed(description=description).set_image(url='attachment://party.png')

        e.add_field(name=f'{self.battle.players[self.nPlayer].name}\'s Party',
            value=self.trainer.as_text(self.bot.dex, showHp=False,  boldBuffs=True)
            + '\n' + self.points_as_text(True) + '\n\u200b', inline=False)
        e.add_field(name=f'{self.battle.players[self.nOpponent].name}\'s Party',
            value=self.opponent.as_text(self.bot.dex, showHp=False,  boldBuffs=True)
            + '\n' + self.points_as_text(False), inline=False)


        if deck['cached_img']:
            # Only delay when not uploading
            if delay: await asyncio.sleep(delay)
            await self.ctx.send(f'''<@{self.uid}>'s Turn!''', embed=e)
        else:
            sent = await ctx.send(f'''<@{self.uid}>'s Turn!''', embed=e, file=discord.File(png.getvalue(), 'party.png'))
            deck['cached_img'] = sent.embeds[0].image.url
            self.bot.party.save_deck(self.uid, deck)


        # if 'color' in self.data[self.battleNo]:
        #     embed.color = self.data[self.battleNo]['color']
        #     intro.color = self.data[self.battleNo]['color']

        # todo maybe color based on round ?

        self.bot.wfm[self.uid] = {
            'handler': self,
            'channel': self.ctx.channel,
            'expires': time.time() + 30 * 60
        }


    def make_updated_embed(self, results):
        #footer = 'Round: 1/1  Turn: 1/2'
        #footer = 'Round: 1 / 1 • Turn: 1 / 2'
        footer = ''
        log = [f'{self.battle.players[self.nPlayer].name}\'s Turn **{self.trainer.turnsElapsed + 1}**  /  {self.battle.turns}  •  Round {self.battle.round + 1}']

        for result in results:
            log.append(self.step_as_text(result))

        #             .set_image(url=self.data[self.battleNo]['img']) \


        description = DBL_BREAK.join(log)
        embed = discord.Embed(description=description) \
            .set_footer(text=footer) \
            .add_field(name=f'{self.battle.players[self.nPlayer].name}\'s Party',
                value=self.trainer.as_text(self.bot.dex, results[-1]['trainer_buff_snapshot'], showHp=False, boldBuffs=True)
                + '\n' + self.points_as_text(True) + '\n\u200b', inline=False) \
            .add_field(name=f'{self.battle.players[self.nOpponent].name}\'s Party',
                value=self.opponent.as_text(self.bot.dex, results[-1]['enemy_buffs_snapshot'][0], showHp=False, boldBuffs=True)
                + '\n' + self.points_as_text(False), inline=False) \
            .set_image(url=self.img)


        return embed

    def process_actions(self, actions):
        error = None
        results = []
        for action in actions:
            self.skip_blank_steps()
            result = self.battle_step(action, 0)

            if result['error']:
                result['status'] = PLAYER_TURN
                error = f'''Couldn't use **{result['pkmn'].name}**. {ERROR_TEXT[result['error']]}'''
                break

            results.append(result)
            if result['status'] in [PLAYER_TURN_END, PARTY_DEAD]:
                break

        # if result['status'] == PARTY_DEAD:
        #     self.defeated[self.battleNo] = True

        # if all(self.defeated):
        #     result['status'] = QUEST_COMPLETE

        if error and not results:
            return None, error

        if result['status'] == PLAYER_TURN_END:
            pass
            # summary, status = self.enemy_turn()
            # results.append({
            #     'enemy_turn_summary': summary,
            #     'status': status
            # })

        # postResult = self.post_step(result['status'])
        # if postResult:
        #     results.append(postResult)

        return results, error


    def step_as_text(self, step, markup=True):
        p = step['pkmn']
        texts = []

        # if 'buff' in self.bot.dex.pkmn[p.no]:
        #     #     result['applied_buff'] = self.bot.dex.pkmn[p.no]['buff']

        # if step['applied_buff']:
        #     inlineBuff = step['applied_buff'].as_inline_text()
        # else:
        #     inlineBuff = '', ''

        inlineBuff = buff_inline_text(p.dexEntry)

        if step['success']:
            move = '_{}{}_'.format(p.move, f' +**{p.z}**%' if p.z else '')
            texts.append(f'''{typeEmoji[p.type]} **{p.name}** [Lv. **{p.lv}**] used {move}{inlineBuff[0]}''')
        # if SKILL_ACTIVATED in log:
        #     text.append('__**{}** activated!__'.format(common.skillName[m.skill]))

        for event in step['log']:
            try:
                if isinstance(event, str):
                    texts.append(event)

                elif event[0] == SKIP_PKMN:
                    cause = event[1]
                    if cause is None:
                        texts.append(f'{typeEmoji[p.type]}Skipped **{p.name}** [Lv. **{p.lv}**]! It focuses & restores **1** PP.')
                    elif cause == NO_PP:
                        texts.append(f'{typeEmoji[p.type]}Not enough PP, skipped **{p.name}** [Lv. **{p.lv}**]. It focuses & restores **1** PP.')
                    # status = event[1]
                    # if status == SLEEP:
                    #     return 'Skipped {} due to Sleep!'.format(name)
                    # if status == PARA:
                    #     return '**Paralyzed!** Skipped {}!'.format(name)
                    # if status == FREEZE:
                    #     return '**Frozen!** Skipped {}!'.format(name)

                elif event[0] == ENEMY_DAMAGED:
                    _, e, hits, dmg, hpTaken, xType, *rest = event
                    self.battle.points[self.nPlayer] += dmg
                    n = self.engagedParty.index(e)

                    effectiveText = ''
                    if dmg > 1:
                        if xType >= 2.5:
                            effectiveText = f'It\'s extremely effective! [x**{xType}**]'
                        elif xType >= 1.75:
                            effectiveText = f'It\'s super effective! [x**{xType}**]'
                    if xType < 0.5:
                        effectiveText = f'It had minimal effect... [x**{xType}**]'
                    elif xType < 0.8:
                        effectiveText = f'It\'s not very effective... [x**{xType}**]'


                    if dmg > 0:
                        hit = f'''**{self.battle.players[self.nOpponent].name}**'s party takes **{dmg}** dmg'''
                    else:
                        hit = f'''**{self.battle.players[self.nOpponent].name}**'s party takes no damage.'''

                    if KILLED in rest:
                        hit += ' ☠'
                        # hit += ' ☠'# if enemy.name != 'Chest' else ''
                        # # if enemy.deathMessage:
                        # #     hit += ' ' + enemy.deathMessage.format(name='{} [{}]'.format(enemy.name, mob.index(enemy) + 1))
                    else:
                        statusTexts = ['was **poisoned**!', 'was **seeded**!', 'was **burned**!',
                                       'was **paralyzed**!', '**flinched**!', 'fell **asleep**!', 'became **confused**!']
                        addedStatus = False
                        for status in [PSN, SEED, BURN, PARA, FLINCH, SLP, CONFUSE]:
                            if not addedStatus and status in rest:
                                hit = f'{hit} and {statusTexts[status]} {statusEmoji[status]}'
                                addedStatus = True
                                break
                            if dmg > 1 and status * X2_STATUS in rest:
                                if addedStatus:
                                    hit = f'{hit} Critical hit due to **{statusNames[status]}**!'
                                else:
                                    hit = f'{hit} - critical hit due to **{statusNames[status]}**!'

                        if hits:
                            hit += inlineBuff[1]
                        # try:
                        #     timer = int(rest[-1][1:])
                        #     hit += '\n🕑 Its timer decreased to **{}**{}'.format(timer, '!' if timer == 0 else '.')
                        # except (IndexError, AttributeError) as e:
                        #     pass



                    if not markup:
                        hit = re.sub(r'[`*_]', '', hit)
                    texts.append(hit)
                    if effectiveText:
                        texts.append(effectiveText)

                # elif event[0] == SP_RESTORE:
                #     _, hpRestore, spRestore = event
                #     text.append('[+**{}** HP / +**{:.2f}** SP🔋]'.format(hpRestore, spRestore))

                elif event[0] == ONE_TURN_TRIUMPH:
                    texts.append('🎉 _1 Turn Triumph_')

            except TypeError:
                pass

        return '\n'.join(texts).strip()





class Pvp:
    def __init__(self, bot):
        self.bot = bot
        self.openbattles = {}

    @commands.command()
    async def battle(self, ctx, *, args=None):
        if not args:
            print('todo help')
            return

        # remove numbers first for rounds
        mention = self.bot.resolve_tag(ctx.message.guild, args)
        if not mention:
            await send_message(ctx, f'''Couldn't find a trainer in this server by that name!''', error=True)
            return

        players = [ctx.author, mention]
        random.shuffle(players)
        battle = PvpManager(self.bot, ctx, *players)

        text = f'''Format: _{battle.rounds} Round, {battle.turns} Turns_{DBL_BREAK}{mention.name}, type `a` to accept or `no` to decline'''
        e = discord.Embed(description=text, color=INFO_BLUE) \
            .set_author(name=f'{ctx.author.name} would like to battle!', icon_url=pokeballUrl)

        await ctx.send(f'<@{mention.id}>', embed=e)

    async def declined(self, battle):
        del self.bot.pvp.openbattles[battle.p1.id]
        del self.bot.pvp.openbattles[battle.p2.id]
        e = discord.Embed(title='Battle Cancelled', description=f'{battle.p2.name} has declined', color=INFO_BLUE)
        await battle.ctx.send(f'<@{battle.p1.id}>', embed=e)


    @commands.command()
    async def pvptest(self, ctx, *, arg=''):
        await ctx.trigger_typing()

        uid = ctx.author.id
        if not uid in self.bot.pc.cache:
            self.bot.pc.load_db_into_cache(uid)
        userPc = self.bot.pc.cache[uid]
        deck = self.bot.party.load_active_deck(ctx.author.id)

        party = [None] * 6
        for p in userPc['badges']:
            try:
                party[deck['ids'].index(p.id)] = p
            except ValueError:
                pass

        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        boosts = deckBoosts[deckKeys[deck['deck']]]
        party[5] = self.bot.pc.make_pkmn(no=self.bot.dex.sample_from_set(1, 1)[0], lv=50)

        party = to_battle_pkmn(party, boosts, xSlots)
        p1 = TrainerState(party, pvp=True)
        p1.name = ctx.author.name
        p1.points = 0
        if deck['cached_img']:
            p1.img = deck['cached_img']
        else:
            ns = [p.no if p else None for p in party if p]
            p1.img = None
            p1.png = self.bot.render.render_deck(deck['deck'], ns)

        party = []
        nos = self.bot.dex.sample_from_set(6, 1)
        for no in nos:
            p = self.bot.pc.make_pkmn(no=no, lv=50)
            party.append(p)
        party = to_battle_pkmn(party, boosts, xSlots)
        p2 = TrainerState(party, pvp=True)
        p2.points = 0
        p2.name = 'Komala'
        ns = [p.no if p else None for p in party if p]
        p2.img = None
        p2.png = self.bot.render.render_deck(deck['deck'], ns)

        p1Quest = PvpQuest(self.bot, uid, p1, p2)
        await p1Quest.start(ctx)


def setup(bot):
    pvp = Pvp(bot)
    bot.add_cog(pvp)
    bot.pvp = pvp

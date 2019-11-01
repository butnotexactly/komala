import time
import bestiary

from battle import *
from common import *

class TrainerBattle(Quest):
    def __init__(self, bot, uid, trainer, location, data, fixedOrder=True, showHelp=True):
        super(TrainerBattle, self).__init__(bot, uid, E_TRAINER_BATTLE, trainer)
        self.location = location
        self.data = data
        self.parties = []
        for b in data:
            party = []
            for stats in b['party']:
                name, lv, t, *extra, = stats
                if extra:
                    extra, = extra
                p = make_enemy_pkmn(self.bot.dex, name, lv, t, extra)
                p.party = party
                party.append(p)
            self.parties.append(party)

        self.defeated = [False] * len(self.parties)
        self.showHelp = showHelp
        self.fixedOrder = fixedOrder
        self.battleNo = None # 0
        self.engagedParty = None#self.parties[0]
        self.ctx = None

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
            if cmd == 'a':
                chain.append((ATTACK, 1, True))
            elif cmd == 's':
                chain.append(SKIP)
            elif cmd == 'r':
                # immediately run todo
                break
            else:
                try:
                    n = int(cmd)
                    if n > 9:
                        raise ValueError
                except ValueError:
                    return
                chain.append((ATTACK, n, False))

        if chain:
            await self.do_actions(chain)

        #await message.delete()

    async def do_actions(self, actions):

        if self.battleNo is None or self.defeated[self.battleNo]:
            target = 0 if actions[0] == SKIP else actions[0][1] - 1
            return await self.engage_party(target)

        results, error = self.process_actions(actions)
        if results:
            enemyText = None
            if 'enemy_turn_summary' in results[-1]:
                enemyText = results.pop()['enemy_turn_summary']

            embed = self.make_updated_embed(results)
            await self.ctx.send(f'<@{self.uid}>', embed=embed)

            if enemyText:
                await self.ctx.send('', embed=self.make_enemy_embed(enemyText))

        if error:
            await send_message(self.ctx, error, error=True)
        else:
            status = results[-1]['status']
            if status == PARTY_DEAD:
                await self.disengage_party()
                # todo handle choice battles, 3 battles, not fixed order
                if self.defeated.count(False) == 1:
                    await self.engage_party(self.defeated.index(False))


    async def start(self, ctx):
        self.ctx = ctx
        if self.fixedOrder:
            await self.engage_party(0)

    async def engage_party(self, target, findNextTarget=False):
        try:
            if findNextTarget:
                while self.defeated[target]:
                    target += 1
            elif self.defeated[target]:
                await send_message(self.ctx, 'You\'ve already beaten that trainer! Select another by typing the number next to them.', error=True)
                return False

            self.engagedParty = self.parties[target]
            self.battleNo = target

        except IndexError:
            await send_message(self.ctx, 'Invalid trainer! Type the number next to the trainer you want to fight, such as `1` for the trainer labelled 1.', error=True)
            return False

        self.bot.wfm.pop(self.uid, None)

        description = ''
        if self.showHelp:
            commands = f'''- Type `a` or a target (`1`, `2`, `3`) to use your Pokémon's ability
- Type `s` to skip a Pokémon and restore 1 PP
- Type `r` to run
- Type `x` or `auto` to automate fighting{DBL_BREAK}Or quickly chain multiple commands such as: `1 s 1 2`'''
            description += DBL_BREAK + commands
            self.showHelp = False


        footer = ''#f'🌠 Meteor Falls'

        embed = discord.Embed(description=description) \
            .set_image(url=self.data[self.battleNo]['img']) \
            .set_footer(text=footer) \
            .add_field(name='Party', value=self.trainer.as_text(self.bot.dex, boldBuffs=True), inline=False) \
            .add_field(name=f'''{self.data[self.battleNo]['name']} sends out...''', value=self.enemy_party_as_text(init=True), inline=False) \
            .set_author(name=f'''{self.data[self.battleNo]['name']} would like to battle!''', icon_url=pokeballUrl)

        #embed.title = 'Team Rocket Grunt would like to battle!'

        dialog = enquote(self.data[self.battleNo]['o']).replace('[NAME]', self.ctx.author.name)

        intro = discord.Embed(title=self.data[self.battleNo]['name'], description=f"_{dialog}_") \
            .set_thumbnail(url=self.data[self.battleNo]['sprite'])

        if 'color' in self.data[self.battleNo]:
            embed.color = self.data[self.battleNo]['color']
            intro.color = self.data[self.battleNo]['color']

        await self.ctx.send(f'<@{self.ctx.author.id}>', embed=intro)
        ##await asyncio.sleep(3)# todo uncomment
        await self.ctx.send(embed=embed)

        self.bot.wfm[self.uid] = {
            'handler': self,
            'channel': self.ctx.channel,
            'expires': time.time() + 30 * 60
        }

    async def disengage_party(self):
        self.bot.wfm.pop(self.uid, None)
        if 'e' in self.data[self.battleNo]:
            outro = discord.Embed(title=self.data[self.battleNo]['name'], description=f"_{enquote(self.data[self.battleNo]['e'])}_") \
            .set_thumbnail(url=self.data[self.battleNo]['sprite'])

            if 'color' in self.data[self.battleNo]:
                outro.color = self.data[self.battleNo]['color']
            await self.ctx.send(f'<@{self.ctx.author.id}>', embed=outro)
            ##await asyncio.sleep(3)# todo uncomment

    def make_updated_embed(self, results):
        footer = ''
        log = []
        for result in results:
            log.append(self.step_as_text(result))

        description = DBL_BREAK.join(log)
        embed = discord.Embed(description=description) \
            .set_image(url=self.data[self.battleNo]['img']) \
            .set_footer(text=footer) \
            .add_field(name='Party', value=self.trainer.as_text(self.bot.dex, results[-1]['trainer_buff_snapshot'], boldBuffs=True), inline=False) \
            .add_field(name=f'''{self.data[self.battleNo]['name']}''', value=self.enemy_party_as_text(results[-1]['enemy_buffs_snapshot']), inline=False)

        return embed

    def make_enemy_embed(self, text):
        for p in self.engagedParty:
            thumb = p.gif
            color = TYPE_COLORS[p.type]
            if p.hp > 0:
                break
        embed = discord.Embed(title='Team Rocket Grunt\'s Turn!', description=text, color=color) \
                    .set_thumbnail(url=thumb)
        return embed

    def process_actions(self, actions):

        error = None
        results = []
        for action in actions:
            self.skip_blank_steps()
            if action == SKIP:
                result = self.battle_step(SKIP, 0)
            else:
                result = self.battle_step(ATTACK, action[1] - 1, action[2])

            if result['error']:
                result['status'] = PLAYER_TURN
                error = f'''Couldn't use **{result['pkmn'].name}**. {ERROR_TEXT[result['error']]}'''
                break

            results.append(result)
            if result['status'] in [PLAYER_TURN_END, PARTY_DEAD]:
                break

        if error and not results:
            return None, error

        if result['status'] == PARTY_DEAD:
            self.defeated[self.battleNo] = True

        if all(self.defeated):
            result['status'] = QUEST_COMPLETE

        elif self.trainer.hp == 0:
            result['status'] = QUEST_FAILED

        elif result['status'] == PLAYER_TURN_END:
            summary, status = self.enemy_turn()
            results.append({
                'enemy_turn_summary': summary,
                'status': status
            })

        # postResult = self.post_step(result['status'])
        # if postResult:
        #     results.append(postResult)

        return results, error

    # def post_step(self, status):
    #     # print("STATUS", status, self.defeated.count(False))
    #     # if status == PARTY_DEAD:
    #     #     print("COUNT", self.defeated.count(False))
    #     #     if self.defeated.count(False) == 1:
    #     #         return self.engage_mob(self.defeated.index(False))
    #     #     #self.battleNo = None

    #     if status == PLAYER_TURN_END:
    #         summary, status = self.enemy_turn()
    #         return {
    #             'enemy_turn_summary': summary,
    #             'status': status
    #         }

        # if status in [QUEST_COMPLETE, QUEST_FAILED]:
        #     self.c.execute("delete from user_quest where discord_id = ?", [self.uid])
        #     if status == QUEST_COMPLETE and not self.player.practiceGame and self.rd > self.lastCompletedRound:
        #         self.submit_score()
        # else:
        #     self.c.execute("update user_quest set data = ? where discord_id = ? and quest_id = ? and type = ?",
        #         [pickle.dumps(self.quest), self.uid, self.cup, common.QUEST_COLI])


    def enemy_turn(self):
        status = ENEMY_TURN_END

        turns = []
        for i, e in enumerate(self.engagedParty):
            texts = []
            if not e.hp > 0:
                continue

            # todo bestiary get power, name, actions
            # check if death after move (self-destruct / recoil)
            # canAttack = True



            # if SLEEPING in e.statuses and not e.no in [14]:
            #     e.statuses[SLEEPING] -= 1
            #     if e.statuses[SLEEPING] > 0:
            #         texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} is fast asleep''')
            #     else:
            #         texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} woke up!''')
            #         del e.statuses[SLEEPING]
            #     canAttack = False

            # if canAttack and PARALYZED in e.statuses:
            #     if random.random() < 0.25:
            #         texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} is paralyzed! It can't move!''')
            #         canAttack = False

            # if canAttack and CHARMED in e.statuses:
            #     if random.random() < 0.4:
            #         texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} is infatuated! It can't move!''')
            #         canAttack = False

            # if canAttack and FLINCH in e.statuses:
            #     texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} flinched!''')
            #     canAttack = False

            # if canAttack and CONFUSED in e.statuses:
            #     if e.statuses[CONFUSED] > 0:
            #         if random.random() < 1/3:
            #             confuseDmg = min(e.hp, int(e.hpMax / 8))
            #             e.hp -= confuseDmg
            #             texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} is confused! It hurt itself in its confusion!''')
            #             canAttack = False

            #         e.statuses[CONFUSED] -= 1
            #     else:
            #         texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} snapped out of its confusion!''')
            #         del e.statuses[CONFUSED]

            # if canAttack and self.trainer.blocks:
            #     block = self.trainer.blocks[0]
            #     block[0] -= 1
            #     texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} used _{e.move}_\n{block[1]}''')
            #     if block[0] <= 0:
            #         del self.trainer.blocks[0]
            #     canAttack = False

            checkResults = pre_attack_status_check(e, self.trainer, e.sleeptalk)
            if checkResults:
                for r in checkResults:
                    if r == SLEEPING:
                        texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} is fast asleep''')

                    elif r == WOKE:
                        texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} woke up!''')

                    elif r == PARALYZED:
                        texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} is paralyzed! It can't move!''')

                    elif r == CHARMED:
                        texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} is infatuated! It can't move!''')

                    elif r == FLINCHED:
                        texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} flinched!''')

                    elif r == CONFUSED:
                        texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} is confused! It hurt itself in its confusion!''')

                    elif r == SNAPPED:
                        texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} snapped out of its confusion!''')

                    elif isinstance(r, str):
                        texts.append(f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} used _{e.move}_\n{r}''')

            if not checkResults or checkResults[-1] in [WOKE, SNAPPED, DECHARMED]:
                result = e.use_move(self.trainer)
                if 'failed' in result:
                    if result['failed'] == MISSED:
                        text = f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} used _{result['move']}_, but it missed!'''
                    else:
                        text = f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} used _{result['move']}_, {result['failed']}'''
                else:
                    #TODO REMOVE THIS
                    # if 'dmg' in result and result['dmg'] > 0:
                    #     self.trainer.apply_damage(result['dmg'])

                    if 'attack_text' in result:
                        text = f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} {result['attack_text']}'''
                    else:
                        text = f'''`[{i+1}]`{e.emoji}{e.name}{typeEmoji[e.type]} {result['action']} _{result['move']}_ for **{result['dmg']}** dmg!'''

                    if 'x_type' in result:
                        if result['dmg'] > 1:
                            if result['x_type'] >= 2.5:
                                text += ' It\'s extremely effective!'
                            elif result['x_type'] >= 1.75:
                                text += ' It\'s super effective!'
                        if result['x_type'] < 0.5:
                            text += ' It had minimal effect...'
                        elif result['x_type'] < 0.8:
                                text += ' It\'s not very effective...'

                if 'note' in result:
                    text += result['note']

                texts.append(text)

            statusLog = post_attack_status_update(e)
            if statusLog:
                texts.append(status_log_as_text(statusLog, e))

            turns.append('\n'.join(texts))

        update_buffs(self.trainer.buffs, 0, True)
        self.trainer.refresh_flat_buff()

        trainerText = self.trainer.as_text(self.bot.dex, showParty=False, boldBuffs=True)

        output = DBL_BREAK.join(turns) + f'{DBL_BREAK}Party {trainerText}'



    #     playerDescription = "Loadout:  {}\nHP: `{} {}`      SP:  **{}**  /  {}".format(medalEmojis, hp_bar(player.hp, player.hpMax, 600), "{:,}".format(player.hp), player.sp if float(player.sp).is_integer() else "{:.2f}".format(player.sp), player.maxSp)

    # if 0 < player.hp <= 500:
    #     playerDescription += "\n⚠ Peril **!!**"
    # elif 0 < player.hp <= 1000:
    #     playerDescription += "\nDanger **!**"

        return output, status

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
            if not 'generic' in step:
                action = 'used _{}{}_{}'.format(p.move, f' +**{p.z}**%' if p.z else '', inlineBuff[0])
            elif step['generic'] == 'sleeptalk':
                action = 'attacks in its sleep!'

            texts.append(f'''{typeEmoji[p.type]} **{p.name}** [Lv. **{p.lv}**] {action}''')

        # if SKILL_ACTIVATED in log:
        #     text.append('__**{}** activated!__'.format(common.skillName[m.skill]))
        for event in step['log']:
            try:
                if isinstance(event, str):
                    texts.append(event)

                elif event[0] == SKIP_PKMN:
                    cause = event[1]
                    if cause is None:
                        texts.append(f'{typeEmoji[p.type]}Skipped **{p.name}** [Lv. **{p.lv}**]! It focuses & restores **2** PP.')

                    elif cause == NO_PP:
                        texts.append(f'{typeEmoji[p.type]}Not enough PP, skipped **{p.name}** [Lv. **{p.lv}**]. It focuses & restores **2** PP.')

                    elif cause == 'recharge':
                        texts.append(f'''{typeEmoji[p.type]} **{p.name}** [Lv. **{p.lv}**] is recharging.''')

                elif event[0] == 'pre_check':
                    checkResult = event[1]
                    name = f'''{typeEmoji[p.type]} **{p.name}** [Lv. **{p.lv}**]'''

                    if checkResult == SLEEPING:
                        texts.append(f'''{name} is fast asleep''')

                    elif checkResult == WOKE:
                        texts.insert(0, f'''{name} woke up!''')

                    elif checkResult == PARALYZED:
                        texts.append(f'''{name} is paralyzed! It can't move!''')

                    elif checkResult == CHARMED:
                        texts.append(f'''{name} is infatuated! It can't move!''')

                    elif checkResult == FLINCHED:
                        texts.append(f'''{name} flinched!''')

                    elif checkResult == CONFUSED:
                        texts.append(f'''{name} is confused! It hurt itself in its confusion!''')

                    elif checkResult == SNAPPED:
                        texts.insert(0, f'''{name} snapped out of its confusion!''')

                    elif isinstance(checkResult, str):
                        texts.append(f'''{name} used _{p.move}_\n{checkResult}''')

                elif event[0] == ENEMY_DAMAGED:
                    _, e, hits, dmg, hpTaken, xType, criticalHit, damageNote, *rest = event
                    n = self.engagedParty.index(e)
                    if dmg > 0:
                        hit = f'''`[{n+1}]` {e.name} takes **{dmg}** dmg'''
                    elif hits > 0:
                        hit = f'''`[{n+1}]` {e.name} takes no damage...'''
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
                                    hit = f'{hit} Strong hit due to **{statusNames[status]}**!'
                                else:
                                    hit = f'{hit} - strong hit due to **{statusNames[status]}**!'

                        hit += inlineBuff[1]
                    if criticalHit:
                        hit += ' ⚠_Critical hit!_'

                    if xType != 1:
                        #hit += f' [x**{xType}**]'
                        #hit += f' `[x{xType}]`'
                        #hit += f' (x**{xType}**)'
                        #hit += f' [**{xType}**x]'
                        if xType < 1:
                            hit += f' 🔻**{xType}**x'
                        else:
                            hit += f' ☄ **{xType}**x'
                        # try:
                        #     timer = int(rest[-1][1:])
                        #     hit += '\n🕑 Its timer decreased to **{}**{}'.format(timer, '!' if timer == 0 else '.')
                        # except (IndexError, AttributeError) as e:
                        #     pass

                    if damageNote:
                        hit += '\n' + damageNote

                    if not markup:
                        hit = re.sub(r'[`*_]', '', hit)
                    texts.append(hit)

                # elif event[0] == SP_RESTORE:
                #     _, hpRestore, spRestore = event
                #     text.append('[+**{}** HP / +**{:.2f}** SP🔋]'.format(hpRestore, spRestore))

                elif event[0] == ONE_TURN_TRIUMPH:
                    texts.append('🎉 _1st Turn Triumph_')

                elif event[0] == 'status_self':
                    status = event[1]
                    statusTexts = ['was **poisoned**!', 'was **seeded**!', 'was **burned**!',
                                       'was **paralyzed**!', '**flinched**!', 'fell **asleep**!', 'became **confused**!']
                    texts.append(f'{statusEmoji[status]} Your party {statusTexts[status]}!')

                elif event[0] == 'hp+':
                    texts.append(f'❤ Restored **{int(event[1]*100)}**% of your party\'s HP!')

                elif event[0] == 'esuna':
                    texts.append(f'💊 Cured all status ailments!')

                elif event[0] == 'dispel':
                    texts.append(f'💬 Dispelled enemy buffs.')

                elif event[0] == 'recoil' and event[1] > 0:
                    texts.append(f'Hurt by **{event[1]}** recoil damage!')

            except TypeError:
                pass

        if self.trainer.hp == 0:
            texts.append(f'_Your party fainted!_')

        return '\n'.join(texts).strip()


def make_enemy_pkmn(dex, name, lv, t, extra=None):
    no = dex.nos[name]
    data = dex.pkmn[no]

    if name in bestiary.classMap:
        p = bestiary.classMap[name](no, lv, name)
    else:
        p = bestiary.Enemy(no, lv, name)

    p.set_stats_by_lv(p.statLv, p.statLv, p.statLv, data)

    # p.hp = p.hpMax = scale_hp(p.statLv, data['hp'], 0, 0)
    # p.attack = scale_stat(p.statLv, data['atk'], 0, 0, 1)
    # p.defense = scale_stat(p.statLv, data['def'], 0, 0, 1)
    p.type = t
    p.catchRate = data['catch']
    p.wtClass = data['wt_class']
    #todo p.gender

    p.emoji = data['emoji']
    p.gif = data['gif']
    p.move = data['move']

    # p.name = data['name']
    #
    # p.thumb = 'https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/{}.png' \
    #     .format(data['thumbnail'] if data['thumbnail'] else p.name.lower())
    # p.emoji = data['emoji']

    return p


class Gym(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rr(self, ctx, *, arg=''):

        boosts = deckBoosts[deckKeys[0]]
        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        party = to_battle_pkmn(self.bot.party.make_test_party(), boosts, xSlots)
        trainer = TrainerState(party)

        location = 0
        battle = TrainerBattle(self.bot, ctx.author.id, trainer, location, gruntBattle2)
        await battle.start(ctx)


    @commands.command()
    async def rs(self, ctx, *, arg=''):
        uid = ctx.author.id
        deck, party = self.bot.party.load_active_party(uid)

        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        boosts = deckBoosts[deckKeys[deck['deck']]]

        if arg:
            p = self.bot.pc.make_pkmn(name=arg, lv=5)
            party[3] = p

        #party[5] = self.bot.pc.make_pkmn(no=self.bot.dex.sample_from_set(1, 1)[0], lv=5)

        party = to_battle_pkmn(party, boosts, xSlots)
        trainer = TrainerState(party)

        location = 0
        battle = TrainerBattle(self.bot, ctx.author.id, trainer, location, gruntBattle)#gruntBattle2
        await battle.start(ctx)

    @commands.command()
    async def rg(self, ctx, *, arg=''):

        boosts = deckBoosts[deckKeys[0]]
        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        party = self.bot.party.make_test_party()

        for p in party:
           #p.lv = random.randint(30, 50)
           # p.z = zRanges[p.tier()-1][1]#random.randint(10, 150)
           p.z = 0

        if arg:
            p = self.bot.pc.make_pkmn(name=arg, lv=5)
            party[3] = p

        party = to_battle_pkmn(party, boosts, xSlots)
        trainer = TrainerState(party)

        location = 0
        battle = TrainerBattle(self.bot, ctx.author.id, trainer, location, testBattle)
        await battle.start(ctx)

    @commands.command()
    async def oak(self, ctx, *, arg=''):
        uid = ctx.author.id
        deck, party = self.bot.party.load_active_party(uid)

        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        boosts = deckBoosts[deckKeys[deck['deck']]]

        party = to_battle_pkmn(party, boosts, xSlots)
        trainer = TrainerState(party)

        location = 0
        battle = TrainerBattle(self.bot, ctx.author.id, trainer, 101, oakBattle1, showHelp=False)
        await battle.start(ctx)

    @commands.command()
    async def roxie(self, ctx, *, arg=''):
        uid = ctx.author.id
        deck, party = self.bot.party.load_active_party(uid)

        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        boosts = deckBoosts[deckKeys[deck['deck']]]

        party = to_battle_pkmn(party, boosts, xSlots)
        trainer = TrainerState(party)

        location = 0
        battle = TrainerBattle(self.bot, ctx.author.id, trainer, 101, roxieBattle1, showHelp=False)
        await battle.start(ctx)

    @commands.command()
    async def yt(self, ctx, *, arg=''):
        e = discord.Embed(description='https://open.spotify.com/track/0ILwVc88cfxvjcOE4QsMar', title='New Christmas Village')
        #await ctx.send('Welcome to New Christmas Village', embed=e)
        await ctx.send('Welcome to New Christmas Village\nhttps://open.spotify.com/track/0ILwVc88cfxvjcOE4QsMar')



def setup(bot):
    gym = Gym(bot)
    bot.add_cog(gym)
    bot.gym = gym

# min battles to fight again?


'''

https://gamefaqs.gamespot.com/ds/960099-pokemon-heartgold-version/faqs/60167
https://gamefaqs.gamespot.com/gbc/198308-pokemon-gold-version/faqs/49457

https://iimarckus.org/dumps/dfirered.txt


 -'It's my turn! There's no escape!'


A hint?




trainers['grunt_1'] = {
    'party': {
        ['alolan rattata', 5, DARK],
        ['alolan meowth', 7, DARK]
    }
    'name': 'Team Rocket Grunt',
    'sprite': NPCS['tr_grunt_m'],
    'img': 'https://i.imgur.com/UREbBg0.png',
    'o': "A helpless new trainer ...with a Charmander! I've never even seen one before, but it'll be mine soon. Let's go!",
    'e': "I can't believe I lost... what a missed opportunity.",
    'x': "Stay out of Team Rocket's business! Get lost.",
}


'''



'''

`grunt`

<dialog> opener

wait 2 sec

battle starts



You are challenged by
woud like to battle!
challenges you!

sends out:

< list of pokemon> >

'''

trainers = {}

#trainers['grunt_1'] =

gruntBattle = [
    {
        'party': [
            ['Alolan Rattata', 3, DARK],
            ['Alolan Meowth', 2, DARK]
        ],
        'name': 'Team Rocket Grunt',
        'sprite': NPCS['tr_grunt_m'],
        'img': 'https://i.imgur.com/UREbBg0.png',
        'color': 0x222222,
        'o': "A helpless new trainer ...with a Charmander! I've never even seen one before, but it'll be mine soon. Let's go!",
        'e': "I can't believe I lost... what a missed opportunity.",
    }
]


adjust = 40
gruntBattle2 = [
    {
        'party': [
            ['Alolan Rattata', 5 * 2 + adjust, DARK],
            ['Alolan Meowth', 7 * 2 + adjust, DARK]
        ],
        'name': 'Team Rocket Grunt',
        'sprite': NPCS['tr_grunt_m'],
        'img': 'https://i.imgur.com/UREbBg0.png',
        'color': 0x222222,
        'o': "A helpless new trainer ...with a Charmander! I've never even seen one before, but it'll be mine soon. Let's go!",
    },
    {
        'party': [
            ['Alolan Raticate', 12 * 2 + adjust, DARK],
            ['Pancham', 8 * 2 + adjust, EARTH],
            ['Alolan Meowth', 7 * 2 + adjust, DARK]
        ],
        'name': 'Team Rocket Grunt',
        'sprite': NPCS['tr_grunt_m'],
        'img': 'https://i.imgur.com/L38MnJ9.png',
        'color': 0x222222,
        'o': "Hmph! Okay then... how about this?",
        'e': "I can't believe I lost... what a missed opportunity.",
    }
]

lv = 50
testBattle = [
    {
        'party': [
            # ['Sandslash', 7, EARTH],
            # ['Mr. Mime (Psychic)', 5, PSYCHIC],
            # ['Gyarados (Dragon)', 7, DRAGON],
            # ['Magikarp', 5, WATER],
            # ['Komala', 8, NORMAL],
            # ['Electrode', 8, ELECTRIC],
            # ['Voltorb', 8, ELECTRIC],
            # ['Gastly', 8, PSYCHIC],
            # ['Haunter', 8, PSYCHIC],
            # ['Gengar', 8, PSYCHIC],

            # ['Bulbasaur', 8, NATURE],
            # ['Ivysaur', 8, NATURE],
            # ['Venusaur', 8, NATURE],
            # ['Oddish', 8, NATURE],


            # ['Venusaur', 8, NATURE],
            # ['Absol', 8, DARK],
            # ['Castform (Sunny)', 8, FIRE],

            ['Chatot', lv, NORMAL],
            ['Chatot', lv, NORMAL],
            ['Electabuzz', lv, ELECTRIC],
            ['Scyther', lv, NATURE],
        ],
        'name': 'Team Rocket Grunt',
        'sprite': NPCS['tr_grunt_m'],
        'img': 'https://i.imgur.com/UREbBg0.png',
        'color': 0x222222,
        'o': "A helpless new trainer ...with a Charmander! I've never even seen one before, but it'll be mine soon. Let's go!",
        'e': "I can't believe I lost... what a missed opportunity.",
    }
]



oakBattle1 = [
    {
        'party': [
            ['Mega Charizard Y', 99, FIRE],
            ['Mega Venusaur', 99, NATURE],
            ['Mega Blastoise', 99, WATER],
        ],
        'name': 'Professor Oak',
        'sprite': NPCS['oak'],
        'img': 'https://i.imgur.com/2Iz27aW.png',
        'color': 0xAD92DE,
        'o': "[NAME]! Don't hold anything back. Let's go!",
    },
    {
        'party': [
            ['Gyarados (Dragon)', 99, DRAGON],
            ['Porygon-Z', 99, NORMAL],
            ['Snorlax', 99, NORMAL],
        ],
        'name': 'Professor Oak',
        'sprite': NPCS['oak'],
        'img': 'https://i.imgur.com/wztcnuc.png',
        'color': 0xAD92DE,
        'o': "Outstanding! Let's try this.",
        'e': "You've become a remarkable trainer.",
    }
]


roxieBattle1 = [
    {
        'party': [
            ['Venusaur', 45-10, NATURE],
            ['Salandit (Fire)', 39-10, FIRE],
            ['Gloom', 37, NATURE],
            ['Castform (Sunny)', 34, FIRE],
        ],
        'name': 'Gym Leader Roxie',
        'sprite': NPCS['roxie'],
        'img': 'https://i.imgur.com/9r0WIvm.png',
        'color': 0xAD4A94,
        'o': "Get ready! I'm gonna rock some sense into ya!",
    },
    {
        'party': [
            ['Nidoqueen', 53-15, NATURE],
            ['Salazzle (Nature)', 49-15, NATURE],
            ['Gastly', 47-15, PSYCHIC],
        ],
        'name': 'Gym Leader Roxie',
        'sprite': NPCS['roxie'],
        'img': 'https://i.imgur.com/dNyU1pp.png',
        'color': 0xAD4A94,
        'o': "It's not over yet! Time to turn this show around for a victory!",
        'e': "You've become a remarkable trainer.",
    }
]

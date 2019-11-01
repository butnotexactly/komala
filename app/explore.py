import time
import copy
import bestiary
import rpg #todo remove

from battle import *

class WildPokemon(bestiary.Enemy):
    def __init__(self, no, lv, rarity, data):
        super(WildPokemon, self).__init__(no, lv)

        self.set_stats_by_lv(self.statLv * 2, self.statLv, self.statLv, data)

        self.type = data['type']
        self.catchRate = data['catch']

        self.name = base_name(data['name'])
        self.move = data['move']
        self.gif = data['gif']
        self.thumb = data['sprite']
        self.emoji = data['emoji']
        self.rarity = rarity

    # def hp(self):
    #     iv = 0
    #     ev = 0
    #     return scale_hp(self.lv, self.dex.pkmn[self.no]['hp'], iv, ev)

    # def attack(self):
    #     xNature = 1
    #     iv = 0
    #     ev = 0
    #     return scale_stat(self.lv, self.dex.pkmn[self.no]['atk'], iv, ev, xNature)


class PokemonEncounter(Quest):
    def __init__(self, bot, uid, trainer, wp, location, vsTrainer=None, canCatch=True, canRun=True, runAfter=None):
        super(PokemonEncounter, self).__init__(bot, uid, E_PKMN_ENCOUNTER, trainer)
        self.wp = wp
        self.engagedParty = [wp]
        self.location = location
        self.log = None
        self.message = None
        self.embed = None
        self.clearLog = False
        self.ctx = None
        self.vsTrainer = vsTrainer
        self.canCatch = canCatch
        self.canRun = canRun
        self.runAfter = runAfter

    async def build_and_send_message(self, ctx):
        description = self.enemy_party_as_text(init=True)
#         commands = f'''{ICON_ATTACK} or type `a` / `1` to use your Pokémon's ability
# {pokemoji['skip']} or type `s` to skip a Pokémon and restore 1 PP
# {pokemoji['pokeball']} or type `c` to throw a pokeball to catch it!
# {ICON_CLOSE} or type `r` to run{DBL_BREAK}Or quickly chain multiple commands such as: `a a s a c`'''

        commands = [f'''{ICON_ATTACK} or type `a` / `1` to use your Pokémon's ability''',
                    f'''{pokemoji['skip']} or type `s` to skip a Pokémon and restore 1 PP''']
        if self.canCatch:
            commands.append(f'''{pokemoji['pokeball']} or type `c` to throw a pokeball to catch it!''')
        if self.canRun:
            commands.append(f''' \nType `r` at any time to run!''')

        description += DBL_BREAK + '\n'.join(commands)

        if len(self.trainer.party) - self.trainer.party.count(None) > 1:
            description += f'''{DBL_BREAK}You can quickly chain multiple commands such as: `a a s a c`'''

        footer = f'🌠 Meteor Falls • No. {self.wp.no} / Base Set 1'

        self.embed = discord.Embed(description=description, color=TYPE_COLORS[self.wp.type]) \
                .set_image(url=self.wp.gif).set_thumbnail(url=self.wp.thumb).set_footer(text=footer) \
                .add_field(name='Party', value=self.trainer.as_text(self.bot.dex), inline=False)

        if self.vsTrainer:
            self.embed.set_author(name=f'''{self.vsTrainer} would like to battle!''', icon_url=pokeballUrl)
            self.embed.title = f'**{self.vsTrainer}** sends out...'

        self.message = await ctx.send(f'<@{ctx.author.id}>', embed=self.embed)

        reactions = [ICON_ATTACK, pokemoji['skip']]
        if self.canCatch:
            #balls = [pokemoji['pokeball'], pokemoji['greatball']]
            reactions += [pokemoji['pokeball']]

        for reaction in reactions:# + [ICON_CLOSE]:
            await self.message.add_reaction(reaction.strip('<>'))

        self.bot.wfr[self.uid] = self
        self.bot.wfm[self.uid] = {
            'handler': self,
            'channel': self.message.channel,
            'expires': time.time() + 30 * 60
        }
        self.ctx = ctx


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
            if cmd == 'a' or cmd == '1':
                chain.append(ATTACK)
            elif cmd == 's':
                chain.append(SKIP)
            elif cmd == 'c':
                await message.delete()
                if not self.canCatch:
                    return
                if chain:
                    await self.do_actions(chain)
                    #chain = None
                await self.throw_ball()
                return
                #break
            elif cmd == 'r' or cmd == 'run' or cmd == 'exit':
                if not self.canRun:
                    return
                # immediately run
                #chain = []
                await message.delete()
                await self.run()
                return
            else:
                # not valid
                return

        await message.delete()
        if chain:
            await self.do_actions(chain)

    async def handle_reaction(self, reaction, user):

        if reaction.emoji == pokemoji['pokeball']:
            await self.throw_ball()
        else:
            if reaction.emoji == ICON_ATTACK:
                await self.do_actions([ATTACK])
            elif reaction.emoji == pokemoji['skip']:
                await self.do_actions([SKIP])

    async def do_actions(self, actions):
        results = self.process_actions(actions)

        if len(self.trainer.party) - self.trainer.party.count(None) > 1:
            if not self.log and self.trainer.turnsElapsed:
                #await self.message.edit(embed=None)
                await self.message.edit(embed=copy.copy(self.embed))


        self.add_step_results_to_embed(results)
        await self.message.edit(embed=self.embed)
        self.refresh_log()

        status = results[-1]['status']
        if status in [QUEST_COMPLETE, QUEST_FAILED]:
            # todo exp screen
            self.bot.wfr[self.uid] = None
            self.bot.wfm[self.uid] = None
            if self.runAfter:
                await self.runAfter(self.bot, self.ctx, status == QUEST_COMPLETE)


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

        if error and not results:
            return None, error

        if self.wp.hp == 0:
            result['status'] = QUEST_COMPLETE

        elif self.trainer.hp == 0:
            result['status'] = QUEST_FAILED

        elif result['status'] == PLAYER_TURN_END:
            summary, status = self.enemy_turn()
            self.clearLog = True
            results.append({
                'enemy_turn_summary': summary,
                'status': status
            })

        # if result['status'] == MOB_DEAD:
        #     result['status'] = QUEST_COMPLETE

        # postResult = self.post_step(result['status'])
        # if postResult:
        #     results.append(postResult)

        return results

    async def run(self):
        self.bot.wfr.pop(self.uid, None)
        self.bot.wfm.pop(self.uid, None)

        self.embed.title = 'Got away safely!'
        self.embed.description = ''
        self.embed.clear_fields()
        await self.message.edit(embed=self.embed)

        await asyncio.sleep(1)
        await self.bot.rpg.play(self.ctx)


    async def throw_ball(self):

        self.bot.wfr.pop(self.uid, None)
        self.bot.wfm.pop(self.uid, None)

        xBall = 1
        shakes = 0
        while shakes < 4:
            if not shake_check(catchRate=self.wp.catchRate, hp=self.wp.hp, hpMax=self.wp.hpMax, xBall=xBall, xStatus=1):
                break
            shakes += 1

        shakes = 3

        logTitle = f'{ordinal(self.trainer.turnsElapsed + 1)} Turn'

        #await self.remove_enemy_field()
        if not self.log:

            #                self.embed.remove_field(1)

            # if not self.log and self.trainer.turnsElapsed:
            #     await self.message.edit(embed=None)

            self.embed.description = self.enemy_party_as_text()
            self.log = [f'''{pokemoji['pb_small']}Threw a Poké Ball!''']
            self.embed.add_field(name=logTitle, value='\n'.join(self.log), inline=False)
        else:
            self.log.append(f'''{pokemoji['pb_small']}Threw a Poké Ball!''')
            self.embed.set_field_at(1, name=logTitle, value='\n'.join(self.log), inline=False)
        await self.message.edit(embed=self.embed)

        await asyncio.sleep(1)

        for i in range(shakes - 1):
            msg =  ['The ball shakes.',
                'The ball shakes again.',
                'The ball shakes again!!']
            self.log.append(f'_{msg[i]}_')
            self.embed.set_field_at(1, name=logTitle, value='\n'.join(self.log), inline=False)
            await self.message.edit(embed=self.embed)
            await asyncio.sleep(1)

        msg = ['Oh, no! The Pokémon broke free!',
                'Aww! It appeared to be caught!',
                'Aargh! Almost had it!',
                'Shoot! It was so close, too!',
                f'All right!{self.wp.emoji}**{self.wp.name}** was caught!']

        # if shakes < 4:
        #     self.log.append(f'💢{msg[shakes]}')
        # else:
        #     self.log.append(f'''{pokemoji['pb_small']}{msg[shakes]}''')
        # self.embed.set_field_at(1, name=logTitle, value='\n'.join(self.log), inline=False)

        # await self.message.edit(embed=self.embed)
        # await asyncio.sleep(1)

        if shakes < 4:
             self.log.append(f'💢{msg[shakes]}')
             self.embed.set_field_at(1, name=logTitle, value='\n'.join(self.log), inline=False)
        else:
            self.embed.description = f'''{pokemoji['pb_small']}{msg[shakes]}'''
            self.embed.clear_fields()

        await self.message.edit(embed=self.embed)
        await asyncio.sleep(1)



        if shakes < 4:
            await self.message.edit(embed=None)
            self.trainer.turnsElapsed += 1
            self.add_step_results_to_embed([self.post_step(PLAYER_TURN_END)])
            await self.message.edit(embed=self.embed)
            self.refresh_log()
            self.bot.wfr[self.uid] = self
            self.bot.wfm[self.uid] = {
                'handler': self,
                'channel': self.message.channel,
                'expires': time.time() + 30 * 60
            }
        else:
            # todo add pokemon to pc
            await asyncio.sleep(1)
            await self.bot.dex.view_entry(self.ctx, self.wp.no, caught=True)
            await self.ctx.send(f'''{pokemoji['pb_small']} _You can view your new Pokémon in your `.pc`_''')

    def add_step_results_to_embed(self, results):
        stepsLog = []
        enemyText = None

        for result in results:
            if 'enemy_turn_summary' in result:
                enemyText = results.pop()['enemy_turn_summary']
            else:
                stepsLog.append(self.step_as_text(result, True))#len(results) < 3))

        self.embed = discord.Embed(description=self.enemy_party_as_text(results[-1]['enemy_buffs_snapshot'] if results else None), color=TYPE_COLORS[self.wp.type]) \
            .set_image(url=self.wp.gif).set_thumbnail(url=self.wp.thumb).set_footer(text=self.embed.footer.text) \
            .add_field(name='Party', value=self.trainer.as_text(self.bot.dex), inline=False)

        if self.vsTrainer:
            self.embed.title = f'{self.vsTrainer}\'s Party'


        #self.embed.description = self.enemy_party_as_text(results[-1]['enemy_buffs_snapshot'] if results else None)

        if stepsLog:
            logTitle = f'{ordinal(self.trainer.turnsElapsed + 1)} Turn'
            if not self.log:
                self.log = stepsLog
                #self.embed.add_field(name=logTitle, value='\n'.join(self.log), inline=False)
            else:
                self.log += stepsLog
                #self.embed.set_field_at(1, name=logTitle, value='\n'.join(self.log), inline=False)
            self.embed.add_field(name=logTitle, value='\n'.join(self.log), inline=False)


        #self.embed.set_field_at(0, name='Party', value=self.trainer.as_text(self.bot.dex), inline=False)

        if enemyText:
            self.embed.add_field(name='Enemy Turn', value=enemyText, inline=False)

    def refresh_log(self):
        if self.clearLog:
            self.log = None
            self.clearLog = False
            self.embed.remove_field(1)
            self.embed.remove_field(1)


    # def post_step(self, status):
    #     if status == PLAYER_TURN_END:
    #         summary, status = self.enemy_turn()
    #         self.clearLog = True
    #         return {
    #             'enemy_turn_summary': summary,
    #             'status': status
    #         }

    def enemy_turn(self):
        status = ENEMY_TURN_END
        d = random.randint(2, 20)
        action = random.choice(['attacks with', 'strikes back using', 'counters with'])
        text = f'''The wild {self.wp.emoji}{self.wp.name} {action} _{self.wp.move}_ for **{d}** dmg!'''
        update_buffs(self.trainer.buffs, 0, True)
        return text, status

    def enemy_party_as_text(self, buffs=None, barsize=BAR_SIZE, init=False):
        buff = buffs[0] if buffs else None
        if self.vsTrainer:
            text = f'{self.wp.emoji} {self.wp.name}\n'
            # if init:
            #     text = f'**{self.vsTrainer}** sends out...\n{self.wp.emoji} {self.wp.name}\n'
            # else:
            #     text = f'{self.vsTrainer}\'s Party\n`[1]` {self.wp.emoji} {self.wp.name}\n'
        else:
            rarityText = [' They\'re pretty common around here.',
                          '',
                          ' You don\'t always see those!',
                          ' It\'s really rare!'][self.wp.rarity] if init else ''
            text = f'''A wild{self.wp.emoji}**{self.wp.name}** appeared!{rarityText}\n'''


        text += f'''{typeEmoji[self.wp.type]}Lv. **{self.wp.lv}**  ♂   HP:  `{hp_bar(self.wp.hp, self.wp.hpMax, 8):}`  {self.wp.hp}  /  {self.wp.hpMax}{status_as_text(self.wp.statuses)}'''

        #if self.wp.hp > 0:
        if not buff:
            buff = get_flat_buff(self.wp.buffs)

        if not buff.is_zero():
            text += '\n' + buff.as_text()
        return text

    def step_as_text(self, step, markup=False):
        p = step['pkmn']

        # if SKILL_ACTIVATED in log:
        #     text.append('__**{}** activated!__'.format(common.skillName[m.skill]))
        texts = [f'''{typeEmoji[p.type]}{p.name} used _{p.move}_!''']
        for event in step['log']:
            try:
                if event[0] == SKIP_PKMN:
                    cause = event[1]
                    if cause is None:
                        texts[0] = f'{typeEmoji[p.type]}Skipped {p.name}! Restored **2** PP.'
                    elif cause == NO_PP:
                        #texts[0] = f'{typeEmoji[p.type]}Not enough PP, skipped {p.name}! Restored **2** PP.'
                        texts[0] = f'{typeEmoji[p.type]}Not enough PP, skipped **{p.name}**. It focuses & restores 2 PP.'

                    # status = event[1]
                    # if status == SLEEP:
                    #     return 'Skipped {} due to Sleep!'.format(name)
                    # if status == PARA:
                    #     return '**Paralyzed!** Skipped {}!'.format(name)
                    # if status == FREEZE:
                    #     return '**Frozen!** Skipped {}!'.format(name)

                elif event[0] == ENEMY_DAMAGED:
                    _, e, hits, dmg, hpTaken, xType, criticalHit, damageNote, *rest = event
                    if dmg > 0:
                        hit = f'''{typeEmoji[p.type]}{p.name}'s _{p.move}_ deals **{dmg}** dmg!'''
                    else:
                        hit = f'''{typeEmoji[p.type]}{p.name}'s _{p.move}_ deals **{dmg}** dmg...'''

                    if KILLED in rest:
                        pass
                        # hit += ' ☠'# if enemy.name != 'Chest' else ''
                        # # if enemy.deathMessage:
                        # #     hit += ' ' + enemy.deathMessage.format(name='{} [{}]'.format(enemy.name, mob.index(enemy) + 1))
                    else:
                        statusTexts = ['was **poisoned**!', 'was **seeded**!', 'was **burned**!',
                                       'was **paralyzed**!', '**flinched**!', 'fell **asleep**!', 'became **confused**!']
                        # statusTexts = ['was poisoned!', 'was seeded!', 'was burned!',
                        #                'was paralyzed!', 'flinched!', 'fell asleep!', 'became confused!']
                        for status in [PSN, SEED, BURN, PARA, FLINCH, SLP, CONFUSE]:
                            if status in rest:
                                hit = f'{hit} {e.name} {statusTexts[status]}'# {statusEmoji[status]}'
                                break
                        # try:
                        #     timer = int(rest[-1][1:])
                        #     hit += '\n🕑 Its timer decreased to **{}**{}'.format(timer, '!' if timer == 0 else '.')
                        # except (IndexError, AttributeError) as e:
                        #     pass

                    if not markup:
                        hit = re.sub(r'[`*_]', '', hit)
                    texts[0] = hit


                # elif event[0] == SP_RESTORE:
                #     _, hpRestore, spRestore = event
                #     text.append('[+**{}** HP / +**{:.2f}** SP🔋]'.format(hpRestore, spRestore))

            except TypeError:
                pass

        if self.trainer.hp == 0:
            texts.append(f'_Your party fainted!_')

        if self.wp.hp == 0:
            if self.vsTrainer:
                texts.append(f'''☠ {self.vsTrainer}'s {self.wp.name} fainted! You win!''')
            else:
                texts.append(f'''☠ The wild {self.wp.name} fainted!''')

        return '\n'.join(texts).strip()

    async def remove_enemy_field(self):
        for i, field in enumerate(self.embed.fields):
            if 'Enemy Turn' in field.name:
                self.embed.remove_field(i)
                return

class Explore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def engage(self, ctx, location, name, lv, rarity=AVERAGE):
        uid = ctx.author.id
        deck, party = self.bot.party.load_active_party(uid)

        if not any(party):
            await send_message(ctx, f'You don\'t have any Pokémon in your active party! Try using `.equip` or `.equip auto`.', error=True)
            return False

        #party[5] = self.bot.pc.make_pkmn(no=self.bot.dex.sample_from_set(1, 1)[0], lv=5)

        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        boosts = deckBoosts[deckKeys[deck['deck']]]
        party = to_battle_pkmn(party, boosts, xSlots)
        trainer = TrainerState(party)

        try:
            no = self.bot.dex.nos[name]
        except KeyError:
            await ctx.send(f'You encountered a {name}! ...but its not in the game yet. Try `ex` again!')
            return

        wp = WildPokemon(no, lv, rarity, self.bot.dex.pkmn[no])
        quest = PokemonEncounter(self.bot, ctx.author.id, trainer, wp, location)
        await quest.build_and_send_message(ctx)


    @commands.command()
    async def ex5(self, ctx, *, arg=''):

        boosts = deckBoosts[deckKeys[0]]
        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        party = to_battle_pkmn(self.bot.party.make_test_party(5, 5), boosts, xSlots)
        trainer = TrainerState(party)

        no, = self.bot.dex.sample_from_set(1, 1)

        wp = WildPokemon(no, 5, self.bot.dex.pkmn[no])
        location = 0
        quest = PokemonEncounter(self.bot, ctx.author.id, trainer, wp, location)
        await quest.build_and_send_message(ctx)

    @commands.command()
    async def rival(self, ctx, *, arg=''):
        uid = ctx.author.id
        deck, party = self.bot.party.load_active_party(uid)

        if not any(party):
            await send_message(ctx, f'You don\'t have any Pokémon in your active party! Try using `.equip` or `.equip auto`.', error=True)
            return False


        xSlots = [1.3, 1.4, 1.5, 1.6, 1.7]
        xSlots.append(1 + sum(xSlots[i] - 1 for i in range(5)) / 8.35)
        boosts = deckBoosts[deckKeys[deck['deck']]]
        party = to_battle_pkmn(party, boosts, xSlots)
        trainer = TrainerState(party)

        no = self.bot.dex.nos['Charmander']
        wp = WildPokemon(no, 5, AVERAGE, self.bot.dex.pkmn[no])
        quest = PokemonEncounter(self.bot, ctx.author.id, trainer, wp, None, vsTrainer='Gary', canCatch=False, canRun=False, runAfter=rpg.pallet.post_rival_battle)
        await quest.build_and_send_message(ctx)




def setup(bot):
    explore = Explore(bot)
    bot.add_cog(explore)
    bot.explore = explore
from common import *
from . import cinnasea

ID = 1

PAL_PALLET_TOWN = 100
PAL_OAKS_LAB = 101

def setup(areas, ow):
    areas[ID] = {
        'name': 'Pallet Town',
        'emoji': '🎨 ',#<:pik:414522420196540417>',
        'dialog': '',
    }


    # Pallet Town
    async def pal_pallet_town_ex(handler, arg):
        if arg == 'lab':
            await handler.move_to(PAL_OAKS_LAB)
            return True

        if arg == 'sea':
            await handler.show_dialog('Cinnabar Sea', f'A beautiful open sea! Why not try using a water Pokémon to cross it? Equip one anywhere in your party using `.equip` and then type `1 sea` where `1` would be the Pokémon\'s position in your party.{DBL_BREAK}In other words, `3 sea` means try to use your third Pokémon on the `sea`. Likewise, `2 tree` means use your second on a `tree`.')
            return False

        action = await handler.parse_pkmn_action(arg)
        if action:
            if action == -1:
                return False
            p, party, slot, target = action

            if 'sea' in target:
                if p.type() == WATER:
                    await handler.show_dialog('', f'{p.format_name()} used **Whirlpool**! The currents subsided to a calm, still water. You can cross now, well done!{DBL_BREAK}There are many puzzles to solve using your Pokémon, so be sure to try using them often! Different ones will produce different effects.', color=TYPE_COLORS[p.type()], image=p.dex_entry()['gif'], thumb=True, ping=False)
                    handler.state.progress['pt_sea'] = True
                    #await asyncio.sleep(0.5)
                    #await handler.move_to(cinnasea.CS_SHORE)
                    #await handler.ctx.send('_Well done! you can use your various pokemon in tons of ways to solve puzzles during this RPG, so be sure to try it often! Different ones will produce different effects._', delete_after=12)
                    return True

                await handler.show_dialog('', f'''{p.format_name()} used **{p.dex_entry()['move']}**, but it had no affect. The water rages on... :(''', color=TYPE_COLORS[p.type()], image=p.dex_entry()['gif'], thumb=True)

    async def pal_pallet_town_move(handler, direction):
        # todo add back
        # if 'fought_rival' not in handler.state.progress:
        #     await handler.show_dialog('Professor Oak', enquote('Come see in my `lab` first!'), image=NPCS['oak'])
        #     return False

        if direction == S:
            if 'pt_sea' not in handler.state.progress:
                # handler.show_dialog('Cinnabar Sea', f'The current is far too strong. Why not try using a water Pokémon? Equip one anywhere in your party using `.equip` and then type `1 sea` where `1` would be the Pokémon\'s position in your party.{DBL_BREAK}In other words, `3 sea` means try to use your third Pokémon on the `sea`. Likewise, `2 tree` means use your second on a `tree`.')
                handler.message = None
                await handler.show_dialog('Cinnabar Sea', f'''The current is far too strong! A water Pokémon can help.{DBL_BREAK}Equip one anywhere in your party using `.equip`, then type `1 sea` where `1` would be the Pokémon\'s position in your party.{DBL_BREAK}In other words,
`3 sea` -> try to use your third Pokémon on the `sea`
`2 tree` -> use your second Pokémonon a `tree`{DBL_BREAK}You can solve lots of puzzles using Pokémon this way!''')
                return False

        return True


    ow[PAL_PALLET_TOWN] = {
        'name': 'Outdoors',
        'desc': '',
        'img': 'https://i.imgur.com/eu55aWZ.png',
        'ex': pal_pallet_town_ex,
        'move': pal_pallet_town_move,
        'actions': ['lab', 'sea'],
    }

    # Oak's Lab
    async def pal_oaks_lab_ex(handler, arg):
        if arg == 'exit':
            await handler.move_to(PAL_PALLET_TOWN)
            return True

        if arg == 'oak':
            if 'fought_rival' not in handler.state.progress:
                await handler.show_dialog('Professor Oak', enquote(f'''Ah, {handler.name()}! There you are. My grandson should be arriving soon... and here he is now! Let's learn to battle! It'll be pretty simple since you both only have one Pokémon each.'''), image=NPCS['oak'])
                # todo freeze player from doing other commands / actions
                await asyncio.sleep(5)
                await handler.show_dialog('Gary Oak', enquote('''Let's check out our new Pokémon! Come on, I'll take you on!'''), image=NPCS['gary'], ping=False)

            else:
                await handler.show_dialog('Professor Oak', enquote('Come see me sometimes. I want to know how your Pokédex is coming along.'), image=NPCS['oak'])



            return True

        return False

    # async def post_rival_battle(self, win=True):
    #     handler.state.progress['fought_rival'] = True
    #     await asyncio.sleep(5)
    #     await handler.show_dialog('Gary Oak', enquote('Unbelievable! I picked the wrong Pokémon!'), image=NPCS['gary'])


    ow[PAL_OAKS_LAB] = {
        'name': 'Oak\'s Lab',
        'desc': '',
        'img': 'https://i.imgur.com/U2Ok0FL.png',
        'ex': pal_oaks_lab_ex,
        'paths': [None, None, PAL_PALLET_TOWN, None],
        'actions': ['oak', 'ball'],
    }

async def post_rival_battle(bot, ctx, win=True):
    await asyncio.sleep(1)
    handler = await bot.rpg.play(ctx, showLocation=False)
    handler.state.progress['fought_rival'] = True
    await handler.show_dialog('Gary Oak', enquote('Unbelievable! I picked the wrong Pokémon!') + DBL_BREAK + '_Well done! You can type `.map` (`.x` for short) to continue your adventure._', image=NPCS['gary'])


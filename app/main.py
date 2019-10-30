import os
import asyncio
import random
import secrets
import discord
import logging
import traceback
import sys
import difflib
import time

#import context
import error
import battle
import checks

from common import *
from game import *

from discord.ext import commands

initial_extensions = (
    'common',
    'admin',
    'error',
    'render',
    'pokedex',
    'pc',
    'party',
    'battle',
    'explore',
    'gym',
    'bestiary',
    'rpg',
    'pvp',
)

def command_prefixes(bot, message):
    return ['.', ',', ';', '!']

# https://discordapp.com/oauth2/authorize?client_id=413774553047891989&scope=bot&permissions=0

class PkmnBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=command_prefixes)

        self.render = None
        self.dex = None
        self.pc = None
        self.party = None
        self.battle = None
        self.explore = None
        self.gym = None
        self.rpg = None
        self.pvp = None

        self.userdb = sqlite3.connect('data/users.db')

        self.wfr = {}
        self.wfm = {}

        # id, type, <other data>... like time (if applicable) or quest object


        # self.client_id = config.client_id
        # self.carbon_key = config.carbon_key
        # bots_key = config.bots_key
        # self.session = aiohttp.ClientSession(loop=self.loop)

        #self.add_command(self.do)

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    '''
    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=context.Context)

        if ctx.command is None:
            return

        await self.invoke(ctx)
    '''

    def resolve_tag(self, server, name):
        if not name:
            return None

        match = idPattern.search(name)
        if match:
            return match.group(1)

        name = name.lower().strip()
        matches = difflib.get_close_matches(name, [m.nick if m.nick else m.name for m in server.members], n=1)
        if matches:
            return server.get_member_named(matches[0])

        return None

bot = PkmnBot()

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

    playing = discord.Game(name='with Pokéballs')
    await bot.change_presence(activity=playing)


@bot.event
async def on_reaction_add(reaction, user):

    #print(f"Reaction added: {reaction.message.id}")
    #if reaction.message.id in bot.wfr and bot.wfr[reaction.message.id].uid == user.id:
    if user.id in bot.wfr and bot.wfr[user.id].message.id == reaction.message.id:
        await bot.wfr[user.id].handle_reaction(reaction, user)
        await reaction.message.remove_reaction(reaction, user)

    #await reaction.message.remove_reaction(reaction, user)

    # when a post is made, add it to temporary memory with reactions



    #client.delete_message(reaction.message)

@bot.event
async def on_message(message):
    if message.author == bot.user or message.guild is None:
        return

    await bot.process_commands(message)
    uid = message.author.id
    if uid in bot.wfm:
        data = bot.wfm[uid]
        if data['channel'] != message.channel:
            return
        try:
            if time.time() > data['expires']:
                del bot.wfm[uid]
                return
        except KeyError:
            pass

        await data['handler'].handle_message(message)

    if uid in bot.pvp.openbattles:
        b = bot.pvp.openbattles[uid]
        if time.time() > b.expires:
            bot.pvp.battle_timeout(b)
            return
        await b.handle_message(message)


@bot.command()
async def test(ctx, arg=''):
    message = await send_message(ctx, 'Some cool error message goes here.', error=True)

@bot.command()
async def register(ctx, arg=''):
    handler = GameHandler(ctx)
    await handler.register(arg)

@bot.command(aliases=['sf', 'sz'])
async def safari(ctx, arg=''):
    await ctx.send('Safari! Type: {}'.format(arg))

# @bot.command(aliases=['deck'])
# async def party(ctx, arg=''):
#     async with ctx.typing():
#         png = bot.render.render_deck(random.randint(0, 9), [random.randint(0, 3) for i in range(6)])
#         e = discord.Embed().set_image(url='attachment://party.png')
#         await ctx.send(embed=e, file=discord.File(png.getvalue(), 'party.png'))


    # await ctx.send(file=discord.File(png, 'new_filename.png'))
    # await ctx.send('Saved')


@bot.command()
@checks.is_jacob()
async def admin(ctx):
    await ctx.send('Some admin command')


@bot.command(name='reloadall', aliases=['reall'], hidden=True)
async def _reloadall(ctx, arg=''):
    """Reloads all modules."""

    bot.wfm = {}
    bot.wfr = {}
    try:
        for extension in initial_extensions:
            bot.unload_extension(extension)
            bot.load_extension(extension)
    except Exception as e:
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')
    else:
        await ctx.send('\N{OK HAND SIGN}')

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

# error.setup(bot)


with open('../config/discord-app.json') as f:
    config = json.load(f)

bot.run(config['token'])

# def load_poke_db(self):
#     if not pokedb:
#         pokedb = sqlite3.connect('data/pokedex.db')
#         pokec = pokedb.cursor()

# def load_user_db(self):
#     if not userdb:
#         userdb = sqlite3.connect('data/users.db')
#         userc = userdb.cursor()
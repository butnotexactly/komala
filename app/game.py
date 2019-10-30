import sqlite3

import trainer

from common import *

class GameHandler(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.uid = ctx.author.id
        #self.trainer = None

    # def load_trainer(self):
    #     pass

    def has_account(self, uid=None):
        return userc.execute('select trainer_id from trainer where discord_id = ?', [uid or self.uid]).fetchone() is not None

    async def register(self, arg):
        if not arg or arg == 'help':
            return await self.ask_to_register(dm=False)

        errorMsg = '''Please pick a version or type `.register help` for details on the differences:
 
{c} `.register red`
{s} `.register blue`
{b} `.register green`
 
{p} + {c}{s}{b} `.register yellow`'''.format(c=pokemoji['poke'][0], s=pokemoji['poke'][0], b=pokemoji['poke'][0], p=pokemoji['poke'][0])
        try:
            version = ('red', 'blue', 'green', 'yellow').index(arg.lower().strip())
        except ValueError:
            await send_message(self.ctx, errorMsg, expires=15, error=True)
            return False

        if self.has_account(self.uid):
            await send_message(self.ctx, 'You''re already registered! <:blobaww:360940687287648256>', error=True)
            return False

        return await trainer.register_user(self.ctx, self.uid)

    async def ask_to_register(self, dm=False):
        await send_message(self.ctx, "Register or something!")


import importlib
import sys
import traceback
import sqlite3
import re
import asyncio

from battle import *
from common import *

import explore
import rpg

class FakeBot(object):
    def __init__(self):
        self.extensions = {}
        self.render = None
        self.dex = None
        self.pc = None
        self.party = None
        self.battle = None
        self.explore = None
        self.rpg = None
        self.gym = None

        self.userdb = 1

        self.wfr = {}
        self.wfm = {}

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

        init_emoji(self)

    def load_extension(self, name):
        if name in self.extensions:
            return

        lib = importlib.import_module(name)
        if not hasattr(lib, 'setup'):
            del lib
            del sys.modules[name]
            raise ValueError('extension does not have a setup function')

        lib.setup(self)
        self.extensions[name] = lib

    def add_cog(self, cog):
        pass

    def get_emoji(self, emoji):
        return str(emoji)

def printc(text):
    #text = re.sub(r'<(:.*?:)[0-9]*>', r'\1', text)
    text = re.sub(r'<:t([a-z]{1,2}):[0-9]*>', r'<\1>'.upper(), text)
    #text = re.sub(r'<(:.*?:)[0-9]*>', r'\1', text)
    text = re.sub(r'<(:.*?:)[0-9]*>', ' ', text)
    text = re.sub(r'[`*_]', '', text)
    print(text)



initial_extensions = (
    #'admin',
    #'error',
    'render',
    'pokedex',
    'pc',
    # 'party',
    # 'battle',
    # 'explore',
    # 'gym',
    'rpg',
)


fakebot = FakeBot()
dex = fakebot.dex

# print('render')
# fakebot.render.render_all()

# print('done')


#pprint(dex.pkmn)

numHtml = [f'<span class="icon-num">{i}</span>' for i in range(10)]

def format_as_html(text):
    text = text.replace('\n', '<br>')
    text = re.sub(r'<:t([a-z]{1,2}):[0-9]*>', r'<img class="icon" src="images/types/\1.png">', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    text = text.replace('\u2006', '')
    text = text.replace('/n.png"', '/normal.png"')
    text = text.replace('/fr.png"', '/fire.png"')
    text = text.replace('/w.png"', '/water.png"')
    text = text.replace('/na.png"', '/nature.png"')
    text = text.replace('/el.png"', '/electric.png"')
    text = text.replace('/e.png"', '/earth.png"')
    text = text.replace('/i.png"', '/ice.png"')
    text = text.replace('/p.png"', '/psychic.png"')
    text = text.replace('/f.png"', '/fairy.png"')
    text = text.replace('/dr.png"', '/dragon.png"')
    text = text.replace('/d.png"', '/dark.png"')
    text = text.replace('/ra.png"', '/rainbow.png"')

    for i, emoji in enumerate(noEmoji):
        text = text.replace(emoji, numHtml[i])

    return text


async def view_all():
    ns = [1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 13, 181, 182, 41, 42, 43, 44, 15, 16, 17, 60, 61, 62, 63, 194, 195, 197, 198, 26, 27, 106, 107, 92, 93, 94, 45, 46, 47, 48, 30, 110, 111, 80, 81, 82, 108, 109, 69, 70, 71, 83, 84, 85, 228, 209, 210, 64, 65, 66, 54, 55, 56, 57, 190, 191, 170, 171, 86, 87, 28, 29, 58, 59, 79, 37, 38, 39, 40, 74, 75, 76, 67, 68, 167, 168, 123, 124, 114, 115, 112, 113, 119, 105, 205, 206, 162, 163, 164, 165, 192, 193, 20, 21, 23, 24, 223, 129, 133, 130, 134, 137, 138, 140, 141, 143, 144, 146, 147, 183, 184, 150, 151, 154, 155, 220, 221, 202, 203, 88, 89, 90, 91, 118, 120, 122, 121, 217, 218, 125, 126, 156, 157, 160, 161, 187, 176, 177, 116, 117, 99, 102, 100, 103, 101, 104, 174, 175, 214, 179, 180, 78, 127, 128, 49, 50, 51, 52, 53, 166, 227, 35, 36, 188, 213, 25, 207, 208, 211, 212, 199, 200, 189, 226, 224, 225, 201, 215, 216, 204, 169, 95, 96, 97, 98, 178, 148, 149, 222, 185, 186, 172, 173, 31, 32, 33, 34, 14, 219, 72, 73]

    data = {}
    for n in ns:
        e = await dex.view_entry(None, n, returnEmbed=True)
        #pprint(e.fields)
        # print(format_as_html(e.title))
        description, bio = format_as_html(e.description).split('<br><br>', 1)
        # print(description)
        # print(bio)
        # print(e.thumbnail.url)

        fields = []
        for f in e.fields:
            if 'Habitats' in f.name:
                continue

            name = format_as_html(f.name)
            name = name.replace('⚔', '<img class="icon" src="images/shield.png">')
            name = name.replace('💥', '<img class="icon" src="images/sword.png">')
            name = name.replace('✨', '<img class="icon" src="images/sparkles.svg">')

            value = format_as_html(f.value)

            fields.append({
                'name': name,
                'value': value
            })

        entry = dex.pkmn[n]
        data[n] = {
            'name': e.title,
            'desc': description,
            'bio': bio,
            'footer': e.footer.text,
            'img': e.image.url,
            'thumb': e.thumbnail.url,
            'type': entry['type'],
            'fields': fields,
        }
        '''
        ** with strong
        __ with em
        \n with <br>
        img
        title
        thumb
        footer
        color
        '''

    print('var dict = ' + str(data))



arr = []
for k,v in rpg.ow.items():
    arr.append([v['name'], v['img']])
print(arr)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(view_all())
# loop.close()
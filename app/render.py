import random
import asyncio
import io
import time
import os
import math

from PIL import Image
from common import *
from discord.ext import commands

OPTIMIZE = False

class Render(commands.Cog):
    def __init__(self, bot):
        # self.db = db
        self.bot = bot
        self.pkmn = {}
        self.evolve = {}
        self.decks = [None] * 20

        # path = 'assets/pokemon/170/'#compressed
        # fns = os.listdir(path)
        # for i in range(len(fns)):
        #     #self.pokemon[i] = Image.open('{}{}'.format(path, fns[i])).convert('RGBA')
        #     self.pokemon.append(Image.open('{}{}'.format(path, fns[i])).convert('RGBA'))
        #     self.pkmn[fns[i]] =
        #     #self.pokemonFull[i] = Image.open('assets/pokemon/300 compressed/{}.png'.format(fns[i])).convert('RGBA')

        path = 'assets/pkmn/standard/'
        for folder in os.listdir(path):
            for fn in os.listdir(path + folder):
                if fn in ['type.png', 'evolve 1.png', 'evolve 2.png', 'evolve 3.png']:
                    continue
                self.pkmn[fn[:-4]] = Image.open('{}{}/{}'.format(path, folder, fn)).convert('RGBA')

        path = 'assets/pkmn/evolve/'
        for folder in os.listdir(path):
            for fn in os.listdir(path + folder):
                self.evolve[fn[:-6]] = Image.open('{}{}/{}'.format(path, folder, fn)).convert('RGBA')

        for i, fn in enumerate(deckKeys):
            self.decks[i] = Image.open('assets/decks/compressed/{}.png'.format(fn)).convert('RGBA')

    def render_pc(self, ns):
        #ns = [i for i in range(random.randint(1,16))]
        size = 170

        count = len(ns)

        if count == 3:
            rows, columns = 1, 3
        elif count == 8:
            rows, columns = 2, 4
        elif count >= 10:
            rows, columns = 3, 4
        else:
            a = math.ceil(math.sqrt(count))
            b = math.ceil(count/a)
            columns  = max(a, b)
            rows     = min(a, b)

        # fp = 'cache/pc/pc.png'
        if True:#not os.path.isfile(fp):
            ox, oy, dx, dy = 0, 0, 0, 0
            canvas = Image.new('RGBA', (size * columns, size * rows), 'white')
            for i, no in enumerate(ns):
                #image = random.choice(self.pokemon)#images[n]
                #image = random.choice(list(self.pkmn.values()))
                key = self.bot.dex.pkmn[abs(no)]['key']
                image = self.pkmn[key] if no >= 0 else self.evolve[key]
                canvas.paste(image, (ox + i % columns * (size + dx), oy + int(i / columns) * (size + dy)), image)

            png = io.BytesIO()
            canvas.save(png, format='PNG', optimize=OPTIMIZE)
            png.seek(0)

            # with open(fp, 'wb') as f:
            #     f.write(png)

            return png

    def render_deck(self, deck, ns):

        #todo if empty page just return fixed image

        canvas = self.decks[deck].copy()
        slotPositions = ((230, 23), (230 + 188, 23), (230 + 188 * 2, 23), (144, 212), (144 + 188, 212), (144 + 188 * 2, 212))
        for i, no in enumerate(ns):
            if no is None:
                continue
            #image = random.choice(self.pokemon)#self.pokemon[n]
            #image = random.choice(list(self.pkmn.values()))
            key = self.bot.dex.pkmn[no]['key']
            image = self.pkmn[key]
            canvas.paste(image, slotPositions[i], image)

        png = io.BytesIO()
        canvas.save(png, format='PNG', optimize=OPTIMIZE)
        png.seek(0)
        
        return png



    def render_all(self):
        #ns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 181, 182, 41, 43, 42, 44, 16, 17, 60, 62, 61, 63, 194, 195, 197, 198, 26, 106, 27, 107, 92, 93, 94, 45, 47, 46, 48, 30, 110, 111, 80, 81, 82, 108, 109, 69, 70, 71, 83, 84, 209, 210, 65, 55, 57, 190, 171, 87, 29, 58, 59, 79, 37, 38, 39, 40, 74, 68, 167, 168, 15, 123, 124, 114, 115, 113, 119, 105, 85, 205, 206, 191, 162, 164, 192, 193, 20, 23, 21, 24, 75, 170, 86, 28, 223, 66, 129, 133, 130, 134, 137, 140, 138, 141, 143, 146, 144, 147, 183, 184, 150, 154, 151, 155, 112, 220, 221, 202, 203, 88, 89, 90, 91, 118, 120, 122, 217, 218, 125, 126, 156, 160, 157, 161, 187, 176, 177, 116, 117, 99, 100, 101, 102, 103, 104, 174, 175, 214, 179, 180, 54, 56, 64, 78, 67, 163, 165, 76, 121, 127, 128, 49, 50, 51, 52, 53, 166, 227, 35, 36, 188, 213, 25, 207, 208, 211, 212, 199, 200, 189, 226, 224, 225, 201, 215, 216, 204, 169, 95, 97, 96, 98, 178, 148, 149, 222, 185, 186, 172, 173, 31, 33, 32, 34, 14, 219, 72, 73]

        ns = [1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 13, 181, 182, 41, 42, 43, 44, 15, 16, 17, 60, 61, 62, 63, 194, 195, 197, 198, 26, 27, 106, 107, 92, 93, 94, 45, 46, 47, 48, 30, 110, 111, 80, 81, 82, 108, 109, 69, 70, 71, 83, 84, 85, 228, 209, 210, 64, 65, 66, 54, 55, 56, 57, 190, 191, 170, 171, 86, 87, 28, 29, 58, 59, 79, 37, 38, 39, 40, 74, 75, 76, 67, 68, 167, 168, 123, 124, 114, 115, 112, 113, 119, 105, 205, 206, 162, 163, 164, 165, 192, 193, 20, 21, 23, 24, 223, 129, 133, 130, 134, 137, 138, 140, 141, 143, 144, 146, 147, 183, 184, 150, 151, 154, 155, 220, 221, 202, 203, 88, 89, 90, 91, 118, 120, 122, 121, 217, 218, 125, 126, 156, 157, 160, 161, 187, 176, 177, 116, 117, 99, 102, 100, 103, 101, 104, 174, 175, 214, 179, 180, 78, 127, 128, 49, 50, 51, 52, 53, 166, 227, 35, 36, 188, 213, 25, 207, 208, 211, 212, 199, 200, 189, 226, 224, 225, 201, 215, 216, 204, 169, 95, 96, 97, 98, 178, 148, 149, 222, 185, 186, 172, 173, 31, 32, 33, 34, 14, 219, 72, 73]


        #ns = list(range(1, 40))
        #ns = ns[:70]
        size = 200#170

        count = len(ns)

        a = math.ceil(math.sqrt(count))
        b = math.ceil(count/a)
        columns  = max(a, b)
        rows     = min(a, b)

        ox, oy, dx, dy = 0, 0, 0, 0
        canvas = Image.new('RGBA', (size * columns, size * rows), 'white')
        for i, no in enumerate(ns):
            #image = random.choice(self.pokemon)#images[n]
            #image = random.choice(list(self.pkmn.values()))
            key = self.bot.dex.pkmn[abs(no)]['key']
            # try:
            #     image = self.evolve[key]
            # except KeyError:
            #     image = self.pkmn[key]

            image = self.pkmn[key]
            canvas.paste(image, (ox + i % columns * (size + dx), oy + int(i / columns) * (size + dy)), image)

        png = io.BytesIO()
        canvas.save(png, format='PNG', optimize=True)
        png.seek(0)

        fp = 'all.png'
        with open(fp, 'wb') as f:
            f.write(png)


def setup(bot):
    render = Render(bot)
    bot.add_cog(render)
    bot.render = render

import os
import re
import random
import math

from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing
from wand.display import display
from wand.color import Color

DISCORD = '#32363B'
ICE = '#9dd1f2'
DRAGON = '#646eab'
WATER = '#78a4bf'
FIRE = '#e88158'
ELECTRIC = '#f2cb6f'
FAIRY = '#f0a1c1'
DARK = '#6b6b6b'
NATURE = '#7fbf78'
NORMAL = '#838383'
EARTH = '#9c6e5a'
PSYCHIC = '#bd8cbf'
WHITE = '#fafafa'


class TrainerGenerator(object):
    def __init__(self):
        self.emblems = {}
        self.pokemon = {}
        self.balls = {}
        self.trainers = {}
        self.markers = {}
        self.numbers = {}

    def load_all_images(self):
        for dir in os.listdir('separate 300/'):
            for filename in os.listdir('separate 300/' + dir):
                if filename in ['type.png']:
                    continue
                self.pokemon[filename[:-4]] = Image(filename='separate 300/' + dir + '/' + filename)

        for filename in os.listdir('battle/pokeballs'):
            self.balls[filename[:-4]] = Image(filename='battle/pokeballs/' + filename)

        for filename in os.listdir('battle/trainers'):
            self.trainers[filename[:-4]] = Image(filename='battle/trainers/' + filename)

        for filename in os.listdir('battle/emblems'):
            self.emblems[filename[:-4]] = Image(filename='battle/emblems/' + filename)

        for filename in os.listdir('battle/markers'):
            self.markers[filename[:-4]] = Image(filename='battle/markers/' + filename)

        for filename in os.listdir('battle/numbers'):
            self.numbers[filename[:-4]] = Image(filename='battle/numbers/' + filename)

        #self.marker = Image(filename='battle/test_marker.png')


    def generate_battle_random(self, saveAs, spacing=100, names=None, types=None, count=random.randint(1,5)):

        if names is None:
            pokemon = random.sample(list(self.pokemon.values()), count)
        else:
            pokemon = [self.pokemon[name] for name in names]

        bgColor = random.choice([NATURE, FIRE, DISCORD, PSYCHIC, EARTH, ELECTRIC, DRAGON])

        if bgColor == DISCORD:
            emblem = self.emblems['emblem_black_1']
        elif bgColor in [DRAGON, NORMAL]:
            emblem = self.emblems['emblem_white']
        else:
            emblem = self.emblems['emblem_black_2']


        bg = Image(width=400, height=300, background=Color(bgColor))
        with Drawing() as draw:
            draw.composite(operator='over', image=emblem, left=77, top=41, width=emblem.width, height=emblem.height)
            draw(bg)

        trainer = random.choice(list(self.trainers.values()))
        with Drawing() as draw:
            draw.composite(operator='over', image=trainer, left=312, top=211, width=trainer.width, height=trainer.height)
            draw(bg)


        ballTypes = list(self.balls.values())
        balls = [self.balls['poke'] if random.random() < 0.8 else random.choice(ballTypes) for i, _ in enumerate(pokemon)]

        oy = 260
        for i, b in enumerate(balls):
            with Drawing() as draw:
                draw.composite(operator='over', image=b, left=290 - i * 22, top=oy, width=b.width, height=b.height)
                draw(bg)

        scale = [175, 175, 150, 125, 125][len(pokemon) - 1]
        centers = []
        markerOrigins = []
        for i, pkmn in enumerate(pokemon):
            if len(pokemon) == 1:
                width = scale + random.randint(-20, 20)
                height = width
                ox = 400 / 2 - width / 2
                oy = 300 / 2 - height / 2
            else:
                attempts = 0
                while True:
                    ox = random.randint(-20, 400 - scale - 20)
                    oy = random.randint(0, 300 - scale - 20)
                    width = scale + random.randint(-20, 20)
                    height = width

                    cx, cy = ox + width / 2, oy + height / 2
                    spaced = True
                    for c in centers:
                        cx2, cy2 = c
                        if math.hypot(cx2 - cx, cy2 - cy) < spacing:
                            spaced = False
                            break
                    if spaced:
                        centers.append((cx, cy))
                        break

                    attempts += 1
                    if attempts == 100000:
                        return False

            markerOrigins.append((ox + (scale - 40) - (scale - width) / 2, oy))
            with Drawing() as draw:
                draw.composite(operator='over', image=pkmn, left=ox, top=oy, width=width, height=height)
                draw(bg)

        for i, pkmn in enumerate(pokemon):
            marker = random.choice(list(self.markers.values())).clone()
            number = self.numbers[str(i+1)]
            with Drawing() as draw:
                draw.composite(operator='over', image=number, left=0, top=0, width=number.width, height=number.height)
                draw(marker)

            ox, oy = markerOrigins[i]
            with Drawing() as draw:
                draw.composite(operator='over', image=marker, left=ox, top=oy, width=marker.width, height=marker.height)
                draw(bg)

        #display(bg)
        bg.save(filename=saveAs)


    def generate_battle_variant(self, saveAs, pool, trainers, colors=None, emblem=None, normalBalls=False, spacing=100, count=random.randint(1,5), unique=True, ordered=False, balls=None):

        pokemon = []
        markers = []
        scales = []
        i = 0
        while len(pokemon) < count:
            if ordered:
                p = pool[i]
                i += 1
            else:
                p = random.choice(pool)
                if unique and self.pokemon[p[0]] in pokemon:
                    continue
            pokemon.append(self.pokemon[p[0]])
            t = random.choice(p[1]) if type(p[1]) == list else p[1]
            markers.append(self.markers[f'marker_{t}'])
            try:
                scales.append(p[2])
            except IndexError:
                scales.append(None)

        if colors is None:
            bgColor = random.choice([NATURE, FIRE, DISCORD, PSYCHIC, EARTH, ELECTRIC, DRAGON])
        else:
            bgColor = random.choice(colors)

        if emblem:
            emblem = self.emblems[emblem]
        else:
            if bgColor == DISCORD:
                emblem = self.emblems['emblem_black_1']
            elif bgColor in [DRAGON, NORMAL]:
                emblem = self.emblems['emblem_white']
            else:
                emblem = self.emblems['emblem_black_2']

        bg = Image(width=400, height=300, background=Color(bgColor))
        with Drawing() as draw:
            draw.composite(operator='over', image=emblem, left=77, top=41, width=emblem.width, height=emblem.height)
            draw(bg)

        trainer = self.trainers[random.choice(trainers)]
        with Drawing() as draw:
            draw.composite(operator='over', image=trainer, left=312, top=211, width=trainer.width, height=trainer.height)
            draw(bg)

        if balls:
            balls = [self.balls[ball] for ball in balls]
        else:
            ballTypes = list(self.balls.values())
            balls = [self.balls['poke'] if normalBalls or random.random() < 0.8 else random.choice(ballTypes) for i, _ in enumerate(pokemon)]

        oy = 260
        for i, b in enumerate(balls):
            with Drawing() as draw:
                draw.composite(operator='over', image=b, left=290 - i * 22, top=oy, width=b.width, height=b.height)
                draw(bg)

        scale = [175, 175, 150, 125, 125][len(pokemon) - 1]
        centers = []
        markerOrigins = []
        for i, pkmn in enumerate(pokemon):
            if scales[i]:
                try:
                    width = scale * random.uniform(scales[i][0], scales[i][1])
                except TypeError:
                    width = scale * scales[i]
            else:
                width = scale + random.randint(-20, 20)
            height = width

            if len(pokemon) == 1:
                ox = 400 / 2 - width / 2
                oy = 300 / 2 - height / 2
            else:
                attempts = 0
                while True:
                    ox = random.randint(-20, 400 - scale - 20)
                    oy = random.randint(0, 300 - scale - 20)

                    cx, cy = ox + width / 2, oy + height / 2
                    spaced = True
                    for c in centers:
                        cx2, cy2 = c
                        if math.hypot(cx2 - cx, cy2 - cy) < spacing:
                            spaced = False
                            break
                    if spaced:
                        centers.append((cx, cy))
                        break

                    attempts += 1
                    if attempts == 100000:
                        return False

            markerOrigins.append((ox + (scale - 40) - (scale - width) / 2, oy))
            with Drawing() as draw:
                draw.composite(operator='over', image=pkmn, left=ox, top=oy, width=width, height=height)
                draw(bg)

        for i, pkmn in enumerate(pokemon):
            marker = markers[i].clone()
            number = self.numbers[str(i+1)]
            with Drawing() as draw:
                draw.composite(operator='over', image=number, left=0, top=0, width=number.width, height=number.height)
                draw(marker)

            ox, oy = markerOrigins[i]
            if ox + marker.width > 400:
                ox = 390 - marker.width
            if ox < 0:
                ox = 10
            with Drawing() as draw:
                draw.composite(operator='over', image=marker, left=ox, top=oy, width=marker.width, height=marker.height)
                draw(bg)

        #display(bg)
        bg.colorspace = 'srgb'
        bg.format = 'png32 '
        bg.save(filename=saveAs)



tg = TrainerGenerator()
tg.load_all_images()

# for i in range(100):
#     tg.generate_battle('battle/out/{}.png'.format(i), spacing=100)

# for i in range(100):
#     tg.generate_battle('battle/out/{}.png'.format(100+i), spacing=125)



pool = (
    ('alolan meowth', 'dark'),
    #('alolan persian', 'dark'),
    ('alolan rattata', 'dark'),
    #('alolan raticate', 'dark'),
    #('pancham', ['dark', 'earth']),
    #('lycanroc (midnight)', 'dark'),
    #('lycanroc (dusk)', 'fire'),
    #('houndoom (dark)', ['fire', 'dark']),
    #('houndour (dark)', ['fire', 'dark']),
    #('murkrow', 'dark'),
    #('gastly', 'psychic'),
    #('gloom', 'nature'),
)

# pool = (
#     ('plusle', 'electric'),
#     ('minun', 'electric'),
#     ('alolan raichu', 'psychic'),
# )

# pool = (
#     ('lairon', 'earth', 1.2),
#     ('larvitar (earth)', 'dark', 1),
#     ('beldum (psychic)', 'psychic', 1),
#     ('metang (earth)', 'earth', 1.1),
# )

# pool = (
#     ('aron', 'earth'),
#     ('alolan sandshrew', 'ice', 1),
#     ('sandslash', 'earth', 1.2),
#     ('komala', 'normal')
# )

# pool = (
#     ('mega steelix', 'earth', [1.2, 1.8]),
# )

pool = (
    ('nidoqueen', 'nature', [1.1, 1.3]),
    ('salazzle (nature)', 'nature'),
    ('gastly', 'psychic', [0.7, 0.9]),
)

trainers = (
    #'rocket_grunt',
    # 'Spr_HGSS_Archer',
    # 'Spr_HGSS_Ariana',
    # 'Spr_HGSS_Rocket_Grunt_M',
    # 'Spr_HGSS_Rocket_Grunt_F',
    # 'Spr_HGSS_Proton',
    # 'Spr_HGSS_Petrel',
    # 'Spr_Pt_Marley'
)

trainers = ['roxie']

colors = [DISCORD]#, PSYCHIC, EARTH, NATURE]
#         bgColor = random.choice([NATURE, FIRE, DISCORD, PSYCHIC, EARTH, ELECTRIC, DRAGON])


print('start')
for i in range(500):
    #tg.generate_battle_variant(f'battle/out/rocket_{i}.png', pool, trainers, colors, spacing=125, count=random.randint(1, 1), unique=True)
    #tg.generate_battle_variant(f'battle/out/surge_{i}.png', pool, trainers, colors, spacing=125, count=random.randint(2, 3), unique=True)

    # tg.generate_battle_variant(f'battle/out/oak_{i}.png', pool, trainers, colors, emblem='emblem_peach', normalBalls=False,
    #     spacing=125, count=3, unique=True, ordered=False)

    tg.generate_battle_variant(f'battle/out/roxie_{i}.png', pool, trainers, colors, normalBalls=False,
        spacing=125, count=len(pool), ordered=True)


    print(f'wrote {i}')

print('Finished')



#
#
# def merge_with_type_bg(inPath, outPath):
#     for dir in os.listdir(inPath):
#         typeBackground = Image(filename=inPath + dir + '/type.png')
#         if not os.path.exists(outPath + dir):
#             os.makedirs(outPath + dir)
#         for filename in os.listdir(inPath + dir):
#             if filename in ['type.png', 'evolve.png']:
#                 continue
#             bg = typeBackground.clone()
#             badge = Image(filename=inPath + dir + '/' + filename)
#             print(outPath + dir + '/' + filename)
#             with Drawing() as draw:
#                 draw.composite(operator='over', image=badge, left=0, top=0, width=300, height=300)
#                 draw(bg)
#
#             bg.save(filename=outPath + dir + '/' + filename)
#
# def merge_with_evolve_icon(inPath, outPath):
#     for dir in os.listdir(inPath):
#         evo1 = Image(filename=inPath + dir + '/evolve 1.png')
#         evo2 = Image(filename=inPath + dir + '/evolve 2.png')
#         evo3 = Image(filename=inPath + dir + '/evolve 3.png')
#         evos = [evo1, evo2, evo3]
#         if not os.path.exists(outPath + dir):
#             os.makedirs(outPath + dir)
#         for filename in os.listdir(inPath + dir):
#             if filename in ['type.png', 'evolve 1.png', 'evolve 2.png', 'evolve 3.png']:
#                 continue
#
#             print(outPath + dir + '/' + filename)
#
#             badge = Image(filename=inPath + dir + '/' + filename)
#             for i, evo in enumerate(evos):
#                 b = badge.clone()
#                 with Drawing() as draw:
#                     draw.composite(operator='over', image=evo, left=98, top=113, width=evo.width, height=evo.height)
#                     draw(b)
#                 b.save(filename='{}{}/{}_{}.png'.format(outPath, dir, filename[:-4], i+1))

# merge_with_type_bg('separate 300/', 'merged 300/')
# merge_with_evolve_icon('merged 170/', 'evolve 170/')












# with Color('red') as bg:
#     with Image(width=200, height=100, background=bg) as img:
#         img.save(filename='merged/test/200x100-red.png')

# inPath = "separate 300/"
# outPath = "merged 300/"
# for dir in os.listdir(inPath):
#     typeBackground = Image(filename=inPath + dir + '/type.png')
#     for file in os.listdir(inPath + dir):
#         if file in ['type.png', 'evolve.png']:
#             continue
#         bg = typeBackground.clone()
#         badge = Image(filename=inPath + dir + '/' + file)
#         cleanName = re.sub('[0-9]', '', file.lower().replace('copy', ''))
#         print(file, clean_name(file))
    #     with Drawing() as draw:
    #         draw.composite(operator='over', image=badge, left=0, top=0, width=300, height=300)
    #         draw(bg)
    #         bg.save(filename=outPath + dir + '/' + file.lower().replace(""))
    #     break
    # break


# wizard = Image(filename='wizard:')
# rose = Image(filename='rose:')

#   w = wizard.clone()
#   r = rose.clone()
#   with Drawing() as draw:
#     draw.composite(operator='over', image=typeIcon)
#     draw(w)
#     display(w)
#     # w = img

# img.format = 'jpeg'
# img.save(filename='pikachu.jpg')

# img.resize(50, 60)


# with Image(filename='pikachu.png') as img:
#     img.format = 'jpeg'
#     img.save(filename='pikachu.jpg')
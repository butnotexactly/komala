import os
import re
import time
from datetime import date

from wand.image import Image
from wand.drawing import Drawing
from wand.display import display
from wand.color import Color

def clean_name(name):
    name = re.sub('[0-9]', '', name.lower().replace('copy', '').replace('-', '_').replace('.png', ' '))
    name = name.strip('_ ')
    name = name.replace('_', ' ')
    name = name.replace('  ', ' ')
    if name.endswith(' (alola)'):
        name = 'alolan ' + name[:-(len(' (alola)'))]
    if name.endswith(' (alolan)'):
        name = 'alolan ' + name[:-(len(' (alolan)'))]
    return name + '.png'

def clean_all_names(inPath):
    for dir in os.listdir(inPath):
        for filename in os.listdir(inPath + dir):
            if filename in ['type.png', 'evolve.png']:
                continue
            clean = clean_name(filename)
            if filename != clean:
                os.rename(inPath + dir + '/' + filename, inPath + dir + '/' + clean)
                #print(filename, clean_name(filename))

def merge_with_type_bg(inPath, outPath):
    for dir in os.listdir(inPath):
        typeBackground = Image(filename=inPath + dir + '/type.png')
        if not os.path.exists(outPath + dir):
            os.makedirs(outPath + dir)
        for filename in os.listdir(inPath + dir):
            if filename in ['type.png', 'evolve 1.png', 'evolve 2.png', 'evolve 3.png']:
                continue

            t = os.path.getmtime(inPath + dir + '/' + filename)
            dt = date.fromtimestamp(t)
            today = date.today()
            if not today == dt:
                continue

            bg = typeBackground.clone()
            badge = Image(filename=inPath + dir + '/' + filename)
            print(outPath + dir + '/' + filename)
            with Drawing() as draw:
                draw.composite(operator='over', image=badge, left=0, top=0, width=300, height=300)
                draw(bg)

            bg.save(filename=outPath + dir + '/' + filename)

def merge_with_evolve_icon(inPath, outPath):
    for dir in os.listdir(inPath):
        evo1 = Image(filename=inPath + dir + '/evolve 1.png')
        evo2 = Image(filename=inPath + dir + '/evolve 2.png')
        evo3 = Image(filename=inPath + dir + '/evolve 3.png')
        evos = [evo1, evo2, evo3]
        if not os.path.exists(outPath + dir):
            os.makedirs(outPath + dir)
        for filename in os.listdir(inPath + dir):
            if filename in ['type.png', 'evolve 1.png', 'evolve 2.png', 'evolve 3.png']:
                continue

            t = os.path.getmtime(inPath + dir + '/' + filename)
            dt = date.fromtimestamp(t)
            today = date.today()
            if not today == dt:
                continue

            print(outPath + dir + '/' + filename)

            badge = Image(filename=inPath + dir + '/' + filename)
            for i, evo in enumerate(evos):
                b = badge.clone()
                with Drawing() as draw:
                    draw.composite(operator='over', image=evo, left=98, top=113, width=evo.width, height=evo.height)
                    draw(b)
                b.save(filename='{}{}/{}_{}.png'.format(outPath, dir, filename[:-4], i+1))

#merge_with_type_bg('separate 300/', 'merged 300/')
merge_with_evolve_icon('merged 170/', 'evolve 170/')












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
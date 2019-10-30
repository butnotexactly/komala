import copy
import pprint


def fmt(text, case=0, prefix = None):
    if not text:
        return "None"

    s = "" if not prefix else prefix + "_"
    if not case:
        return s + text.replace(" ", "_").replace("'", "")
    if case > 0:
        return s + text.upper().replace(" ", "_").replace("'", "")
    return s + text.lower().replace(" ", "_").replace("'", "")

def make_area(prefix, name, image):
    return f"""
    # {name}
    async def {prefix.lower()}_{fmt(name, -1)}_ex(handler, arg):
        pass

    ow[{fmt(name, 1, pre)}] = {{
        'name': '{name}',
        'desc': '',
        'img': '{image}',
        'ex': {prefix.lower()}_{fmt(name, -1)}_ex,
        #'actions': [''],
    }}"""

names = [["Outskirts","Pokémon Institute","Residences"],["West Exit","City Fountain","East Exit"],["Side Street","Market Street","Finance District"],["Backalley","South Exit","???'s House"]]
images = [["https://i.imgur.com/d4GFqf4.png","https://i.imgur.com/7uExDn3.png","https://i.imgur.com/r7Tx9wB.png"],["https://i.imgur.com/CEyaGQh.png","https://i.imgur.com/fAnatKp.png","https://i.imgur.com/htK7JKr.png"],["https://i.imgur.com/3MSAVaJ.png","https://i.imgur.com/rbeXeBd.png","https://i.imgur.com/RVJuevZ.png"],["https://i.imgur.com/MvNpcAn.png","https://i.imgur.com/MrPG6lR.png","https://i.imgur.com/vpwO1HM.png"]]
id = 62
pre = "JA"

keys = []
rest = []
map = copy.copy(names)
for row, _ in enumerate(names):
    for col, name in enumerate(_):
        if not name:
            continue
        # print(col, row, name)
        # print(images[row][col])
        # print(fmt(name, 1, pre))
        keys.append(fmt(name, 1, pre))
        map[row][col] = fmt(name, 1, pre)
        rest.append(make_area(pre, name, images[row][col]))


map = str(map).replace('], ', '],\n\t\t\t').replace("'", "")
keys = '\n'.join(f'{key} = {n+id*100}' for n, key in enumerate(keys))
rest = '\n'.join(rest)

output = f"""from common import *

ID = {id}

{keys}

def setup(areas, ow):
    areas[ID] = {{
        'name': '',
        'emoji': '',
        'dialog': '',
        'map': {map}
    }}

{rest}"""

f = open('map_out.py', 'w+')
f.write(output)
f.close()

print(output)




#PREFIX = '{pre}'

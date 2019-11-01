import math

ns = [1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 13, 181, 182, 41, 42, 43, 44, 15, 16, 17, 60, 61, 62, 63, 194, 195, 197, 198, 26, 27, 106, 107, 92, 93, 94, 45, 46, 47, 48, 30, 110, 111, 80, 81, 82, 108, 109, 69, 70, 71, 83, 84, 85, 228, 209, 210, 64, 65, 66, 54, 55, 56, 57, 190, 191, 170, 171, 86, 87, 28, 29, 58, 59, 79, 37, 38, 39, 40, 74, 75, 76, 67, 68, 167, 168, 123, 124, 114, 115, 112, 113, 119, 105, 205, 206, 162, 163, 164, 165, 192, 193, 20, 21, 23, 24, 223, 129, 133, 130, 134, 137, 138, 140, 141, 143, 144, 146, 147, 183, 184, 150, 151, 154, 155, 220, 221, 202, 203, 88, 89, 90, 91, 118, 120, 122, 121, 217, 218, 125, 126, 156, 157, 160, 161, 187, 176, 177, 116, 117, 99, 102, 100, 103, 101, 104, 174, 175, 214, 179, 180, 78, 127, 128, 49, 50, 51, 52, 53, 166, 227, 35, 36, 188, 213, 25, 207, 208, 211, 212, 199, 200, 189, 226, 224, 225, 201, 215, 216, 204, 169, 95, 96, 97, 98, 178, 148, 149, 222, 185, 186, 172, 173, 31, 32, 33, 34, 14, 219, 72, 73]

size = 100
count = len(ns)
a = math.ceil(math.sqrt(count))
b = math.ceil(count/a)
columns  = max(a, b)
rows     = min(a, b)

css = []
nodes = []

for i, n in enumerate(ns):
    x = -(i % columns) * size
    y = -(i // columns) * size
    css.append(f'.badge-{n} {{ background-position: {x}px {y}px; }}')
    nodes.append(f'<div id="bage_{n}" class="badge badge-{n}" data-no={n}></div>')

print('\n'.join(css))
#print('\n'.join(nodes))


'''

<div class="badge badge-1" data-no=1></div>


'''
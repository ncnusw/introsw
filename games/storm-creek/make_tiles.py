"""Draws extra.png (creek, bridge, tea rows) in the Kenney Tiny Town palette. Run once: python3 make_tiles.py
Original pixel art for this site, released under CC0 like the Kenney tiles."""
from PIL import Image
import pathlib

OUT = pathlib.Path(__file__).with_name('extra.png')
G, G2, GL = (132, 198, 105), (101, 165, 86), (139, 216, 125)     # grass
INK = (63, 38, 49)                                               # outline
W1, W2, WL, WD = (88, 155, 214), (68, 128, 196), (170, 220, 245), (52, 102, 168)   # water
WO, WOD, WOL = (189, 108, 74), (118, 59, 54), (234, 165, 108)    # wood
TEA, TEAD, TEAL = (71, 159, 74), (44, 112, 60), (120, 200, 96)   # tea
MUD, MUDD = (150, 110, 80), (110, 80, 62)

img = Image.new('RGBA', (192, 16), (0, 0, 0, 0))
px = img.load()

def tile(i, f):
    for y in range(16):
        for x in range(16):
            c = f(x, y)
            if c: px[i * 16 + x, y] = c + (255,)

def water(x, y, ph=0):
    if (y in (4, 11)) and ((x + ph) % 8) in (1, 2, 3): return WL
    if (y in (5, 12)) and ((x + ph) % 8) in (0, 4): return W2
    if (x * 7 + y * 3 + ph) % 23 == 0: return WD
    return W1

tile(0, lambda x, y: water(x, y, 0))
tile(1, lambda x, y: water(x, y, 4))
# 2: water with grass bank on top
tile(2, lambda x, y: (G if y < 3 else (G2 if y == 3 and x % 3 else (INK if y == 4 else water(x, y)))))
# 3: water with grass bank below
tile(3, lambda x, y: (G if y > 12 else (G2 if y == 12 and x % 3 else (INK if y == 11 else water(x, y)))))

# 4: bridge planks (cross north-south): rails at the sides, boards across
def bridge(x, y):
    if x in (0, 15): return INK
    if x in (1, 14): return WOD
    if y % 4 == 3: return WOD
    if y % 4 == 0 and x % 5 == 2: return WOL
    return WO
tile(4, bridge)

# 5: tea row (solid bush on grass)
def tea(x, y):
    cx, r = 7.5, 6.6
    d = ((x - cx) ** 2 + ((y - 8) * 1.15) ** 2) ** .5
    if d > r + .9: return G if (x + y) % 9 else G2
    if d > r: return INK
    if y < 6 and (x + y) % 3 == 0: return TEAL
    if (x * 3 + y) % 7 == 0: return TEAD
    return TEA
tile(5, tea)

# 6: muddy, flooded path
tile(6, lambda x, y: (W1 if (x * 5 + y * 7) % 11 == 0 else (MUDD if (x + 2 * y) % 6 == 0 else MUD)))

# 7: water edge left (grass on left)
tile(7, lambda x, y: (G if x < 3 else (INK if x == 3 else water(x, y))))
# 8: water edge right
tile(8, lambda x, y: (G if x > 12 else (INK if x == 12 else water(x, y))))

img.save(OUT)
print('wrote', OUT)

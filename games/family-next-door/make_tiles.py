"""Draws extra.png (streetlights, trash pile, garden bed, blackboard, flowers) in the Kenney Tiny Town palette.
Run once: python3 make_tiles.py. Original pixel art for this site, released under CC0 like the Kenney tiles."""
from PIL import Image
import pathlib

OUT = pathlib.Path(__file__).with_name('extra.png')
INK = (63, 38, 49)
G, G2 = (132, 198, 105), (101, 165, 86)
METAL, METALD, METALL = (120, 128, 150), (78, 84, 104), (170, 178, 196)
OFF, OFFD = (70, 76, 96), (50, 54, 70)
LIT, LITL, GLOW = (255, 209, 102), (255, 240, 180), (255, 226, 140)
BAG, BAGD, BAGL = (58, 62, 74), (36, 38, 48), (96, 102, 118)
SOIL, SOILD = (140, 96, 66), (104, 70, 50)
WO, WOD = (189, 108, 74), (118, 59, 54)
SPR, SPRD = (120, 200, 96), (71, 159, 74)

img = Image.new('RGBA', (192, 16), (0, 0, 0, 0))
px = img.load()

def tile(i, f):
    for y in range(16):
        for x in range(16):
            c = f(x, y)
            if c: px[i * 16 + x, y] = c + (255,)

def lamp(on):
    def f(x, y):
        # pole
        if 7 <= x <= 8 and 5 <= y <= 13: return METALL if x == 7 else METAL
        if (x in (6, 9)) and 5 <= y <= 13: return INK
        if 13 <= y <= 15 and 4 <= x <= 11:
            return INK if y == 15 or x in (4, 11) else METALD
        # head
        if y == 0 and 4 <= x <= 11: return INK
        if 1 <= y <= 2 and 3 <= x <= 12: return INK if x in (3, 12) else METALD
        if y == 3 and 4 <= x <= 11: return INK if x in (4, 11) else (LITL if on and 6 <= x <= 9 else (LIT if on else OFF))
        if y == 4 and 5 <= x <= 10: return INK if x in (5, 10) else (LIT if on else OFFD)
        if on and y in (5, 6) and 2 <= x <= 13 and (x + y) % 3 == 0 and not 6 <= x <= 9: return GLOW
        if on and y == 1 and x in (1, 14): return GLOW
        return None
    return f
tile(0, lamp(False))
tile(1, lamp(True))

def trash(x, y):
    blobs = [(5, 10, 4.6), (10.5, 11, 4.2), (8, 6.5, 3.8)]
    inside = [((x - cx) ** 2 + (y - cy) ** 2) ** .5 - r for cx, cy, r in blobs]
    d = min(inside)
    if y > 15: return None
    if d > .9: 
        if (x, y) in ((2, 3), (13, 2), (12, 4)): return INK   # flies
        return None
    if d > 0: return INK
    if (x * 5 + y * 3) % 13 == 0: return BAGL
    if (x == 8 and y in (3, 4)) or (x in (7, 9) and y == 3): return INK   # knot
    if (x + y) % 9 == 0: return BAGD
    if (x, y) in ((4, 12), (5, 12), (12, 9), (13, 9)): return (224, 110, 90)
    if (x, y) in ((9, 13), (10, 13)): return (240, 220, 120)
    return BAG
tile(2, trash)

def garden(x, y):
    if y < 3 or y > 14: return None
    if y in (3, 14) or x in (0, 15): return INK
    if y in (4, 13) or x in (1, 14): return WO if (x + y) % 4 else WOD
    if (x in (4, 8, 12)) and y in (6, 9, 11) : return SPRD
    if (x in (3, 5, 7, 9, 11, 13)) and y in (5, 8, 10): return SPR
    return SOILD if (x * 3 + y) % 7 == 0 else SOIL
tile(3, garden)

def flowers(x, y):
    pts = {(3, 4): (255, 120, 140), (11, 3): (255, 209, 102), (7, 9): (190, 140, 255), (12, 11): (255, 120, 140), (4, 12): (255, 209, 102)}
    for (fx, fy), c in pts.items():
        if (x, y) == (fx, fy): return c
        if abs(x - fx) + abs(y - fy) == 1: return (255, 250, 240) if y != fy + 1 else SPRD
    return None
tile(4, flowers)

# 9-11: blackboard (left, middle, right) hung on a wall
BB, BBL, CH, FR = (46, 84, 66), (60, 104, 82), (225, 232, 220), (140, 92, 58)
def board(part):
    def f(x, y):
        if y < 2 or y > 13: return None
        if y in (2, 13): return FR
        if part == 0 and x < 2: return FR
        if part == 2 and x > 13: return FR
        if y == 12 and x % 5 == 1: return CH
        if part == 1 and y in (5, 8) and 2 < x < 13 and (x * 3 + y) % 4: return CH
        if part == 0 and y == 6 and 4 < x < 13: return CH
        return BBL if (x + y) % 7 == 0 else BB
    return f
tile(9, board(0)); tile(10, board(1)); tile(11, board(2))

img.save(OUT)
print('wrote', OUT)

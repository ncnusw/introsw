"""Builds data.js for 青溪颱風夜 Storm Over Clear Creek. Run from this folder: python3 build_data.py
Maps are drawn here in code so every row has the right length; the story script is the SCRIPT string below.
Edit the script, then run this again. It also checks that every door and every person can be reached."""
import json, pathlib, collections

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / 'data.js'

# ---------------------------------------------------------------- tiles
SOLID_G = set('~`^vW V')   # ground chars that block (V and W are walls)
SOLID_O = set('TUOabcdehijlmnprpABCDEFGYLMNRPS()_|t3459w0z1')   # obj chars that block ('2' stools do not)

def blank(w, h, ch='.'):
    return [[ch] * w for _ in range(h)]

def stamp(grid, x, y, rows):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != ' ':
                grid[y + j][x + i] = c

GRAY6 = ['abbdbc', 'ehhjhi', 'lnmnnr', 'lmmpmr']
RED6 = ['ABDBBC', 'EFYFFG', 'LNMNNR', 'LMMPMR']
RED11 = ['ABBBBDBBBBC', 'EFFFFYFFFFG', 'LNMNMNMNMNR', 'LNMNMPMNMNR']

# ---------------------------------------------------------------- village 36 x 26
W, H = 36, 26
g = blank(W, H, '.')
o = blank(W, H, '.')
for y in range(H):
    for x in range(W):
        if (x * 7 + y * 13) % 17 == 0: g[y][x] = ','
        elif (x * 5 + y * 11) % 41 == 0: g[y][x] = '*'
# border trees
for x in range(W): o[0][x] = 'T'; o[H - 1][x] = 'T'
for y in range(H): o[y][0] = 'T'; o[y][W - 1] = 'T'
# north houses (rows 1-4)
stamp(o, 2, 1, GRAY6)     # Lin, door (5,4)
stamp(o, 9, 1, RED6)      # Wu, door (12,4)
stamp(o, 16, 1, RED11)    # school / activity center, door (21,4)
stamp(o, 28, 1, GRAY6)    # tea co-op, door (31,4)
for x in (1, 8, 15, 27, 34): o[1][x] = 'U' if x % 2 else 'T'
o[5][8] = 'O'; o[5][15] = '6'; o[5][27] = '6'; o[5][1] = 'O'
# main road rows 6-7
for y in (6, 7):
    for x in range(1, 35): g[y][x] = '='
# west: path down to the tunnel, trees on both sides, rock face with the tunnel door
for y in range(8, 15):
    for x in range(1, 8): o[y][x] = 'T' if (x + y) % 3 else 'U'
for y in range(8, 12):
    o[y][4] = '.'; g[y][4] = '='
for x in range(2, 7): o[12][x] = 'w'
o[12][4] = 'z'
# tea field
for y in (9, 11, 13):
    for x in range(9, 16): o[y][x] = 't'
# closed grocery
stamp(o, 16, 9, GRAY6)    # door (19,12)
# path from road to bridge (x 23-24)
for y in range(8, 15):
    g[y][23] = '='; g[y][24] = '='
# east: riverside trees and a log bench
for (x, y) in [(27, 9), (31, 9), (33, 11), (26, 13), (30, 13), (34, 9)]: o[y][x] = 'T' if (x + y) % 2 else 'U'
o[11][28] = 'g'; o[11][29] = 'g'
# creek rows 15-17, bridge at x 23-24
for x in range(1, 35):
    g[15][x] = '^'; g[16][x] = '~' if x % 3 else '`'; g[17][x] = 'v'
for y in (15, 16, 17):
    g[y][23] = 'b'; g[y][24] = 'b'
for y in (15, 16, 17): o[y][0] = 'T'; o[y][W - 1] = 'T'
# south side
stamp(o, 26, 18, GRAY6)   # Grandma Chen, door (29,21)
for y in (18, 19, 20, 21):
    g[y][23] = '='; g[y][24] = '='
for x in range(4, 31): g[22][x] = '='
for y in (20, 21): g[y][4] = '='
for x in range(1, 8): o[18][x] = 'T'
for x in range(2, 7): o[19][x] = 'w'
o[19][4] = 'z'
for (x, y) in [(10, 19), (14, 20), (17, 19), (33, 19), (32, 23), (12, 24), (20, 24), (8, 23), (2, 22), (2, 24), (6, 24), (34, 21)]:
    o[y][x] = 'T' if (x + y) % 2 else 'U'
for (x, y) in [(19, 20), (21, 23), (27, 23), (15, 23)]: o[y][x] = 'O'
village = {
    'ground': [''.join(r) for r in g], 'obj': [''.join(r) for r in o],
    'doors': {
        'lin': {'x': 5, 'y': 4, 'to': 'lin', 'tx': 5, 'ty': 6, 'dir': 'up'},
        'wu': {'x': 12, 'y': 4, 'to': 'wu', 'tx': 5, 'ty': 6, 'dir': 'up'},
        'school': {'x': 21, 'y': 4, 'to': 'school', 'tx': 7, 'ty': 8, 'dir': 'up'},
        'coop': {'x': 31, 'y': 4, 'to': 'coop', 'tx': 5, 'ty': 6, 'dir': 'up'},
        'grocery': {'x': 19, 'y': 12, 'locked': True, 'msg': '雜貨店已經關門了。玻璃門上貼著：「感謝大家四十年來的照顧」。'},
        'chen': {'x': 29, 'y': 21, 'to': 'chen', 'tx': 5, 'ty': 6, 'dir': 'up'},
        'tunnelN': {'x': 4, 'y': 12, 'to': 'tunnel', 'tx': 2, 'ty': 1, 'dir': 'down'},
        'tunnelS': {'x': 4, 'y': 19, 'to': 'tunnel', 'tx': 15, 'ty': 7, 'dir': 'up'},
    }}

# ---------------------------------------------------------------- tunnel 18 x 9
# Fixed maze (same every time, so students learn it across tries). 13 x 9 cells -> 27 x 19 tiles.
import random
MZ_W, MZ_H = 13, 9
_rng = random.Random(20261027)
_tw, _th = MZ_W * 2 + 1, MZ_H * 2 + 1
_t = [['W'] * _tw for _ in range(_th)]
_seen = {(0, 0)}; _stack = [(0, 0)]; _t[1][1] = 'u'
while _stack:
    cx, cy = _stack[-1]
    nb = [(cx + dx, cy + dy, dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
          if 0 <= cx + dx < MZ_W and 0 <= cy + dy < MZ_H and (cx + dx, cy + dy) not in _seen]
    if not nb: _stack.pop(); continue
    nx, ny, dx, dy = _rng.choice(nb)
    _t[cy * 2 + 1 + dy][cx * 2 + 1 + dx] = 'u'; _t[ny * 2 + 1][nx * 2 + 1] = 'u'
    _seen.add((nx, ny)); _stack.append((nx, ny))
# a few extra openings so there is more than one way through
for _ in range(7):
    while True:
        x, y = _rng.randrange(1, _tw - 1), _rng.randrange(1, _th - 1)
        if _t[y][x] == 'W' and ((_t[y][x - 1] == 'u' and _t[y][x + 1] == 'u' and _t[y - 1][x] == 'W' and _t[y + 1][x] == 'W') or
                                (_t[y - 1][x] == 'u' and _t[y + 1][x] == 'u' and _t[y][x - 1] == 'W' and _t[y][x + 1] == 'W')):
            _t[y][x] = 'u'; break
TUN_IN, TUN_OUT = (1, 1), (_tw - 2, _th - 2)
_t[0][1] = '+'; _t[_th - 1][_tw - 2] = '+'
tun_g = [''.join(r) for r in _t]
tun_o = ['.' * _tw for _ in tun_g]
def _bfs(start):
    d = {start: 0}; q = collections.deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if 0 < n[0] < _tw - 1 and 0 < n[1] < _th - 1 and _t[n[1]][n[0]] == 'u' and n not in d: d[n] = d[(x, y)] + 1; q.append(n)
    return d
_din, _dout = _bfs(TUN_IN), _bfs(TUN_OUT)
# the boy waits in a dead end that is a real detour from the shortest route
_dead = [c for c in _din if sum(_t[c[1] + b][c[0] + a] == 'u' for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) == 1 and c not in (TUN_IN, TUN_OUT)]
_direct = _din[TUN_OUT]
KID_POS = max(_dead, key=lambda c: (min(_din[c], _dout[c]), _din[c] + _dout[c]))
MAZE_STEPS = _din[KID_POS] + _dout[KID_POS]
tunnel = {'ground': tun_g, 'obj': tun_o, 'doors': {
    'top': {'x': 1, 'y': 0, 'to': 'village', 'tx': 4, 'ty': 11, 'dir': 'up'},
    'bottom': {'x': TUN_OUT[0], 'y': _th - 1, 'to': 'village', 'tx': 4, 'ty': 20, 'dir': 'down'}}}
village['doors']['tunnelN'].update({'tx': TUN_IN[0], 'ty': TUN_IN[1]})
village['doors']['tunnelS'].update({'tx': TUN_OUT[0], 'ty': TUN_OUT[1]})

# ---------------------------------------------------------------- interiors
def room(w, h, floor, out_to, ox, oy, obj_rows, door_x=None):
    door_x = door_x if door_x is not None else w // 2
    gr = ['W' * w, 'WW' + 'V' + 'W' * (w - 6) + 'V' + 'WW'] + ['W' + floor * (w - 2) + 'W' for _ in range(h - 3)] + ['W' * door_x + '+' + 'W' * (w - door_x - 1)]
    return {'ground': gr, 'obj': obj_rows, 'doors': {'out': {'x': door_x, 'y': h - 1, 'to': out_to, 'tx': ox, 'ty': oy, 'dir': 'down'}}}

school = room(15, 10, 'f', 'village', 21, 5, [
    '...............', '...............', '.3...........4.', '...............', '..1.........1..',
    '.2.2.......2.2.', '...............', '...............', '...............', '...............'], 7)
small = ['...........', '...........', '.0.....3...', '......1....', '......2....', '...........', '...........', '...........']
lin = room(11, 8, 'k', 'village', 5, 5, small)
wu = room(11, 8, 'f', 'village', 12, 5, ['...........', '...........', '.3.....4...', '......1....', '......2....', '...........', '...........', '...........'])
coop = room(11, 8, 'f', 'village', 31, 5, ['...........', '...........', '.4.....4...', '...........', '...........', '.........x.', '...........', '...........'])
chen = room(11, 8, 'k', 'village', 29, 22, small)

# ---------------------------------------------------------------- lecture hall (opening and ending): 20 x 21, 60 seats
CW, CH = 20, 21
cg = ['W' * CW, 'W' * CW] + ['W' + 'f' * (CW - 2) + 'W' for _ in range(CH - 3)] + ['W' * 10 + '+' + 'W' * (CW - 11)]
co = blank(CW, CH)
co[1][6] = '7'
for x in range(7, 13): co[1][x] = '8'
co[1][13] = '9'
for x in (9, 10, 11): co[3][x] = '1'          # teacher's desk
SEAT_COLS = [2, 3, 4, 5, 8, 9, 10, 11, 14, 15, 16, 17]
SEAT_ROWS = [6, 9, 12, 15, 18]
for y in SEAT_ROWS:
    for x in SEAT_COLS: co[y - 1][x] = '1'      # a desk in front of every seat
classroom = {'ground': cg, 'obj': [''.join(r) for r in co], 'doors': {'out': {'x': 10, 'y': CH - 1, 'locked': True, 'msg': '還沒下課，不能離開教室。'}}}
PLAYER_SEAT = (16, 18)
TALKERS = {(15, 18): 'cls_a', (17, 18): 'cls_b', (11, 18): 'cls_c'}
def classroom_puts(with_labels=True):
    looks = ['v2', 'v3', 'v5', 'v6', 'v7', 'v8', 'v9']
    out, n = [], 0
    for y in SEAT_ROWS:
        for x in SEAT_COLS:
            if (x, y) == PLAYER_SEAT: continue
            lab = TALKERS.get((x, y), '-') if with_labels else '-'
            out.append(f"@put s{n} {looks[(n * 3 + y) % len(looks)]} classroom {x} {y} {lab}{' !' if lab != '-' else ''}")
            n += 1
    assert n == 59
    return '\n'.join(out)

MAPS = {'village': village, 'tunnel': tunnel, 'school': school, 'lin': lin, 'wu': wu, 'coop': coop, 'chen': chen, 'classroom': classroom}

# ---------------------------------------------------------------- checks
def walkable(m, x, y, doors_ok=True):
    gr, ob = m['ground'], m['obj']
    if not (0 <= y < len(gr) and 0 <= x < len(gr[0])): return False
    if gr[y][x] in SOLID_G: return False
    if ob[y][x] in SOLID_O: return False
    return True

def reach(m, sx, sy):
    seen = {(sx, sy)}; q = collections.deque([(sx, sy)])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and walkable(m, *n): seen.add(n); q.append(n)
    return seen

for mid, m in MAPS.items():
    w = len(m['ground'][0])
    assert all(len(r) == w for r in m['ground'] + m['obj']), mid
    assert len(m['ground']) == len(m['obj']), mid

# people/things placed in the script must stand on walkable tiles
PLACES = {}

# ---------------------------------------------------------------- game data (JS)
CHARS = ['an', 'lin', 'v2', 'v3', 'mei', 'v5', 'v6', 'v7', 'v8', 'v9', 'chen', 'hao', 'wu', 'kid', 'me', 'li', 'chief']

LEGEND = {
    'ground': {
        '.': ['town', 0, 0], ',': ['town', 1, 0], '*': ['town', 2, 0], '=': ['town', 40, 0], 'o': ['town', 43, 0],
        '~': ['extra', 0, 1], '`': ['extra', 1, 1], '^': ['extra', 2, 1], 'v': ['extra', 3, 1], 'b': ['extra', 4, 0],
        'f': ['dungeon', 48, 0], 'k': ['dungeon', 0, 0], 'u': ['dungeon', 1, 0],
        'W': ['dungeon', 40, 1], 'V': ['dungeon', 28, 1], '+': ['dungeon', 42, 0]},
    'obj': {
        'T': ['town', 16, 1], 'U': ['town', 15, 1], 'O': ['town', 5, 1], '6': ['town', 94, 1],
        'A': ['town', 52, 1], 'B': ['town', 53, 1], 'C': ['town', 54, 1], 'D': ['town', 55, 1], 'E': ['town', 64, 1], 'F': ['town', 65, 1],
        'G': ['town', 66, 1], 'Y': ['town', 67, 1], 'L': ['town', 72, 1], 'M': ['town', 73, 1], 'R': ['town', 75, 1], 'N': ['town', 84, 1], 'P': ['town', 85, 1],
        'a': ['town', 48, 1], 'b': ['town', 49, 1], 'c': ['town', 50, 1], 'd': ['town', 51, 1], 'e': ['town', 60, 1], 'h': ['town', 61, 1],
        'i': ['town', 62, 1], 'j': ['town', 63, 1], 'l': ['town', 76, 1], 'm': ['town', 77, 1], 'r': ['town', 79, 1], 'n': ['town', 88, 1], 'p': ['town', 89, 1],
        'S': ['town', 83, 1], 'g': ['town', 106, 1], 'x': ['town', 130, 1], 't': ['extra', 5, 1],
        'w': ['dungeon', 40, 1], 'z': ['dungeon', 33, 1], '7': ['extra', 9, 1], '8': ['extra', 10, 1], '9': ['extra', 11, 1],
        '0': ['dungeon', 67, 1], '1': ['dungeon', 72, 1], '2': ['dungeon', 73, 0], '3': ['dungeon', 63, 1], '4': ['dungeon', 75, 1]}}
# keep the checker in step with the legend
SOLID_G_LEG = {k for k, v in LEGEND['ground'].items() if v[2]}
SOLID_O_LEG = {k for k, v in LEGEND['obj'].items() if v[2]}
for mid, m in MAPS.items():
    for r in m['ground']:
        for c in r: assert c in LEGEND['ground'], (mid, c)
    for r in m['obj']:
        for c in r: assert c == '.' or c in LEGEND['obj'], (mid, c)
SOLID_G.clear(); SOLID_G.update(SOLID_G_LEG); SOLID_O.clear(); SOLID_O.update(SOLID_O_LEG)

SPEAKERS = {
    'An': {'name': '小安（社工）', 'sprite': 'an'},
    'Me': {'name': '你', 'sprite': 'me'},
    'Teacher': {'name': '老師', 'sprite': 'D:88'},
    'Classmate': {'name': '同學', 'sprite': 'v5'},
    'Chief': {'name': '黃里長', 'sprite': 'chief'},
    'Zhou': {'name': '周專員（縣政府）', 'sprite': 'D:85'},
    'Driver': {'name': '公車司機', 'sprite': 'D:86'},
    'Lin': {'name': '林阿姨', 'sprite': 'lin'},
    'Wu': {'name': '吳伯伯', 'sprite': 'wu'},
    'Hao': {'name': '阿豪', 'sprite': 'hao'},
    'Li': {'name': '李大哥', 'sprite': 'li'},
    'Chen': {'name': '陳奶奶', 'sprite': 'chen'},
    'Kid': {'name': '阿弟', 'sprite': 'kid'},
    'Mei': {'name': '美玲', 'sprite': 'mei'},
    'Phone': {'name': '📱 手機', 'sprite': None},
    'Everyone': {'name': '大家', 'sprite': None},
}

# Definitions follow the textbook (黃源協、莊俐昕主編，第3版，2026), Ch. 6, pp. 139-171.
TERMS = {
    'nbcd': {'en': 'need-based community development (NBCD)', 'zh': '以需求為基礎的社區發展', 'def': '從社區的問題、缺陷與不足出發，靠外部專家調查分析，由上而下、由外而內解決。居民容易變成受助者。'},
    'community': {'en': 'community', 'zh': '社區', 'def': '具備四項基本要素：(1) 個人、團體或組織；(2) 地方；(3) 社會互動；(4) 心理認同或歸屬。'},
    'community_work': {'en': 'community work', 'zh': '社區工作', 'def': '社會工作的三大方法之一。比個案工作和團體工作更關心外在環境與社會結構對人的影響。'},
    'abcd': {'en': 'asset-based community development (ABCD)', 'zh': '以資產為基礎的社區發展', 'def': '從社區既有的資產、優勢和能力出發（例如具備技能的個人、社區組織、文化團體），由下而上、由內而外；居民是貢獻者。'},
    'self_det': {'en': 'community self-determination', 'zh': '社區自決', 'def': '社區工作的原則之一：由社區自己做決定，社區工作者是諮詢者，不是決定者。'},
    'participation': {'en': 'community participation', 'zh': '社區參與', 'def': '社區工作的原則之一：居民一起投入社區事務的討論、決定與行動。'},
    'sense': {'en': 'sense of community', 'zh': '社區意識', 'def': '社區成員之間的連結程度，以及他們對環境相互關係的認知。'},
    'capacity': {'en': 'community capacity building', 'zh': '社區能力建構', 'def': '幫助社區成員、團體或組織發展技能和能力，以增強社區解決問題、適應挑戰、提供服務及實現目標的能力。'},
    'committee': {'en': 'steering committee', 'zh': '指導委員會', 'def': '社區工作實務過程的第一步：由社區中各方代表組成，負責指導整個社區發展的推動與執行。'},
    'social_planning': {'en': 'social planning', 'zh': '社會計畫', 'def': 'Rothman 模式之一：透過科學理性的方法與技術（蒐集並分析資料）解決具體的社會問題；工作者像專家。'},
    'social_action': {'en': 'social action', 'zh': '社會行動', 'def': 'Rothman 模式之一：主要起因於受壓迫，目標是改變權力結構、重新分配資源；動員群眾、直接行動、談判協商。'},
    'locality': {'en': 'locality development', 'zh': '地方發展', 'def': 'Rothman 模式之一：擴大社區參與、共同決策，提升社區能力與自助（過程導向）；工作者是使能者、協調者。'},
    'mixed': {'en': 'mixed model', 'zh': '混合模式', 'def': 'Rothman (2001) 指出，實務上常常需要同時混合使用不同的模式。'},
    'park': {'en': 'PARK', 'zh': '保留、增加、移除、避免', 'def': '資料分析後選擇行動的方法：保留 Preserve 重要特色、增加 Add 關鍵資產、移除 Remove 降低生活品質的因素、避免 Keep out 威脅。'},
    'dependency': {'en': 'cycle of dependency', 'zh': '依賴循環', 'def': '以需求為基礎的發展前景：居民是受助者、依賴外部援助，援助一停，社區什麼都沒有留下。'},
    'celebrate': {'en': 'celebrating results', 'zh': '慶祝成果與表彰成就', 'def': '社區工作實務過程的第七步：慶祝和表彰可以提高知名度、認可參與者的貢獻，並鼓勵更多人投入。'},
}

QUIZZES = {
    'q1': {'tag': '第一章 · 小測驗 1/2', 'q': '縣府報告寫：「青溪里是一個需求很多的衰退社區，需要外部專家來解決。」這是哪一種觀點？',
           'options': ['asset-based community development (ABCD)', 'need-based community development (NBCD)', 'community care', 'social action'], 'answer': 1, 'hint': '報告從「缺什麼」開始，靠外面的人來解決。'},
    'q2': {'tag': '第一章 · 小測驗 2/2', 'q': '在 ABCD（以資產為基礎）的觀點中，居民的角色是什麼？',
           'options': ['receivers / dependents', 'outside experts', 'contributors / citizens', 'funders'], 'answer': 2, 'hint': '林阿姨、吳伯伯、阿豪都在「貢獻」自己的能力。'},
    'q3': {'tag': '第二章 · 小測驗 1/2', 'q': '颱風夜，村民自己決定要怎麼救陳奶奶，社工只提供建議、不替大家決定。這符合哪一個社區工作原則？',
           'options': ['community self-determination', 'means test', 'social planning', 'community care'], 'answer': 0, 'hint': '由社區「自己決定」。'},
    'q4': {'tag': '第二章 · 小測驗 2/2', 'q': '阿豪找人、李大哥開路、林阿姨照顧長輩：社區成員發揮技能，整個社區解決問題的能力變強了。這叫做什麼？',
           'options': ['casework', 'community capacity building', 'New Poor Law', 'friendly visiting'], 'answer': 1, 'hint': '社區的「能力」被「建構」起來了。'},
    'q5': {'tag': '第三章 · Rothman 1/3', 'q': '周專員提議：「請交通專家蒐集資料、分析路線，制定最佳方案。」這是 Rothman 的哪一種模式？',
           'options': ['locality development', 'social planning', 'social action', 'self-help group'], 'answer': 1, 'hint': '專家、資料、分析、最佳方案。'},
    'q6': {'tag': '第三章 · Rothman 2/3', 'q': '阿豪提議：「發動連署、到客運公司抗議，要求恢復公車！」這是哪一種模式？',
           'options': ['locality development', 'social planning', 'social action', 'remedial model'], 'answer': 2, 'hint': '動員群眾、改變有權力的一方。'},
    'q7': {'tag': '第三章 · Rothman 3/3', 'q': '里長提議：「村民一起討論、共同決定，用合作社的貨車組成我們自己的接送小組。」這是哪一種模式？',
           'options': ['locality development', 'social planning', 'social action', 'reciprocal model'], 'answer': 0, 'hint': '擴大參與、共同決策、提升社區自己的能力。'},
    'q8': {'tag': '第三章 · PARK', 'q': '計畫中「在舊學校開一個新的茶葉體驗教室」屬於 PARK 的哪一項？',
           'options': ['Preserve 保留', 'Add 增加', 'Remove 移除', 'Keep out 避免'], 'answer': 1, 'hint': '原本沒有，現在要多一個。'},
    'qn': {'tag': '第一條路 · 小測驗', 'q': '縣府的外部援助一停，青溪里什麼都不會了。以需求為基礎的社區發展（NBCD）做到最後，常常會帶來哪一種結果？',
           'options': ['hopeful, sustainable development', 'a cycle of dependency', 'community capacity building', 'community self-determination'], 'answer': 1, 'hint': '居民一直是「受助者」，最後只能「依賴」。'},
    'q9': {'tag': '第三章 · 實務過程', 'q': '社區工作實務過程的第一步是什麼？',
           'options': ['form a steering committee', 'celebrate results', 'evaluate and revise the plan', 'propose a new vision'], 'answer': 0, 'hint': '先找出各方代表，組成一個帶頭的團隊。'},
}

TEXT = {
    'locked': '門鎖著。',
    'idle': '走到人或東西旁邊，按 A 說話。頭上有 ! 的地方有新的事。',
    'choose': '你會怎麼做？',
    'right': '答對了！',
    'hintLead': '再想想：',
    'pauseHead': '⏸ 暫停',
    'waitFor': '{s} 後可以繼續。',
    'pickFirst': '請先選一個答案。',
    'badCode': '密碼不對。請看老師投影片上的密碼。',
    'newTerm': '新名詞 ',
    'endStats': '第一次就答對：<b>{f} / {n}</b> 題<br>筆記本：<b>{t} / {T}</b> 個名詞',
}

# ---------------------------------------------------------------- story (see story.py)
import story
_ids = {}
for line in classroom_puts().split('\n'):
    parts = line.split()
    if parts[6] != '-': _ids[parts[6]] = parts[1]
SCRIPT = (story.SCRIPT.replace('{{CLASSROOM}}', classroom_puts()).replace('{{CLASSROOM_PLAIN}}', classroom_puts(False))
          .replace('{{KIDX}}', str(KID_POS[0])).replace('{{KIDY}}', str(KID_POS[1])).replace('{{MAZE_SECONDS}}', str(story.maze_seconds(MAZE_STEPS)))
          .replace('{{A}}', _ids['cls_a'][1:]).replace('{{B}}', _ids['cls_b'][1:]).replace('{{C}}', _ids['cls_c'][1:]))
PAUSES = story.PAUSES

data = {
    'id': 'storm-creek-v2', 'start': 'intro', 'player': 'me',
    'assets': {'town': '../../assets/tiles/tinytown.png', 'dungeon': '../../assets/tiles/tinydungeon.png',
               'chars': '../../assets/tiles/characters.png', 'extra': 'extra.png'},
    'chars': CHARS, 'legend': LEGEND, 'maps': MAPS, 'speakers': SPEAKERS, 'terms': TERMS, 'quizzes': QUIZZES, 'pauses': PAUSES,
    'jumps': story.JUMPS,
    'hashJumps': {},
    'text': TEXT,
}

# every door target must be walkable, and from village spawn every exterior door must be adjacent to a reachable tile
for mid, m in MAPS.items():
    for did, d in m['doors'].items():
        if d.get('to'):
            assert walkable(MAPS[d['to']], d['tx'], d['ty']), f'{mid}/{did} lands on a wall'
north = reach(village, 33, 7)
south = reach(village, 4, 20)
def adj(seen, x, y): return any((x + a, y + b) in seen for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
for did in ('lin', 'wu', 'school', 'coop', 'grocery', 'tunnelN'): assert adj(north, village['doors'][did]['x'], village['doors'][did]['y']), did
for did in ('chen', 'tunnelS'): assert adj(south, village['doors'][did]['x'], village['doors'][did]['y']), did
assert (24, 18) in north, 'bridge must connect north and south'
t = reach(tunnel, *TUN_IN); assert TUN_OUT in t and KID_POS in t, 'tunnel must connect'
# check: every @put lands on a walkable, unblocked tile; labels exist; notes/quizzes exist
import re
labels = set(re.findall(r'^:: (\S+)', SCRIPT, re.M))
for m in re.finditer(r'^@put (\S+) (\S+) (\S+) (\d+) (\d+) (\S+)', SCRIPT, re.M):
    _id, spr, mp, x, y, lab = m.groups()
    assert walkable(MAPS[mp], int(x), int(y)), f'@put {_id} on a blocked tile {mp} {x},{y}'
    assert lab == '-' or lab in labels, f'@put {_id}: unknown label {lab}'
    assert spr in CHARS or re.match(r'^[TD]:\d+$', spr), spr
STARTS = {'village': [(33, 7), (4, 20)], 'tunnel': [TUN_IN], 'school': [(7, 8)], 'lin': [(5, 6)], 'wu': [(5, 6)], 'coop': [(5, 6)], 'chen': [(5, 6)], 'classroom': [PLAYER_SEAT]}
for m in re.finditer(r'^@put (\S+) (\S+) (\S+) (\d+) (\d+) (\S+)', SCRIPT, re.M):
    _id, spr, mp, x, y, lab = m.groups()
    if lab == '-' or _id == 'an': continue
    seen = set()
    for st in STARTS[mp]: seen |= reach(MAPS[mp], *st)
    assert adj(seen, int(x), int(y)), f'cannot walk up to {_id} on {mp} {x},{y}'
for m in re.finditer(r'^@(?:goto|label \S+) (\S+)', SCRIPT, re.M):
    assert m.group(1) == '-' or m.group(1) in labels, m.group(0)
for m in re.finditer(r'^@if \S+ (\S+)', SCRIPT, re.M): assert m.group(1) in labels, m.group(0)
for m in re.finditer(r'-> (\S+)', SCRIPT): assert m.group(1) in labels, m.group(0)
for m in re.finditer(r'^@note (\S+)', SCRIPT, re.M): assert m.group(1) in TERMS, m.group(0)
for m in re.finditer(r'^@quiz (\S+)', SCRIPT, re.M): assert m.group(1) in QUIZZES, m.group(0)
for m in re.finditer(r'^(\w[\w .]*?): ', SCRIPT, re.M):
    if not m.group(1).startswith(('?',)): assert m.group(1) in SPEAKERS, m.group(1)
assert set(TERMS) == set(re.findall(r'^@note (\S+)', SCRIPT, re.M)), 'every term should be collectable'
assert set(QUIZZES) == set(re.findall(r'^@quiz (\S+)', SCRIPT, re.M)), 'every quiz should be used'

js = ('/* 青溪颱風夜 Storm Over Clear Creek — chapter data for the story-walk engine (../engine/engine.js).\n'
      ' * GENERATED by tools/build_data.py. Edit tools/story.py (story, passwords, discussion questions) or build_data.py (maps, terms, quizzes) and run build_data.py again.\n'
      ' * Content follows textbook Ch. 6 社區工作 (黃源協、莊俐昕主編，第3版，2026). Clear Creek and its people are fictional.\n'
      ' * Art: Tiny Town + Tiny Dungeon by Kenney (www.kenney.nl), CC0 1.0; extra.png drawn for this site (CC0). */\n'
      'window.GAME = ' + json.dumps({k: v for k, v in data.items()}, ensure_ascii=False, indent=1) + ';\n'
      'window.GAME.script = ' + json.dumps(SCRIPT, ensure_ascii=False) + ';\n')
OUT.write_text(js, encoding='utf-8')
print('maze: route via the boy =', MAZE_STEPS, 'steps; direct route =', _direct, '; time limit =', story.maze_seconds(MAZE_STEPS), 's; boy at', KID_POS)
print('wrote', OUT, len(js), 'bytes;', len(labels), 'labels,', len(TERMS), 'terms,', len(QUIZZES), 'quizzes')

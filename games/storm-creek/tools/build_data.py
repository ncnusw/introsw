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
tun_g = [
    'WW+WWWWWWWWWWWWWWW',
    'WWuWWWWWWWWWWWWWWW',
    'WWuuuuuuuWWWuuuuWW',
    'WWuWWWWWuWWWuWWuWW',
    'WuuuuuWWuuuuuWWuWW',
    'WuWWWuWWWWWWuWWuWW',
    'WuWuuuWWWWWWuuuuWW',
    'WuuuWWWWWWWWWWWuWW',
    'WWWWWWWWWWWWWWW+WW',
]
tun_o = ['.' * 18 for _ in tun_g]
tunnel = {'ground': tun_g, 'obj': tun_o, 'doors': {
    'top': {'x': 2, 'y': 0, 'to': 'village', 'tx': 4, 'ty': 11, 'dir': 'up'},
    'bottom': {'x': 15, 'y': 8, 'to': 'village', 'tx': 4, 'ty': 20, 'dir': 'down'}}}

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

MAPS = {'village': village, 'tunnel': tunnel, 'school': school, 'lin': lin, 'wu': wu, 'coop': coop, 'chen': chen}

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
CHARS = ['an', 'lin', 'v2', 'v3', 'mei', 'v5', 'v6', 'v7', 'v8', 'v9', 'chen', 'hao', 'wu', 'kid', 'v14', 'li', 'chief']

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
        'w': ['dungeon', 40, 1], 'z': ['dungeon', 33, 1],
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
    'An': {'name': '小安（你）', 'sprite': 'an'},
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
    'nbcd': {'en': 'need-based community development (NBCD)', 'zh': '以需求為基礎的社區發展', 'def': '從社區的問題、缺陷與不足出發，靠外部專家調查分析，由上而下、由外而內解決。居民容易變成受助者（課本 pp. 163–165）。'},
    'community': {'en': 'community', 'zh': '社區', 'def': '具備四項基本要素：(1) 個人、團體或組織；(2) 地方；(3) 社會互動；(4) 心理認同或歸屬（p. 141）。'},
    'community_work': {'en': 'community work', 'zh': '社區工作', 'def': '社會工作的三大方法之一。比個案工作和團體工作更關心外在環境與社會結構對人的影響（p. 142）。'},
    'abcd': {'en': 'asset-based community development (ABCD)', 'zh': '以資產為基礎的社區發展', 'def': '從社區既有的資產、優勢和能力出發（例如具備技能的個人、社區組織、文化團體），由下而上、由內而外；居民是貢獻者（pp. 163–165）。'},
    'self_det': {'en': 'community self-determination', 'zh': '社區自決', 'def': '社區工作的原則之一：由社區自己做決定，社區工作者是諮詢者，不是決定者（p. 158）。'},
    'participation': {'en': 'community participation', 'zh': '社區參與', 'def': '社區工作的原則之一：居民一起投入社區事務的討論、決定與行動（pp. 155, 158）。'},
    'sense': {'en': 'sense of community', 'zh': '社區意識', 'def': '社區成員之間的連結程度，以及他們對環境相互關係的認知（p. 159）。'},
    'capacity': {'en': 'community capacity building', 'zh': '社區能力建構', 'def': '幫助社區成員、團體或組織發展技能和能力，以增強社區解決問題、適應挑戰、提供服務及實現目標的能力（p. 170）。'},
    'committee': {'en': 'steering committee', 'zh': '指導委員會', 'def': '社區工作實務過程的第一步：由社區中各方代表組成，負責指導整個社區發展的推動與執行（p. 166）。'},
    'social_planning': {'en': 'social planning', 'zh': '社會計畫', 'def': 'Rothman 模式之一：透過科學理性的方法與技術（蒐集並分析資料）解決具體的社會問題；工作者像專家（pp. 161–162）。'},
    'social_action': {'en': 'social action', 'zh': '社會行動', 'def': 'Rothman 模式之一：主要起因於受壓迫，目標是改變權力結構、重新分配資源；動員群眾、直接行動、談判協商（pp. 161–163）。'},
    'locality': {'en': 'locality development', 'zh': '地方發展', 'def': 'Rothman 模式之一：擴大社區參與、共同決策，提升社區能力與自助（過程導向）；工作者是使能者、協調者（pp. 161–162）。'},
    'mixed': {'en': 'mixed model', 'zh': '混合模式', 'def': 'Rothman (2001) 指出，實務上常常需要同時混合使用不同的模式（課本圖 6.2，pp. 163–164）。'},
    'park': {'en': 'PARK', 'zh': '保留、增加、移除、避免', 'def': '資料分析後選擇行動的方法：保留 Preserve 重要特色、增加 Add 關鍵資產、移除 Remove 降低生活品質的因素、避免 Keep out 威脅（p. 167）。'},
    'celebrate': {'en': 'celebrating results', 'zh': '慶祝成果與表彰成就', 'def': '社區工作實務過程的第七步：慶祝和表彰可以提高知名度、認可參與者的貢獻，並鼓勵更多人投入（p. 169）。'},
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
    'badCode': '密碼不對。每一章開始時，畫面上會顯示這一章的密碼。',
    'newTerm': '新名詞 ',
    'endStats': '第一次就答對：<b>{f} / {n}</b> 題<br>筆記本：<b>{t} / {T}</b> 個名詞',
}

SCRIPT = r'''
// ======================= PROLOGUE =======================
:: prologue
@save
@clear
@tint none
@music warm
@player an
@title 青溪里，颱風來的三天前|Clear Creek Village · three days before the typhoon
@door village/tunnelN lock 隧道口用木板封著。現在不需要進去。
@door village/tunnelS lock 隧道口用木板封著。
@put driver D:86 village 32 7 p_driver !
@put zhou D:85 village 29 7 -
@put stop T:83 village 33 5 c1_stop
@map village 33 8 up
@goal 和公車司機說話。

:: p_driver
@label driver p_driver2
Driver: 到了，青溪里，終點站。
Driver: 你是新來的社工吧？我勸你看看就好。
Driver: 這條路線一天兩班，客運說一直虧錢。下個月……可能就停了。
An: 那村裡的長輩要怎麼去鎮上看醫生？
Driver: 這就要問縣政府囉。喏，那位穿西裝的，就是縣府的人。
@label zhou p_zhou !
@goal 和縣府的周專員說話（司機左邊）。

:: p_driver2
Driver: 氣象說有颱風要來，你自己小心喔。

:: p_zhou
@label zhou -
Zhou: 你就是派來青溪里的社區社工？我是縣府的周專員。
Zhou: 這是我們請專家做的調查報告。你看一下。
@item 縣府報告 The County Report
> 報告封面寫著：「青溪里：一個需求很多的衰退社區」。
> 人口外流、老化、國小廢校、雜貨店關門、公車虧損、獨居長者沒吃飯……
Zhou: 問題太多了。專家建議：停掉這裡的關懷據點經費，把長輩送到城裡的機構。
An: 什麼？那他們的家怎麼辦？
Zhou: 三天後是村裡的燈籠夜，我會再來一次。
Zhou: 如果到時候，村民拿得出一份像樣的社區計畫，我就向上面爭取經費。拿不出來……就照專家的建議辦。
@move zhou 34 7
@del zhou
An: （這份報告從頭到尾只寫「缺什麼」。可是住在這裡的人呢？）
@note nbcd
@put chief chief school 7 3 ch1 !
@goal 到村子中間的社區活動中心（舊國小，紅色大屋頂）找黃里長。

:: c1_stop
> 公車站牌：「青溪里　每日 7:10、16:40」。下面貼著一張紙：「本路線將於下月停駛」。

// ======================= CHAPTER 1 =======================
:: ch1
@save
@clear
@tint none
@music warm
@player an
@title 第一章：兩張地圖|Chapter 1 · Two Maps　（密碼 MAPS）
@door village/tunnelN lock 隧道口用木板封著。陳奶奶說過，這條舊水圳隧道已經很多年沒人走了。
@door village/tunnelS lock 隧道口用木板封著。
@put chief chief school 7 3 c1_chief_wait
@put kitchen D:72 school 11 2 a_kitchen !
@put lin lin lin 5 3 a_lin !
@put wu wu wu 5 3 a_wu !
@put hao hao village 12 12 a_hao !
@put li li coop 5 3 a_li !
@put chen chen chen 5 3 a_chen !
@put mei mei village 14 8 c1_mei
@put stop T:83 village 33 5 c1_stop
@map school 7 5 up
Chief: 你就是新來的社工？歡迎、歡迎！我是黃里長。
Chief: 周專員給你看報告了吧？唉，他只看到我們缺什麼。
An: 里長，我想先好好認識這個**社區**。
Chief: 社區？就是我們這個村子啊。
An: 課本說，社區有四項基本要素：個人、團體或組織；地方；社會互動；還有心理認同或歸屬。
Chief: 喔……所以社區不只是一塊地，還是一群彼此有來往、覺得「這裡是我家」的人。
@note community
An: 而且**社區工作**不只看一個人的問題，也看整個環境和社會結構。
@note community_work
Chief: 那你打算怎麼做？
An: 專員畫了一張「問題地圖」。我想畫另一張：「資產地圖」。
Chief: 資產？我們窮得很，哪有什麼資產？
An: 有技能的人、團體和組織、地方和設施、文化和故事。這些都是社區的資產。
@note abcd
Chief: 好！那你去村子裡走走。找到六個資產，再回來告訴我。
@set assets 0
@goal 找出青溪里的六個資產（{assets}/6）。頭上有 ! 的人或東西，去看看。

:: c1_chief_wait
Chief: 資產找到幾個了？{assets} 個？加油，頭上有 ! 的人或東西都去看看。

:: c1_mei
Mei: 你在找村子的資產？去溪對面問問陳奶奶吧，過橋就到了。她知道村裡所有的故事。
Mei: 還有，舊學校裡面的廚房，你看過了嗎？

:: a_kitchen
@label kitchen a_kitchen2
> 舊國小的廚房：兩口大鍋、瓦斯爐，隔壁教室還可以坐五十個人吃飯。
An: 學校關了，可是廚房和教室都還在。這是**地方與設施**。
@item 資產卡：舊學校的廚房和教室（地方與設施）
@goto a_count

:: a_kitchen2
> 大鍋擦得很乾淨，好像隨時可以再煮一頓大餐。

:: a_lin
@label lin a_lin2
Lin: 你是新來的社工？來，先量個血壓。
Lin: 我在醫院當了三十年護理師。退休以後，每個星期天幫鄰居量血壓。
Lin: 誰的血壓高、誰最近吃不下飯，我都知道。
An: 林阿姨，你是這個村子的健康守護者！
@item 資產卡：林阿姨（具備技能的個人）
@goto a_count

:: a_lin2
Lin: 有空來量血壓喔。

:: a_wu
@label wu a_wu2
Wu: 這些竹燈籠，是我爸爸教我的。現在全村只剩我會做。
Wu: 每年秋天的燈籠夜，在外地的孩子都會回來。那一天，青溪里最熱鬧。
Wu: 我的燈籠用竹子和油紙做，風吹雨打都不會熄。
An: 這不只是一門手藝，是整個村子的記憶。
@item 資產卡：吳伯伯的竹燈籠（文化與故事）
@goto a_count

:: a_wu2
Wu: 三天後就是燈籠夜了，我還有好多燈籠要做。

:: a_hao
@label hao a_hao2
Hao: 你好！我是阿豪。我在臺北做了五年行銷，去年回來種茶。
Hao: 村裡的 LINE 群組是我開的，一百多個人，連住在臺中的孩子都在裡面。
Hao: 有什麼事，我發一則訊息，十分鐘全村都知道。
@item 資產卡：阿豪和村民群組（具備技能的個人）
@goto a_count

:: a_hao2
Hao: 今年的茶，香得不得了！

:: a_li
@label li a_li2
Li: 這裡是青溪茶農產銷合作社。三十二戶茶農，一起買肥料、一起賣茶。
Li: 我們還有一台貨車，平常載茶葉下山。
An: 一個早就習慣一起合作的組織，還有一台車！
@item 資產卡：茶農合作社和貨車（社區組織）
@goto a_count

:: a_li2
Li: 合作社的大家，都是從小一起長大的。

:: a_chen
@label chen a_chen2
Chen: 小姐，你從橋那邊走過來的？這座橋，我小時候還是竹子搭的。
Chen: 我在這條溪邊住了八十二年。哪裡會淹水、哪裡有路，我都知道。
Chen: 西邊山腳下有一條很老的水圳隧道，從村子那頭可以一直通到我家這頭。現在沒人走了，裡面黑漆漆的。
An: 陳奶奶，你就是一本活的地圖。
Chen: 呵呵。只是……公車要是停了，我每個星期四就沒辦法去鎮上看醫生了。
@item 資產卡：陳奶奶的河流故事（文化與故事）
@goto a_count

:: a_chen2
Chen: 西邊山腳下的舊水圳隧道，記得喔。說不定哪天用得到。

:: a_count
@inc assets
@goal 找出青溪里的六個資產（{assets}/6）。頭上有 ! 的人或東西，去看看。
@if assets>=6 a_done

:: a_done
@goal 回社區活動中心，把資產地圖拿給黃里長看。
@label chief c1_report !

:: c1_report
@label chief c1_chief_done
Chief: 六個？你真的找到六個？
An: 林阿姨、吳伯伯的燈籠、阿豪的群組、茶農合作社、舊學校的廚房，還有陳奶奶的河流故事。
Chief: ……這些我每天都看到，卻從來沒想過它們是「資產」。
An: 專員的報告從缺陷出發，由外而內，居民只是等人來幫忙的受助者。
An: 資產地圖從我們已經有的東西出發，由內而外，居民是貢獻者。
@quiz q1
@quiz q2
Chief: 好！燈籠夜那天，我們就拿這張資產地圖給專員看！
> 就在這時候，所有人的手機同時響了起來。
Phone: 【颱風警報】強烈颱風今晚登陸，中部山區將有豪雨，請民眾提早做好準備。
Chief: 什麼？今天晚上？
@goto ch2

:: c1_chief_done
Chief: 颱風要來了，大家小心！

// ======================= CHAPTER 2 =======================
:: ch2
@save
@clear
@tint storm
@music tick
@player an
@title 第二章：颱風夜|Chapter 2 · Typhoon Night　（密碼 STORM）
@set team 0
@door village/tunnelN lock 隧道裡黑漆漆的，什麼都看不到。需要一盞不會被風雨吹熄的燈。
@door village/tunnelS lock 這是隧道的另一頭出口。
@door village/chen lock 先回活動中心，看看大家怎麼樣了。
@put rock1 D:66 village 23 16 c2_bridge
@put rock2 D:66 village 24 16 c2_bridge
@put tree T:16 village 4 9 c2_tree
@put chief chief school 7 3 c2_chief !
@put hao hao school 4 4 c2_hao_wait
@put lin lin school 10 4 c2_lin_wait
@put mei mei school 3 6 c2_mei
@put li li coop 5 3 c2_li_wait
@put wu wu wu 5 3 c2_wu_wait
@put kid kid tunnel 13 6 c2_kid !
@put chen chen chen 5 3 c2_chen !
@zone storm village 0 0 36 26 c2_out
@zone dark tunnel 0 0 18 9 c2_in
@zone in1 school 0 0 15 10 c2_indoor
@zone in2 wu 0 0 11 8 c2_indoor
@zone in3 coop 0 0 11 8 c2_indoor
@zone in4 lin 0 0 11 8 c2_indoor
@zone in5 chen 0 0 11 8 c2_indoor
@map school 7 6 up
> 晚上九點。狂風暴雨打在活動中心的窗戶上。
> 停電了。村民拿著手電筒，陸續來到活動中心避難。
@goal 和黃里長說話。

:: c2_out
@tint storm

:: c2_indoor
@tint night

:: c2_in
@tint night
@if tun=1 c2_in_done
@set tun 1
> 竹燈籠照亮了潮濕的石壁。水從頭上一滴一滴落下來。
Lin: 小心腳下，地很滑。

:: c2_in_done
@tint night

:: c2_bridge
> 溪水變成了咖啡色，轟隆隆地衝過來。橋被沖壞了，到處都是石頭和斷木。
An: 這裡過不去。

:: c2_chief
@label chief c2_chief_wait
Chief: 社工！剛剛消防隊打電話來：溪水暴漲，橋被沖壞了，救援隊最快明天中午才進得來。
Chief: 我們……就只能等縣府的人來救了吧？
An: 里長，你還記得那張資產地圖嗎？
@choice
? 等縣府的救援隊明天來處理。 -> c2_wait
? 把村民召集起來，一起想辦法。 -> c2_gather

:: c2_wait
Chief: 也是，這種事還是交給專業的人……
> 一個小時過去了。雨越下越大。
Mei: 里長！有人看到陳奶奶嗎？她家在溪的對岸，電話一直打不通！
An: （只靠外面的人，可能會來不及。社區自己也有力量。）
@goto c2_gather

:: c2_gather
Chief: 好！大家聽我說——
An: 這是大家的村子。要怎麼做，由大家一起決定。我會幫忙，但不會替大家決定。
@note self_det
Everyone: 好！
Chief: 第一件事：我們要確定每一戶都平安。
@label hao c2_hao !
@goal 請阿豪用村民群組確認大家是否平安。

:: c2_chief_wait
Chief: 大家都在等你。我們一起想辦法！

:: c2_mei
Mei: 我家阿弟……剛剛說要去找小狗，到現在還沒回來……

:: c2_mei2
Mei: 謝謝你找到阿弟！

:: c2_hao_wait
Hao: 群組裡大家都在問怎麼了。里長有什麼要我做的嗎？

:: c2_hao
@label hao c2_hao2
Hao: 交給我！我在群組發訊息，請每一戶回報平安。
@wait 500
Phone: 【青溪村民群組】已回報：98 戶……102 戶……104 戶……
Hao: 只剩一戶沒有回報……是陳奶奶。
Mei: 陳奶奶有高血壓，她的藥這兩天剛好吃完了……
An: 她家在溪的對岸，橋又斷了。
An: 等等，還有另一條路！陳奶奶說過，西邊山腳下有一條舊水圳隧道，可以通到她家那頭。
Chief: 那條隧道？二十年沒人走了！而且去隧道的路上，剛剛有一棵大樹倒下來……
An: 所以我們需要大家一起幫忙。每個人都出一點力。
@note participation
@label li c2_li !
@label wu c2_wu !
@label lin c2_lin !
@goal 召集救援小隊（{team}/3）：合作社的貨車（右上）、吳伯伯的燈籠、林阿姨（就在這裡）。

:: c2_hao2
Hao: 我會一直盯著群組。你們小心！

:: c2_lin_wait
Lin: 好大的雨。陳奶奶一個人在家，不知道怎麼樣了。

:: c2_lin
@label lin c2_lin2
Lin: 陳奶奶的藥？我家有一樣的，而且我可以幫她量血壓。
Lin: 我跟你們一起去。三十年的護理師，這點風雨不算什麼。
@item 救援小隊：林阿姨加入！
@goto c2_team

:: c2_lin2
Lin: 我準備好了。藥和血壓計都帶了。

:: c2_li_wait
Li: 這種天氣，貨車可不能隨便開出去。

:: c2_li
@label li c2_li2
Li: 去隧道的路上有大樹倒了？我們合作社有貨車，還有繩子和鏈鋸。
Li: 我去叫幾個年輕的茶農，在西邊路口集合！
@set truck 1
@item 救援小隊：茶農合作社的貨車和繩子！
@goto c2_team

:: c2_li2
Li: 茶農們都到了。西邊路口見！

:: c2_wu_wait
Wu: 風這麼大，我的燈籠可不能被吹壞。

:: c2_wu
@label wu c2_wu2
Wu: 隧道裡很黑？拿我的竹燈籠去。油紙做的，風吹雨打都不會熄。
Wu: 我做了一輩子燈籠，沒想到有一天能拿來救人。
@item 救援小隊：吳伯伯的竹燈籠！
@door village/tunnelN reset
@door village/tunnelS reset
@goto c2_team

:: c2_wu2
Wu: 燈籠拿好。路上小心！

:: c2_team
@inc team
@goal 召集救援小隊（{team}/3）：合作社的貨車、吳伯伯的燈籠、林阿姨。
@if team>=3 c2_go

:: c2_go
@door village/chen reset
@goal 到西邊山腳下的舊水圳隧道。先處理路上倒下來的大樹！
@label tree c2_tree !

:: c2_tree
@if team>=3 c2_tree_go
> 一棵大樹倒在路上，擋住了去隧道的路。一個人根本搬不動。

:: c2_tree_go
@label tree -
Li: 來，繩子綁好！大家一起——一、二、三，拉！
> 茶農們把大樹鋸開，一起拖到路邊。
@del tree
Li: 我們平常一起採茶，今天一起救人！
@goal 走進舊水圳隧道，找到通往溪對岸的出口。

:: c2_kid
@label kid c2_kid2
Kid: 嗚……誰？有燈！
An: 阿弟？你怎麼會在這裡？
Kid: 我的小狗跑掉了，我一直追到這裡，雨好大，我不敢出去……
Lin: 沒事了，沒事了。你媽媽在活動中心等你。
Kid: 姊姊，你們要去陳奶奶家嗎？我知道路！往前走，右轉，再一直走，就到陳奶奶家旁邊了！
@set kid 1
@item 找到阿弟了！
@label mei c2_mei2

:: c2_kid2
Kid: 往前走，右轉，再一直走！

:: c2_chen
@label chen c2_chen2
Chen: ……是誰？
An: 陳奶奶！我們來接你了！
Chen: 你們……怎麼過來的？橋不是斷了嗎？
An: 走你告訴我的那條舊水圳隧道。
@put lin lin chen 7 3 -
Lin: 奶奶，我先幫你量血壓……有點高，先把藥吃了。
Chen: 我還以為……今天晚上就要一個人待在這裡了。
An: 不會的。這個村子不會丟下任何一個人。
Chen: 青溪里……還是青溪里啊。
@note sense
@put chen chen school 9 3 -
@put lin lin school 10 4 -
@label chief c2_back !
@goal 護送陳奶奶，從隧道回到社區活動中心。

:: c2_chen2
> 李大哥背著陳奶奶，林阿姨提著燈籠走在旁邊。

:: c2_back
@label chief -
Chief: 回來了！陳奶奶平安回來了！
Everyone: 太好了！
@if kid=1 c2_back_kid
@goto c2_back2

:: c2_back_kid
Mei: 阿弟！你跑到哪裡去了！……謝謝你們！
@goto c2_back2

:: c2_back2
Chief: 今天晚上，沒有人只是等別人來救。我們自己救了自己。
An: 阿豪找人、李大哥和茶農開路、吳伯伯的燈籠照路、林阿姨照顧陳奶奶……
An: 每個人都發揮了自己的能力，整個社區解決問題的能力也變強了。這就是**社區能力建構**。
@note capacity
@quiz q3
@quiz q4
> 天快亮的時候，風雨慢慢停了。
@goto ch3

// ======================= CHAPTER 3 =======================
:: ch3
@save
@clear
@tint none
@music warm
@player an
@title 第三章：村民大會|Chapter 3 · The Town Hall　（密碼 TOWNHALL）
@put zhou D:85 school 7 2 c3_start !
@put chief chief school 5 3 c3_wait
@put hao hao school 3 4 c3_wait
@put li li school 11 4 c3_wait
@put lin lin school 10 3 c3_wait
@put chen chen school 9 3 c3_wait
@put wu wu school 4 3 c3_wait
@put mei mei school 2 6 c3_wait
@map school 7 7 up
> 颱風過後的早上。周專員提早來了。
@goal 和周專員說話，開始村民大會。

:: c3_wait
> 大家都在等周專員開口。

:: c3_start
@label zhou -
Zhou: 我聽說昨晚的事了。這正好證明：住在這裡太危險，長輩應該搬到城裡。
Chief: 專員，請先聽聽我們的計畫。
Zhou: ……好，你們說說看。不過我要先問：這個計畫是誰在帶頭？
An: 我們成立了一個**指導委員會**：里長、林阿姨、合作社的李大哥、阿豪，還有陳奶奶。各方代表都有。
@quiz q9
@note committee
Zhou: 嗯。那公車停駛的問題呢？我聽說大家意見不太一樣。
> 好幾個人同時舉手。
Zhou: 一個一個來。我先說縣府的想法：我們可以請交通專家蒐集資料、分析路線，制定最佳方案。
@quiz q5
@note social_planning
Hao: 我覺得應該發動連署，到客運公司和縣議會抗議！他們不能說停就停！
@quiz q6
@note social_action
Chief: 我覺得村民應該一起討論、共同決定，用合作社的貨車組成我們自己的接送小組。
@quiz q7
@note locality
An: 三個方法都有道理。Rothman 也說過，真實的社區常常需要混合使用不同的模式。
An: 指導委員會的各位，你們想怎麼混合？
@choice
? 先組村民接送小組，同時請專家設計長期路線。（地方發展＋社會計畫）
? 先連署爭取恢復公車，同時組村民接送小組。（社會行動＋地方發展）
? 請專家調查，再拿調查結果去和客運公司談判。（社會計畫＋社會行動）
@note mixed
Chief: 好！就這麼決定。
An: 最後，我們用 PARK 整理整個計畫。
An: 保留 Preserve：舊學校的廚房、燈籠夜。增加 Add：村民接送小組、長輩共餐。
An: 移除 Remove：長輩一個人在家吃不到飯的情況。避免 Keep out：讓長輩被迫離開自己的家。
@note park
@quiz q8
Zhou: ……我來這裡以前，手上只有一份問題清單。
Zhou: 現在我看到的，是一個能自己站起來的社區。
Zhou: 好。我回去向上面爭取經費，讓你們試試看這個計畫。
Everyone: 耶！
Chief: 今天晚上的燈籠夜，照常舉行！
@goto epilogue

// ======================= EPILOGUE =======================
:: epilogue
@save
@clear
@tint dusk
@music bright
@player an
@title 尾聲：燈籠夜|Epilogue · Lantern Night　（密碼 LANTERN）
@put l1 T:94 village 5 5 -
@put l2 T:94 village 11 5 -
@put l3 T:94 village 19 5 -
@put l4 T:94 village 24 5 -
@put l5 T:94 village 30 5 -
@put chief chief village 21 5 ep_chief !
@put wu wu village 13 7 ep_wu
@put chen chen village 18 7 ep_chen
@put hao hao village 25 7 ep_hao
@put lin lin village 9 7 ep_lin
@put li li village 28 6 ep_li
@put mei mei village 16 6 ep_mei
@put kid kid village 17 6 ep_kid
@put stop T:83 village 33 5 c1_stop
@map village 21 7 up
> 天黑了。上百盞竹燈籠沿著村子的道路亮了起來。
@goal 和黃里長說話。

:: ep_chief
@label chief ep_chief2
Chief: 各位！今天，我們要謝謝颱風夜裡每一個出力的人！
> 里長把一張張感謝狀，發給阿豪、李大哥和茶農們、吳伯伯、林阿姨，還有阿弟。
An: （社區工作的第七步：**慶祝成果與表彰成就**。被看見的人，下一次會更願意投入。）
@note celebrate
Chief: 還有我們的社工！
Everyone: 謝謝小安！
@put driver D:86 village 32 7 ep_driver !
@goal 和大家說說話。好像有人在公車站等你（右邊）。

:: ep_chief2
Chief: 明年的燈籠夜，一定更熱鬧！

:: ep_wu
Wu: 今年的燈籠，是全村一起做的。連阿弟都做了一個，歪歪的，可是很好看。

:: ep_chen
Chen: 社工小姐，明年燈籠夜，你還會在這裡嗎？
An: 會的。而且明年，我們要一起想一個新的願景。

:: ep_hao
Hao: 我想好新的願景了：「青溪里，一個沒有人被留下的村子。」怎麼樣？

:: ep_lin
Lin: 從下個星期開始，舊學校每個星期三中午有長輩共餐。我負責量血壓！

:: ep_li
Li: 合作社的貨車，以後每個星期四載長輩去鎮上看醫生。

:: ep_mei
Mei: 謝謝你們，青溪里好像又活過來了。

:: ep_kid
Kid: 我的小狗也找到了！牠自己跑回家了！

:: ep_driver
Driver: 嘿！社工！好消息！
Driver: 客運公司說，只要村裡的接送小組幫忙接駁，這條路線先不停，再試半年！
An: 太好了！
> 燈籠的光，一盞一盞映在溪水上。
@end
'''

data = {
    'id': 'storm-creek', 'start': 'prologue', 'player': 'an',
    'assets': {'town': '../../assets/tiles/tinytown.png', 'dungeon': '../../assets/tiles/tinydungeon.png',
               'chars': '../../assets/tiles/characters.png', 'extra': 'extra.png'},
    'chars': CHARS, 'legend': LEGEND, 'maps': MAPS, 'speakers': SPEAKERS, 'terms': TERMS, 'quizzes': QUIZZES, 'pauses': {},
    'jumps': {'MAPS': 'ch1', 'STORM': 'ch2', 'TOWNHALL': 'ch3', 'LANTERN': 'epilogue'},
    'hashJumps': {'prologue': 'prologue', 'ch1': 'ch1', 'ch2': 'ch2', 'ch3': 'ch3', 'epilogue': 'epilogue'},
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
t = reach(tunnel, 2, 1); assert (15, 7) in t, 'tunnel must connect'
# check: every @put lands on a walkable, unblocked tile; labels exist; notes/quizzes exist
import re
labels = set(re.findall(r'^:: (\S+)', SCRIPT, re.M))
for m in re.finditer(r'^@put (\S+) (\S+) (\S+) (\d+) (\d+) (\S+)', SCRIPT, re.M):
    _id, spr, mp, x, y, lab = m.groups()
    assert walkable(MAPS[mp], int(x), int(y)), f'@put {_id} on a blocked tile {mp} {x},{y}'
    assert lab == '-' or lab in labels, f'@put {_id}: unknown label {lab}'
    assert spr in CHARS or re.match(r'^[TD]:\d+$', spr), spr
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
      ' * GENERATED by tools/build_data.py. Edit that file (story script, maps, terms, quizzes) and run it again.\n'
      ' * Content follows textbook Ch. 6 社區工作 (黃源協、莊俐昕主編，第3版，2026). Clear Creek and its people are fictional.\n'
      ' * Art: Tiny Town + Tiny Dungeon by Kenney (www.kenney.nl), CC0 1.0; extra.png drawn for this site (CC0). */\n'
      'window.GAME = ' + json.dumps({k: v for k, v in data.items()}, ensure_ascii=False, indent=1) + ';\n'
      'window.GAME.script = ' + json.dumps(SCRIPT, ensure_ascii=False) + ';\n')
OUT.write_text(js, encoding='utf-8')
print('wrote', OUT, len(js), 'bytes;', len(labels), 'labels,', len(TERMS), 'terms,', len(QUIZZES), 'quizzes')

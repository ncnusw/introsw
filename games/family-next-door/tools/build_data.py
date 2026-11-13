"""Builds data.js for 隔壁那一家 The Family Next Door. Run from anywhere: python3 tools/build_data.py
Maps, terms and exam questions are here; the story script, pauses and jump codes are in story.py.
It also checks that every door and every person can be reached and every label exists."""
import json, pathlib, collections, re, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
OUT = HERE.parent / 'data.js'

def blank(w, h, ch='.'):
    return [[ch] * w for _ in range(h)]

def stamp(grid, x, y, rows):
    for j, r in enumerate(rows):
        for i, c in enumerate(r):
            if c != ' ':
                grid[y + j][x + i] = c

GRAY6 = ['abbdbc', 'ehhjhi', 'lnmnnr', 'lmmpmr']
RED6 = ['ABDBBC', 'EFYFFG', 'LNMNNR', 'LMMPMR']
GRAY11 = ['abbbbdbbbbc', 'ehhhhjhhhhi', 'lnmnmnmnmnr', 'lmmmmpmmmmr']
RED11 = ['ABBBBDBBBBC', 'EFFFFYFFFFG', 'LNMNMNMNMNR', 'LNMNMPMNMNR']

# ---------------------------------------------------------------- Peace Lane 和平巷, 38 x 22
W, H = 38, 22
g = blank(W, H, '.')
o = blank(W, H, '.')
for y in range(H):
    for x in range(W):
        if (x * 7 + y * 13) % 17 == 0: g[y][x] = ','
        elif (x * 5 + y * 11) % 41 == 0: g[y][x] = '*'
for x in range(W): o[0][x] = 'T'; o[H - 1][x] = 'T'
for y in range(H): o[y][0] = 'T'; o[y][W - 1] = 'T'
# north row: Jay's home, the Chens, Auntie Wang, the library
stamp(o, 2, 1, GRAY6)      # Jay, door (5,4)
stamp(o, 9, 1, RED6)       # Chen, door (12,4)
stamp(o, 16, 1, GRAY6)     # Wang, door (19,4)
stamp(o, 23, 1, GRAY11)    # library, door (28,4)
for x in (1, 8, 15, 22): o[1][x] = 'U' if x % 2 else 'T'
for y in range(1, 5):
    for x in (34, 35, 36): o[y][x] = 'T' if (x + y) % 2 else 'U'
# the lane
for y in (6, 7):
    for x in range(1, 37): g[y][x] = '='
# empty lot (dirt) in the south-west
for y in range(10, 18):
    for x in range(2, 11): g[y][x] = 'd'
for x in (2, 10): o[9][x] = 'O'
# south row: the Lees, Hillside University, the Huangs
stamp(o, 13, 12, GRAY6)    # Lee, door (16,15)
stamp(o, 20, 12, RED11)    # university, door (25,15)
stamp(o, 31, 12, RED6)     # Huang, door (34,15)
# paths: two connectors down to a lower lane
for y in range(8, 18):
    g[y][11] = '='; g[y][19] = '='
for x in range(11, 37):
    g[16][x] = '='; g[17][x] = '='
o[9][13] = 'g'; o[9][14] = 'g'                    # log bench near the lot
for (x, y) in [(3, 19), (7, 20), (12, 19), (16, 20), (22, 19), (27, 20), (31, 19), (35, 19), (14, 10), (29, 10), (33, 9), (1, 12), (1, 16)]:
    o[y][x] = 'T' if (x + y) % 2 else 'U'
for (x, y) in [(18, 10), (24, 9), (31, 10), (36, 10)]: o[y][x] = 'O'
lane = {
    'ground': [''.join(r) for r in g], 'obj': [''.join(r) for r in o],
    'doors': {
        'jay': {'x': 5, 'y': 4, 'to': 'jay', 'tx': 5, 'ty': 6, 'dir': 'up'},
        'chen': {'x': 12, 'y': 4, 'to': 'chen', 'tx': 5, 'ty': 6, 'dir': 'up'},
        'wang': {'x': 19, 'y': 4, 'locked': True, 'msg': '王阿姨家。門關著，裡面傳來電視的聲音。'},
        'library': {'x': 28, 'y': 4, 'to': 'library', 'tx': 8, 'ty': 10, 'dir': 'up'},
        'lee': {'x': 16, 'y': 15, 'locked': True, 'msg': '李先生家。門鎖著。'},
        'univ': {'x': 25, 'y': 15, 'to': 'hall', 'tx': 7, 'ty': 8, 'dir': 'up'},
        'huang': {'x': 34, 'y': 15, 'locked': True, 'msg': '黃伯伯家。門鎖著。'},
    }}

# ---------------------------------------------------------------- interiors
def room(w, h, floor, out_to, ox, oy, obj_rows, door_x=None):
    door_x = door_x if door_x is not None else w // 2
    gr = (['W' * w, 'WW' + 'V' + 'W' * (w - 6) + 'V' + 'WW'] + ['W' + floor * (w - 2) + 'W' for _ in range(h - 3)]
          + ['W' * door_x + '+' + 'W' * (w - door_x - 1)])
    return {'ground': gr, 'obj': obj_rows, 'doors': {'out': {'x': door_x, 'y': h - 1, 'to': out_to, 'tx': ox, 'ty': oy, 'dir': 'down'}}}

home_rows = ['...........', '...........', '.0.....3...', '......1....', '......2....', '...........', '...........', '...........']
jay = room(11, 8, 'k', 'lane', 5, 5, home_rows)
chen = room(11, 8, 'f', 'lane', 12, 5, ['...........', '...........', '.0.....4...', '......1....', '......2....', '...........', '...........', '...........'])
# library 17 x 12: shelves on the back wall, two collections (BSW left, MSW right) placed by the script
library = room(17, 12, 'f', 'lane', 28, 5, [
    '.................',
    '.................',
    '.34343.....34343.',
    '.................',
    '.................',
    '.................',
    '.................',
    '..1.2.......2.1..',
    '.................',
    '.................',
    '.................',
    '.................'], 8)
# exam hall 15 x 10, blackboard on the back wall
hall = room(15, 10, 'f', 'lane', 25, 16, [
    '...............', '.....789.......', '...............', '...............', '..1.1.....1.1..',
    '..2.2.....2.2..', '...............', '...............', '...............', '...............'], 7)

MAPS = {'lane': lane, 'jay': jay, 'chen': chen, 'library': library, 'hall': hall}

# ---------------------------------------------------------------- tiles
LEGEND = {
    'ground': {
        '.': ['town', 0, 0], ',': ['town', 1, 0], '*': ['town', 2, 0], '=': ['town', 40, 0], 'd': ['town', 25, 0],
        'f': ['dungeon', 48, 0], 'k': ['dungeon', 0, 0],
        'W': ['dungeon', 40, 1], 'V': ['dungeon', 28, 1], '+': ['dungeon', 42, 0]},
    'obj': {
        'T': ['town', 16, 1], 'U': ['town', 15, 1], 'O': ['town', 5, 1],
        'A': ['town', 52, 1], 'B': ['town', 53, 1], 'C': ['town', 54, 1], 'D': ['town', 55, 1], 'E': ['town', 64, 1], 'F': ['town', 65, 1],
        'G': ['town', 66, 1], 'Y': ['town', 67, 1], 'L': ['town', 72, 1], 'M': ['town', 73, 1], 'R': ['town', 75, 1], 'N': ['town', 84, 1], 'P': ['town', 85, 1],
        'a': ['town', 48, 1], 'b': ['town', 49, 1], 'c': ['town', 50, 1], 'd': ['town', 51, 1], 'e': ['town', 60, 1], 'h': ['town', 61, 1],
        'i': ['town', 62, 1], 'j': ['town', 63, 1], 'l': ['town', 76, 1], 'm': ['town', 77, 1], 'r': ['town', 79, 1], 'n': ['town', 88, 1], 'p': ['town', 89, 1],
        'g': ['town', 106, 1],
        '7': ['extra', 9, 1], '8': ['extra', 10, 1], '9': ['extra', 11, 1],
        '0': ['dungeon', 67, 1], '1': ['dungeon', 72, 1], '2': ['dungeon', 73, 0], '3': ['dungeon', 63, 1], '4': ['dungeon', 75, 1]}}
SOLID_G = {k for k, v in LEGEND['ground'].items() if v[2]}
SOLID_O = {k for k, v in LEGEND['obj'].items() if v[2]}
for mid, m in MAPS.items():
    w = len(m['ground'][0])
    assert all(len(r) == w for r in m['ground'] + m['obj']), mid
    assert len(m['ground']) == len(m['obj']), mid
    for r in m['ground']:
        for c in r: assert c in LEGEND['ground'], (mid, c)
    for r in m['obj']:
        for c in r: assert c == '.' or c in LEGEND['obj'], (mid, c)

def walkable(m, x, y):
    gr, ob = m['ground'], m['obj']
    if not (0 <= y < len(gr) and 0 <= x < len(gr[0])): return False
    return gr[y][x] not in SOLID_G and ob[y][x] not in SOLID_O

def reach(m, sx, sy, blocked=frozenset()):
    seen = {(sx, sy)}; q = collections.deque([(sx, sy)])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and n not in blocked and walkable(m, *n): seen.add(n); q.append(n)
    return seen

# ---------------------------------------------------------------- characters, speakers
# order = position in assets/tiles/characters.png
CHARS = ['liu', 'librarian', 'v2', 'chenma', 'v4', 'star', 'v6', 'wang', 'v8', 'v9', 'jaymom', 'lee', 'agong', 'yu', 'me', 'huang', 'chief']
SPEAKERS = {
    'Me': {'name': '阿哲（你）', 'sprite': 'me'},
    'Mom': {'name': '媽媽', 'sprite': 'jaymom'},
    'ChenMa': {'name': '陳媽媽', 'sprite': 'chenma'},
    'Yu': {'name': '小宇', 'sprite': 'yu'},
    'Agong': {'name': '陳阿公', 'sprite': 'agong'},
    'Chief': {'name': '里長', 'sprite': 'chief'},
    'Wang': {'name': '王阿姨', 'sprite': 'wang'},
    'Lee': {'name': '李先生', 'sprite': 'lee'},
    'Huang': {'name': '黃伯伯', 'sprite': 'huang'},
    'Liu': {'name': '劉小姐', 'sprite': 'liu'},
    'Star': {'name': '籃球網紅「小飛」', 'sprite': 'star'},
    'Lib': {'name': '溫館員（圖書館）', 'sprite': 'librarian'},
    'Prof': {'name': '張教授', 'sprite': 'D:88'},
    'ProfYe': {'name': '葉教授', 'sprite': 'D:100'},
    'Student': {'name': '同學', 'sprite': 'v6'},
    'Everyone': {'name': '大家', 'sprite': None},
}

TERMS = {
    # ways of knowing that are not research (Act 1)
    'intuition': {'en': 'intuition & personal experience', 'zh': '個人直覺與經驗', 'def': '「我以前也是這樣，所以他一定也是。」只用自己的感覺和經驗下判斷，沒有去查證。 Judging from your own feelings and past, without checking.'},
    'authority': {'en': 'authority', 'zh': '權威人士的說法', 'def': '因為說話的人有地位（里長、老師、專家），就相信他說的是對的。 Believing something because of who says it.'},
    'tradition': {'en': 'tradition', 'zh': '傳統與前例', 'def': '「我們一直都是這樣做的。」照過去的做法，卻沒有檢查它有沒有用。 Doing it the old way without checking whether it works.'},
    'common_sense': {'en': 'common sense', 'zh': '一般常識', 'def': '「大家都知道……」聽起來很合理，但不一定是真的。 What "everyone knows" can be wrong.'},
    'logic': {'en': 'logic (reasoning)', 'zh': '邏輯推理', 'def': '推理的形式正確，但如果前提沒有查證，結論還是會錯。 Correct reasoning from an unchecked premise still gives a wrong answer.'},
    'halo': {'en': 'halo effect', 'zh': '月暈效應', 'def': '因為一個人某方面很好（籃球、外表、名氣），就以為他每一方面都很好。 Good at one thing ≠ good at everything.'},
    # BSW collection
    'empirical': {'en': 'empirical research', 'zh': '實證研究', 'def': '有系統地蒐集資料、分析資料，用證據來回答問題。 Answering questions by collecting and analyzing data.'},
    'purposes': {'en': 'five purposes of research', 'zh': '研究的五個目的', 'def': '敘述（發生什麼？）、解釋（為什麼？）、預測（會怎樣？）、介入與處遇（該怎麼做？）、比較與評估（有效嗎？）。 Describe, explain, predict, intervene, evaluate.'},
    'quantitative': {'en': 'quantitative research', 'zh': '量化研究', 'def': '用數字「算」：問卷、統計。適合描述多少人、比較、預測。 Counting: surveys and statistics.'},
    'qualitative': {'en': 'qualitative research', 'zh': '質性研究', 'def': '用文字「懂」：訪談、觀察，在自然的情境中了解人的經驗與意義。 Understanding: interviews and observation.'},
    'deductive': {'en': 'deductive logic', 'zh': '演繹法', 'def': '從理論或假設出發，再用資料檢驗（常見於量化研究）。 Theory → hypothesis → data.'},
    'inductive': {'en': 'inductive logic', 'zh': '歸納法', 'def': '從資料出發，慢慢找出模式，建立新的想法或理論（常見於質性研究）。 Data → patterns → new idea.'},
    'research_question': {'en': 'research question', 'zh': '研究問題', 'def': '研究要回答的問題。好的研究問題清楚、可以用資料回答、而且重要。 Clear, answerable, and important.'},
    'hypothesis': {'en': 'hypothesis', 'zh': '研究假設', 'def': '可以被資料檢驗的預測，常寫成「如果……，那麼……」。 A testable prediction: "If…, then…"'},
    # MSW collection
    'six_steps': {'en': 'six steps of research', 'zh': '研究的六個步驟', 'def': '選定研究問題 → 檢閱文獻 → 提出研究設計 → 蒐集資料 → 分析資料 → 撰寫研究報告。'},
    'lit_review': {'en': 'literature review', 'zh': '文獻探討', 'def': '先查已經有哪些研究，並判斷來源可不可信（例如經過同儕審查的期刊），不要從零開始猜。 What do we already know?'},
    'informed_consent': {'en': 'informed consent', 'zh': '知情同意', 'def': '研究前先說清楚目的、過程與風險；參與者了解後自願同意，也可以隨時退出。 People agree freely after they understand.'},
    'confidentiality': {'en': 'confidentiality', 'zh': '保密', 'def': '保護參與者的身分和資料，不公開可以認出他們的資訊。 Protect who said what.'},
    'ebp': {'en': 'evidence-based practice (EBP)', 'zh': '實證為基礎的實務', 'def': '結合三件事：最好的研究證據、社工的專業經驗、案主的價值與偏好。 Evidence + expertise + client values.'},
    'needs_assessment': {'en': 'needs assessment', 'zh': '需求評量', 'def': '在方案開始「之前」，先蒐集資料了解大家真正需要什麼。 Before the program: what do people need?'},
    'output_outcome': {'en': 'output vs. outcome', 'zh': '產出與成效', 'def': '產出＝做了多少（辦了幾次課）；成效＝改變了多少（跌倒少了多少）。 How much we did vs. how much changed.'},
    'comparison_group': {'en': 'comparison group', 'zh': '比較組', 'def': '找一群相似、但沒有參加方案的人來比較，才比較能確定改變是方案造成的。 Compare with similar people who did not get the program.'},
    # Act 3
    'mixed_methods': {'en': 'mixed methods', 'zh': '混合研究方法', 'def': '同時使用量化（問卷）和質性（訪談），既知道「多少」，也知道「為什麼」。 Counting and understanding together.'},
}

def exam(tag, q, options, answer, var):
    return {'tag': tag, 'q': q, 'options': options, 'answer': answer, 'hint': '', 'exam': var}

QUIZZES = {
    # BSW final exam (one question per BSW book)
    'e1': exam('BSW 畢業考 · 1 / 5', 'Ah-Zhe asks every household on the lane to fill in a survey, then counts and analyzes the answers. What is this?\n阿哲請巷子裡每一戶填問卷，再統計、分析答案。這是什麼？',
               ['empirical research 實證研究', 'authority 權威', 'tradition 傳統與前例', 'halo effect 月暈效應'], 0, 'bsw'),
    'e2': exam('BSW 畢業考 · 2 / 5', '"**Why** does Xiao Yu skip school?" This question is mainly about which purpose of research?\n「小宇**為什麼**蹺課？」這主要是哪一個研究目的？',
               ['describe 敘述', 'explain 解釋', 'predict 預測', 'evaluate 評估'], 1, 'bsw'),
    'e3': exam('BSW 畢業考 · 3 / 5', 'Ah-Zhe talks with Grandpa Chen for one hour about his life, then looks for themes in his words. What kind of research is this?\n阿哲和陳阿公聊了一小時，再從他的話裡找出主題。這是哪一種研究？',
               ['qualitative research 質性研究', 'quantitative research 量化研究', 'common sense 一般常識', 'an experiment 實驗'], 0, 'bsw'),
    'e4': exam('BSW 畢業考 · 4 / 5', 'A researcher starts with a theory, makes a hypothesis, and then tests it with data. Which logic is this?\n研究者從理論出發，提出假設，再用資料檢驗。這是哪一種邏輯？',
               ['inductive 歸納法', 'deductive 演繹法', 'intuition 直覺', 'tradition 傳統'], 1, 'bsw'),
    'e5': exam('BSW 畢業考 · 5 / 5', 'Which sentence is a **hypothesis**?\n哪一句是**研究假設**？',
               ['Older adults are very important. 長輩很重要。',
                'If older adults join a weekly exercise group, then they will fall less. 如果長輩參加每週運動團體，那麼他們會比較少跌倒。',
                'How are you today? 你今天好嗎？',
                'Falling down is sad. 跌倒很難過。'], 1, 'bsw'),
    # MSW final exam (one question per MSW book)
    'f1': exam('MSW 畢業考 · 1 / 5', 'What is the **first** step of a research study?\n研究的**第一步**是什麼？',
               ['collect data 蒐集資料', 'write the report 撰寫報告', 'choose a research question 選定研究問題', 'analyze data 分析資料'], 2, 'msw'),
    'f2': exam('MSW 畢業考 · 2 / 5', 'Ah-Zhe wants to know what is already known about preventing falls. Which source should he trust most?\n阿哲想知道「預防跌倒」已經有哪些研究。他最該相信哪一個來源？',
               ['a viral video by a famous athlete 名人運動員的爆紅影片', 'peer-reviewed studies and research reviews 經過同儕審查的研究與研究回顧',
                'what the neighbors have always done 鄰居一直以來的做法', 'his own feeling 他自己的感覺'], 1, 'msw'),
    'f3': exam('MSW 畢業考 · 3 / 5', 'Before an interview, Ah-Zhe explains the study, says it is voluntary, and asks Grandpa Chen if he agrees. This is…\n訪談前，阿哲說明研究目的、告訴陳阿公可以自由決定，再問他是否同意。這是……',
               ['informed consent 知情同意', 'halo effect 月暈效應', 'comparison group 比較組', 'output 產出'], 0, 'msw'),
    'f4': exam('MSW 畢業考 · 4 / 5', 'Evidence-based practice combines the best research evidence, the worker\'s professional expertise, and…\n實證為基礎的實務結合：最好的研究證據、社工的專業經驗，還有……',
               ['the client\'s values and preferences 案主的價值與偏好', 'the agency\'s budget only 只有機構的預算',
                'the worker\'s intuition alone 只有社工的直覺', 'what famous people say 名人怎麼說'], 0, 'msw'),
    'f5': exam('MSW 畢業考 · 5 / 5', 'Falls went down after an exercise group started. What makes us **more sure** the group caused the change?\n運動團體開始後，跌倒變少了。怎樣能讓我們**更確定**是團體造成的？',
               ['count how many sessions were held 算辦了幾次', 'ask the borough chief 問里長',
                'compare with a similar group that did not join 和沒參加的相似一群人比較', 'hold the group for longer 把團體辦久一點'], 2, 'msw'),
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
    'badCode': '密碼不對。請問老師。',
    'newTerm': '新名詞 ',
    'examSaved': '✎ 已作答。考完才會公布成績。 Answer recorded. Results at the end.',
    'endStats': '學士畢業考：考了 <b>{bswTries}</b> 次<br>碩士畢業考：考了 <b>{mswTries}</b> 次<br>筆記本：<b>{t} / {T}</b> 個名詞',
}

# ---------------------------------------------------------------- story
import story
SCRIPT = story.SCRIPT
data = {
    'id': 'family-next-door-v1', 'start': 'intro', 'player': 'me',
    'assets': {'town': '../../assets/tiles/tinytown.png', 'dungeon': '../../assets/tiles/tinydungeon.png',
               'chars': '../../assets/tiles/characters.png', 'extra': 'extra.png'},
    'chars': CHARS, 'legend': LEGEND, 'maps': MAPS, 'speakers': SPEAKERS, 'terms': TERMS, 'quizzes': QUIZZES, 'pauses': story.PAUSES,
    'jumps': story.JUMPS, 'hashJumps': {}, 'text': TEXT,
}

# ---------------------------------------------------------------- checks
for mid, m in MAPS.items():
    for did, d in m['doors'].items():
        if d.get('to'):
            assert walkable(MAPS[d['to']], d['tx'], d['ty']), f'{mid}/{did} lands on a wall'
LANE_STARTS = [(5, 5)]
lane_seen = reach(lane, 5, 5)
def adj(seen, x, y): return any((x + a, y + b) in seen for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
for did, d in lane['doors'].items(): assert adj(lane_seen, d['x'], d['y']), 'cannot reach door ' + did
labels = set(re.findall(r'^:: (\S+)', SCRIPT, re.M))
STARTS = {'lane': [(5, 5)], 'jay': [(5, 6)], 'chen': [(5, 6)], 'library': [(8, 10)], 'hall': [(7, 8)]}
# blocks that set up a scene: every person must stand on a free tile, and be reachable with all the others standing
for blk in re.split(r'^(?=:: )', SCRIPT, flags=re.M):
    puts = re.findall(r'^@put (\S+) (\S+) (\S+) (\d+) (\d+) (\S+)', blk, re.M)
    pos = {}
    for _id, spr, mp, x, y, lab in puts:
        x, y = int(x), int(y)
        assert mp in MAPS, mp
        assert walkable(MAPS[mp], x, y), f'@put {_id} on a blocked tile {mp} {x},{y}'
        assert lab == '-' or lab in labels, f'@put {_id}: unknown label {lab}'
        assert spr in CHARS or re.match(r'^[TDX]:\d+$', spr), spr
        pos[_id] = (mp, x, y)
    for _id, (mp, x, y) in pos.items():
        lab = [p for p in puts if p[0] == _id][-1][5]
        if lab == '-': continue
        blocked = frozenset((px, py) for i2, (m2, px, py) in pos.items() if m2 == mp and i2 != _id)
        seen = set()
        for s in STARTS[mp]: seen |= reach(MAPS[mp], *s, blocked)
        assert adj(seen, x, y), f'cannot walk up to {_id} on {mp} {x},{y} (block starting {blk[:30]!r})'
for m in re.finditer(r'^@(?:goto|label \S+) (\S+)', SCRIPT, re.M):
    assert m.group(1) == '-' or m.group(1) in labels, m.group(0)
for m in re.finditer(r'^@if \S+ (\S+)', SCRIPT, re.M): assert m.group(1) in labels, m.group(0)
for m in re.finditer(r'^@zone \S+ \S+ \d+ \d+ \d+ \d+ (\S+)', SCRIPT, re.M): assert m.group(1) in labels, m.group(0)
for m in re.finditer(r'-> (\S+)', SCRIPT): assert m.group(1) in labels, m.group(0)
for m in re.finditer(r'^@note (\S+)', SCRIPT, re.M): assert m.group(1) in TERMS, m.group(0)
for m in re.finditer(r'^@quiz (\S+)', SCRIPT, re.M): assert m.group(1) in QUIZZES, m.group(0)
for m in re.finditer(r'^@pause (\S+)', SCRIPT, re.M): assert m.group(1) in story.PAUSES, m.group(0)
ENGINE_SPEAKER = re.compile(r"^[A-Za-z][A-Za-z ./']*$")   # same rule as SPEAK in engine.js (no digits)
for m in re.finditer(r'^([^:\s>@?/][^:]*?)(?: \(VO\))?: ', SCRIPT, re.M):
    assert m.group(1) in SPEAKERS and ENGINE_SPEAKER.match(m.group(1)), m.group(1)
for k in SPEAKERS: assert ENGINE_SPEAKER.match(k), k
assert set(TERMS) == set(re.findall(r'^@note (\S+)', SCRIPT, re.M)), set(TERMS) ^ set(re.findall(r'^@note (\S+)', SCRIPT, re.M))
assert set(QUIZZES) == set(re.findall(r'^@quiz (\S+)', SCRIPT, re.M)), 'every exam question should be used'
for code, lab in story.JUMPS.items(): assert lab in labels, code
blob = json.dumps(data, ensure_ascii=False) + SCRIPT
for pat in (r'第\s*[0-9一二三四五六七八九十]+\s*[週章]', r'[Ww]eek\s*[0-9]', r'[Cc]hapter\s*[0-9]'):
    assert not re.search(pat, blob), f'week or chapter mentioned: {re.search(pat, blob).group(0)}'

js = ('/* 隔壁那一家 The Family Next Door — game data for the story-walk engine (../engine/engine.js).\n'
      ' * GENERATED by tools/build_data.py. Edit tools/story.py (story, pauses, codes) or build_data.py (maps, terms, exams) and run it again.\n'
      ' * Peace Lane, Hillside University and all their people are fictional.\n'
      ' * Art: Tiny Town + Tiny Dungeon by Kenney (www.kenney.nl), CC0 1.0; extra.png drawn for this site (CC0). */\n'
      'window.GAME = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n'
      'window.GAME.script = ' + json.dumps(SCRIPT, ensure_ascii=False) + ';\n')
OUT.write_text(js, encoding='utf-8')
print('wrote', OUT, len(js), 'bytes;', len(labels), 'labels,', len(TERMS), 'terms,', len(QUIZZES), 'exam questions')

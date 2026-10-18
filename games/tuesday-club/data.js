/* The Tuesday Club (星期二俱樂部) — chapter data for the story-walk engine (../engine/engine.js).
 * To make another chapter game: copy this folder, then change the maps, cast, terms, quizzes, pauses and script.
 * Art: Tiny Town + Tiny Dungeon by Kenney (www.kenney.nl), CC0 1.0. Characters recolored/redrawn for this game. */
window.GAME = {
  id: 'tuesday-club',
  start: 'prologue',
  player: 'old_rosa',
  assets: {
    town: '../../assets/tiles/tinytown.png',
    dungeon: '../../assets/tiles/tinydungeon.png',
    chars: '../../assets/tiles/characters.png'
  },
  // order of the 16x16 frames in characters.png
  chars: ['rosa', 'old_rosa', 'clara', 'addams', 'hannah', 'greta', 'sofia', 'miriam', 'bridget', 'mamma', 'old_woman', 'man', 'greco', 'tommaso', 'boy', 'neighbor', 'neighbor2'],

  /* ---------- tiles: [sheet, tile number, solid?] (sheets are 12 tiles wide) ---------- */
  legend: {
    ground: {
      '.': ['town', 0, 0], ',': ['town', 1, 0], '*': ['town', 2, 0], '#': ['town', 109, 0], '=': ['town', 40, 0],
      '-': ['town', 41, 0], 'o': ['town', 43, 0],
      'f': ['dungeon', 48, 0], 'k': ['dungeon', 0, 0], 'W': ['dungeon', 40, 1], 'V': ['dungeon', 28, 1], '+': ['dungeon', 42, 0]
    },
    obj: {
      T: ['town', 16, 1], U: ['town', 15, 1], O: ['town', 5, 1],
      // red roof / wood walls (Hull House, pharmacy roof)
      A: ['town', 52, 1], B: ['town', 53, 1], C: ['town', 54, 1], D: ['town', 55, 1], E: ['town', 64, 1], F: ['town', 65, 1], G: ['town', 66, 1], Y: ['town', 67, 1],
      L: ['town', 72, 1], M: ['town', 73, 1], R: ['town', 75, 1], N: ['town', 84, 1], P: ['town', 85, 1],
      // gray roof / stone walls (tenements)
      a: ['town', 48, 1], b: ['town', 49, 1], c: ['town', 50, 1], d: ['town', 51, 1], e: ['town', 60, 1], h: ['town', 61, 1], i: ['town', 62, 1], j: ['town', 63, 1],
      l: ['town', 76, 1], m: ['town', 77, 1], r: ['town', 79, 1], n: ['town', 88, 1], p: ['town', 89, 1],
      // fences and street things
      '(': ['town', 80, 1], '_': ['town', 81, 1], ')': ['town', 82, 1], '|': ['town', 59, 1],
      S: ['town', 83, 1], s: ['town', 57, 1], x: ['town', 130, 1], k: ['town', 107, 1], g: ['town', 106, 1],
      '@': ['dungeon', 66, 1], '&': ['dungeon', 67, 1],
      // indoors
      '1': ['dungeon', 72, 1], '2': ['dungeon', 73, 0], '3': ['dungeon', 63, 1], '4': ['dungeon', 75, 1], '9': ['dungeon', 45, 1], '0': ['dungeon', 67, 1]
    }
  },

  /* ---------- maps: ground layer + object layer, same size ---------- */
  maps: {
    street: {
      ground: [
        '..............................',
        '..............................',
        '..............................',
        '..............................',
        '..............................',
        '..,.....*.....o....*....,.....',
        '##############################',
        '==============================',
        '==============================',
        '##############################',
        '.......................-------',
        '.......................-------',
        '.......................-------',
        '.......................-------',
        '------------------------------',
        '.,......,......,.......-------',
        '..........*........,...-------',
        '......,................-------',
        '.......................-------',
        '..............................'
      ],
      obj: [
        'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
        'TabbdbcTTABBBBDBBBBCTTabbdbcTT',
        'TehhjhiTTEFFFFYFFFFGTTehhjhiTT',
        'Olnmnnr..LNMNMNMNMNR..lnmnnrO.',
        '.lmmpmr..LNMNMPMNMNR..lmmpmr..',
        'O........(__)...(__)s.......U.',
        '..............................',
        '..............................',
        '..............................',
        '..............................',
        '.abbdbc...xk&..ABBDBC.....k...',
        '.ehhjhi........EFFYFG...@...@.',
        '.lnmnnr........lnmnmrS....@...',
        '.lmmpmr........lnmpmr.........',
        '........................g...g.',
        'O.......U.....O..........@....',
        '...........................@..',
        '..T........O.....T............',
        '.......................(_____)',
        'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT'
      ],
      doors: {
        miriam: { x: 4, y: 4, locked: true, msg: '門鎖著。這是米莉安家住的公寓。' },
        hull: { x: 14, y: 4, to: 'hall', tx: 7, ty: 8, dir: 'up' },
        east: { x: 25, y: 4, locked: true, msg: '門鎖著。' },
        rosa: { x: 4, y: 13, to: 'home', tx: 5, ty: 6, dir: 'up' },
        pharm: { x: 18, y: 13, locked: true, msg: '藥房的門關著。招牌上寫著「藥房 Drugstore」。' }
      }
    },
    hall: {
      ground: [
        'WWWWWWWWWWWWWWW',
        'WWWWWWVWVWWWWWW',
        'WfffffffffffffW',
        'WfffffffffffffW',
        'WfffffffffffffW',
        'WfffffffffffffW',
        'WfffffffffffffW',
        'WfffffffffffffW',
        'WfffffffffffffW',
        'WWWWWWW+WWWWWWW'
      ],
      obj: [
        '...............',
        '...9.......9...',
        '.3...........4.',
        '...............',
        '..1.........1..',
        '.2.2.......2.2.',
        '...............',
        '...............',
        '...............',
        '...............'
      ],
      doors: {
        club: { x: 3, y: 1, to: 'club', tx: 6, ty: 7, dir: 'up' },
        office: { x: 11, y: 1, to: 'office', tx: 5, ty: 6, dir: 'up' },
        out: { x: 7, y: 9, to: 'street', tx: 14, ty: 5, dir: 'down' }
      }
    },
    club: {
      ground: [
        'WWWWWWWWWWWWW',
        'WWWVWWWWWVWWW',
        'WfffffffffffW',
        'WfffffffffffW',
        'WfffffffffffW',
        'WfffffffffffW',
        'WfffffffffffW',
        'WfffffffffffW',
        'WWWWWW+WWWWWW'
      ],
      obj: [
        '.............',
        '.............',
        '.3.........4.',
        '....2...2....',
        '......1......',
        '...2.....2...',
        '.....2.2.....',
        '.............',
        '.............'
      ],
      doors: { out: { x: 6, y: 8, to: 'hall', tx: 3, ty: 2, dir: 'down' } }
    },
    office: {
      ground: [
        'WWWWWWWWWWW',
        'WWWWWVWWWWW',
        'WfffffffffW',
        'WfffffffffW',
        'WfffffffffW',
        'WfffffffffW',
        'WfffffffffW',
        'WWWWW+WWWWW'
      ],
      obj: [
        '...........',
        '...........',
        '.3.......4.',
        '...1.......',
        '...........',
        '...........',
        '...........',
        '...........'
      ],
      doors: { out: { x: 5, y: 7, to: 'hall', tx: 11, ty: 2, dir: 'down' } }
    },
    home: {
      ground: [
        'WWWWWWWWWWW',
        'WWVWWWWWVWW',
        'WkkkkkkkkkW',
        'WkkkkkkkkkW',
        'WkkkkkkkkkW',
        'WkkkkkkkkkW',
        'WkkkkkkkkkW',
        'WWWWW+WWWWW'
      ],
      obj: [
        '...........',
        '...........',
        '.0.....3...',
        '......1....',
        '......2....',
        '...........',
        '...........',
        '...........'
      ],
      doors: { out: { x: 5, y: 7, to: 'street', tx: 4, ty: 14, dir: 'down' } }
    },
    apt35: {
      ground: [
        'WWWWWWWWW',
        'WWVWWWVWW',
        'WfffffffW',
        'WfffffffW',
        'WfffffffW',
        'WfffffffW',
        'WWWW+WWWW'
      ],
      obj: [
        '.........',
        '.........',
        '.3...1...',
        '.....2...',
        '.........',
        '.........',
        '.........'
      ],
      doors: { out: { x: 4, y: 6, to: 'street', tx: 4, ty: 14, dir: 'down' } }
    }
  },

  /* ---------- who talks (script name -> display name + portrait) ---------- */
  speakers: {
    'Rosa': { name: '蘿莎', sprite: 'rosa' },
    'Old Rosa': { name: '老蘿莎', sprite: 'old_rosa', vo: '老蘿莎（回憶）' },
    'Miss Clara': { name: '克萊拉小姐', sprite: 'clara' },
    'Jane Addams': { name: '珍·亞當斯', sprite: 'addams' },
    'Hannah': { name: '漢娜', sprite: 'hannah' },
    'Greta': { name: '葛蕾塔', sprite: 'greta' },
    'Sofia': { name: '蘇菲亞', sprite: 'sofia' },
    'Miriam': { name: '米莉安', sprite: 'miriam' },
    'Bridget': { name: '布莉姬', sprite: 'bridget' },
    'Tommaso': { name: '托馬索', sprite: 'tommaso' },
    'Mamma': { name: '媽媽', sprite: 'mamma' },
    'Neighbor boy': { name: '鄰居男孩', sprite: 'boy' },
    'Old Woman': { name: '門口的老太太', sprite: 'old_woman' },
    'Man in line': { name: '排隊的男人', sprite: 'man' },
    'Mr Greco': { name: '葛雷科先生', sprite: 'greco' },
    'Greta and Hannah': { name: '葛蕾塔、漢娜', sprite: 'greta' },
    'Everyone': { name: '大家', sprite: null }
  },

  /* ---------- notebook terms (in the order students meet them) ---------- */
  terms: {
    collectivity: { en: 'collectivity', zh: '集合體', def: '一群剛好在同一個地方的人，彼此沒有互動，也沒有共同目標。' },
    resident: { en: 'resident', zh: '駐館工作者', def: '住進睦鄰組織（例如 Hull House）、和鄰居一起生活的工作者。' },
    screening: { en: 'screening', zh: '篩選', def: '團體開始前，先和每個人個別談話，了解他的需要，看團體適不適合他。' },
    formed_group: { en: 'formed group', zh: '組成團體', def: '由工作者或機構刻意組織起來的團體（相對於自然形成的團體）。' },
    closed_group: { en: 'closed group', zh: '封閉式團體', def: '開始以後就不再接受新成員的團體，讓成員有時間建立信任。' },
    convening: { en: 'convening', zh: '聚集期', def: '團體剛開始，成員彼此陌生、很小心，觀察這裡安不安全。' },
    common_goal: { en: 'common goal', zh: '共同目標', def: '成員一起想達成的目標。這是團體的特徵之一。' },
    confidentiality: { en: 'confidentiality', zh: '保密', def: '在團體裡聽到的私人資訊，不帶到團體外面。' },
    interaction: { en: 'interaction', zh: '互動', def: '成員彼此說話、回應、互相影響。這也是團體的特徵之一。' },
    formation: { en: 'formation', zh: '形成期', def: '成員開始有自己的角色、規則和默契。' },
    identification: { en: 'identification', zh: '認同', def: '成員覺得「我屬於這個團體」。這也是團體的特徵之一。' },
    self_determination: { en: 'self-determination', zh: '自決', def: '成員有權利為自己和自己的團體做決定，工作者不替他們決定。' },
    homogeneity: { en: 'homogeneity', zh: '同質性', def: '成員之間相似的程度。太像，學不到新東西；差太多，又很難互相理解。' },
    conflict: { en: 'conflict', zh: '衝突期', def: '成員開始爭權、意見不合。這很正常，不代表團體失敗了。' },
    maintenance: { en: 'maintenance', zh: '維持期', def: '成員彼此信任，一起把事情做好，也互相支持。' },
    problem_solving: { en: 'problem-solving', zh: '問題解決', def: '團體一起找出問題的原因，並想辦法解決。' },
    social_action: { en: 'social action', zh: '社會行動', def: '一群人一起行動，改變造成問題的制度或政策。' },
    socialization: { en: 'socialization', zh: '社會化', def: '在團體中學會與人相處、表達自己、遵守共同的規範。' },
    termination: { en: 'termination', zh: '結束期', def: '團體結束，成員回顧、道別，把學到的帶走。' },
    social_goals_model: { en: 'social goals model', zh: '社會目標模式', def: '透過團體學習民主與公民責任、一起促成社會改變的團體工作模式（Papell & Rothman 歸納的三種模式之一）。' },
    enabler: { en: 'enabler', zh: '使能者', def: '社會目標模式中工作者的角色：不替成員做決定，而是幫助成員發現自己的力量。' }
  },

  /* ---------- chapter checks: Chinese question, English answers ---------- */
  quizzes: {
    q1: { tag: '第一章 · 小測驗 1/2', q: '在 Hull House 門口排隊報名的人，彼此不認識、也不交談。他們是：',
      options: ['a group', 'a collectivity', 'a committee', 'a family'], answer: 1, hint: '他們只是「剛好」站在一起。' },
    q2: { tag: '第一章 · 小測驗 2/2', q: '克萊拉小姐決定第二週以後不收新成員。這是哪一種團體？',
      options: ['open group', 'natural group', 'closed group', 'task group'], answer: 2, hint: '門是「關起來」的。' },
    q3: { tag: '第二章 · 小測驗 1/2', q: '俱樂部的成員開始爭吵、彼此懷疑、搶著當領導。這是團體發展的哪一個階段？',
      options: ['convening', 'formation', 'conflict', 'termination'], answer: 2, hint: '名字就是「衝突」。' },
    q4: { tag: '第二章 · 小測驗 2/2', q: '蘇菲亞在俱樂部裡說的秘密，蘿莎不應該隨便告訴別人。這是哪一個倫理原則？',
      options: ['screening', 'confidentiality', 'social action', 'homogeneity'], answer: 1, hint: '這是俱樂部的第三條規則。' },
    q5: { tag: '第三章 · 小測驗 1/2', q: '女孩們不只幫蘇菲亞一家，還一起連署，要求市政府改善收垃圾的制度。這是什麼？',
      options: ['casework', 'charity', 'social action', 'screening'], answer: 2, hint: '一群人一起「行動」，改變社會。' },
    q6: { tag: '第三章 · 小測驗 2/2', q: '最後一次聚會，成員回顧學到的東西、互相道別。這是哪一個階段？',
      options: ['convening', 'conflict', 'maintenance', 'termination'], answer: 3, hint: '團體「結束」的階段。' }
  },

  /* ---------- classroom pauses (the code is shown on the teacher's slide) ---------- */
  pauses: {
    p1: {
      code: 'CONVENE',
      html: `<p>Put your phones down. 你們四個人現在也是一個團體。請一起完成：</p>
        <ol><li>幫你們的小組取一個名字（英文或中文都可以）。</li>
        <li>寫下今天的一個 <b>common goal</b>（共同目標）。</li>
        <li>寫下兩條小組規則。</li></ol>
        <p class="small">等老師公布密碼後，輸入密碼繼續。 Enter the code from the slide to continue.</p>`
    },
    p2: {
      code: 'CONFLICT', var: 'choice2',
      html: `<p>Put your phones down. 先看看每個人知道什麼：</p>
        <ul class="recap">
        <li><b>蘿莎</b>：蘇菲亞偷偷說，錢是她拿的，因為媽媽生病要買藥。她求蘿莎不要說出去。</li>
        <li><b>漢娜</b>：去年在工廠，布莉姬也被冤枉偷錢，後來發現是工頭說謊。</li>
        <li><b>葛蕾塔</b>：錢不見的那天，她看到布莉姬站在錢盒旁邊。</li>
        <li><b>克萊拉小姐</b>：大家約好這是 closed group，第二週以後不收新人；可是布莉姬晚上沒有地方可去。</li></ul>
        <ol><li>四個人一起討論：<b>克萊拉小姐應該怎麼做？</b>選一個答案。</li>
        <li>準備一個理由。老師會請每組舉手。</li></ol>`,
      choices: ['A. 請布莉姬離開，讓大家冷靜下來。', 'B. 請蘿莎當場說出她知道的事。',
        'C. 克萊拉小姐私下找蘇菲亞談，讓蘇菲亞自己決定要不要告訴大家。', 'D. 暫停演戲計畫，把錢的事交給亞當斯小姐處理。']
    },
    pick3: {
      head: '你們在第二次暫停時選了哪一個？',
      var: 'choice2',
      html: '<p class="small">Which answer did your group choose at Pause 2?</p>',
      choices: ['A. 請布莉姬離開', 'B. 蘿莎說出來', 'C. 克萊拉小姐私下找蘇菲亞', 'D. 交給亞當斯小姐']
    },
    p3: {
      code: 'GOODBYE', unlockAfter: 120,
      html: `<p>Put your phones down. 你們的小組今天也要結束了。</p>
        <ol><li>輪流對組裡的一位同學說一句話：謝謝他／她、今天印象最深的一刻，或你學到的一件事（英文或中文都可以）。</li>
        <li>說完以後，再一起看結局。</li></ol>`
    }
  },
  jumps: { CONVENE: 'ch2', CONFLICT: 'jump3', GOODBYE: 'epilogue' },
  hashJumps: { prologue: 'prologue', ch1: 'ch1', ch2: 'ch2', ch3: 'jump3', epilogue: 'epilogue' },

  text: {
    locked: '門鎖著。',
    idle: '走到人或東西旁邊，按 A 說話。頭上有 ! 的地方有新的事。',
    choose: '你會怎麼說？',
    right: '答對了！',
    hintLead: '再想想：',
    pauseHead: '⏸ 暫停！放下手機。',
    waitFor: '{s} 後可以按「繼續」，或輸入老師的密碼。',
    pickFirst: '請先選一個答案（A–D）。',
    badCode: '密碼不對。請看投影片上的密碼。',
    newTerm: '新名詞 ',
    endStats: '第一次就答對：<b>{f} / {n}</b> 題<br>筆記本：<b>{t} / {T}</b> 個名詞'
  },

  /* ================================ SCRIPT ================================ */
  script: `
:: prologue
@save
@clear
@tint sepia
@music quiet
@player old_rosa
@title 芝加哥，1935 年 5 月|Chicago, May 1935
@door street/rosa apt35 4 5
@put paper D:66 apt35 5 2 p_paper !
@put boy boy street 6 14 p_boy !
@put fl1 T:2 street 13 5 -
@put fl2 T:2 street 15 5 -
@put oldwoman old_woman hall 7 6 p_oldwoman !
@put box D:89 club 10 2 p_box_early
@map apt35 4 4 up
@goal 看看桌上的報紙。

:: p_paper
@label paper -
> 報紙上寫著：「珍·亞當斯逝世，享年七十四歲。」
Old Rosa: ……
Old Rosa: 亞當斯小姐。
Old Rosa: 四十多年了。我以為我早就準備好聽到這個消息。
@goal 走出門，到對面的 Hull House（紅色屋頂的大房子）。

:: p_boy
@label boy p_boy2 -
Neighbor boy: 蘿莎老師！你今天不用去醫院帶團體嗎？
Old Rosa: 今天不用。今天……我要回 Hull House 一趟。
Neighbor boy: 那棟紅磚大房子？聽說好多人都去那裡獻花。

:: p_boy2
Neighbor boy: 門口有好多花喔。

:: p_oldwoman
@label oldwoman p_oldwoman2 -
Old Woman: 你也是這裡長大的孩子吧？去吧，房間都開著。
@label box p_box !
@goal 走進以前的俱樂部房間（大廳左上的門）。

:: p_oldwoman2
Old Woman: 慢慢看。今天大家都想回來看看。

:: p_box_early
Old Rosa: 一個舊箱子。……先跟門口的老太太打聲招呼吧。

:: p_box
@label box -
Old Rosa: 這個箱子……還在？
@item 舊筆記本 The Club Notebook
> 封面寫著：「星期二俱樂部 — 記錄員：蘿莎」
Old Rosa: 是我的字。歪歪扭扭的，那時候我連英文都寫不好。
Old Rosa: 第一頁……1890 年代的某個秋天。那天，我差點沒有走進這扇門。
@goto ch1

// ======================= CHAPTER 1 =======================
:: ch1
@save
@clear
@tint none
@music warm
@player rosa
@title 第一章：第一次聚會|Chapter 1 · The First Meeting
@door street/hull lock 門口排了好長的隊。先問問排隊的人吧。
@put mamma mamma home 2 3 c1_mamma_wait
@put tommaso tommaso home 7 5 c1_tommaso
@put basket T:130 home 3 5 c1_basket
@put man man street 15 6 c1_line !
@put n1 neighbor street 16 6 c1_crowd
@put n2 neighbor2 street 17 6 c1_crowd
@map home 5 5 up
@goal
Mamma: 蘿莎，這些袖子今天要縫完。工頭明天早上來拿。
Rosa: 媽……對面那棟紅磚房子，今天晚上有女孩的聚會。我可以去嗎？
Mamma: 去做什麼？喝茶、聊天？我們沒有時間聊天。
Rosa: 他們會教英文。如果我會說英文，就可以幫你跟工頭談價錢。
Tommaso: 姊姊想去談戀愛！
Rosa: 才沒有！
Mamma: ……縫完十二雙袖子，就可以去。一雙都不能少。
@label basket c1_basket !
@goal 到針線籃（水桶旁）縫完十二雙袖子。

:: c1_mamma_wait
Mamma: 袖子還沒縫完，哪裡都不能去。

:: c1_mamma_after
Mamma: 九點以前回來。記得。

:: c1_tommaso
Tommaso: 姊姊，Hull House 真的有餅乾嗎？

:: c1_basket
@label basket -
> 你坐下來，一針一針地縫。
> 四雙……八雙……十二雙。
@item 十二雙袖子縫好了
@label mamma c1_mamma_after
Mamma: ……好。去吧。九點以前回來。
Tommaso: 幫我看看那裡有沒有餅乾！
@goal 走出門，到對面的 Hull House（紅色屋頂）。

:: c1_crowd
> 他們在排隊，好像不太想聊天。

:: c1_line
@label man c1_line2 -
Man in line: 小姑娘，別插隊。我們都在等報名夜間英文班。
Rosa: 你們都是一起的嗎？
Man in line: 一起？哈！我連前面那個人叫什麼都不知道。我們只是剛好站在同一個地方。
@note collectivity
@put clara clara street 13 5 -
Miss Clara: （從門裡探出頭）你是來參加女孩聚會的嗎？從側門進來就好，不用排隊。
@del clara
@door street/hull reset
@put clara clara office 6 3 c1_clara !
@put note D:66 office 3 3 c1_note !
@goal 進 Hull House，到克萊拉小姐的辦公室（大廳右上的門）。

:: c1_line2
Man in line: 我還要排很久呢。

:: c1_note
@label note c1_note2 -
> 桌上有一張克萊拉小姐的計畫筆記：
> 「女孩俱樂部：8 人左右，13–16 歲。每週二晚上七點，共十二週。」
> 「第二週以後不收新成員（closed group）。先個別談話，再決定。」

:: c1_note2
> 「8 人左右……每週二……共十二週。」

:: c1_clara
@label clara c1_clara_wait
Miss Clara: 坐吧。我是克萊拉，住在這裡的 **resident**（駐館工作者）。在你加入之前，我想先跟你聊聊。
@note resident
Rosa: 這是考試嗎？
Miss Clara: （笑）不是。我只是想知道你為什麼想來，以及這個團體適不適合你。我們叫它 **screening**（篩選）。
@note screening
Miss Clara: 你為什麼想來？
@choice
? 我想學英文。
? 我想交朋友。
? ……我也不知道。
Miss Clara: 很好的理由。這個俱樂部是我們刻意組起來的，是一個 **formed group**（組成團體），不是街上自己湊在一起的那種。
@note formed_group
Miss Clara: 我們只收大約八個人。太少，聊不起來；太多，害羞的人就永遠不敢開口。
Miss Clara: 而且第二週以後就不收新人了。這叫 **closed group**（封閉式團體）。大家要有時間慢慢信任彼此。
@note closed_group
Rosa: 那……我可以加入嗎？
Miss Clara: 可以。不過我需要你幫一個忙。有三個女孩還沒拿到邀請卡。你可以幫我送去嗎？
@item 三張邀請卡
@set invites 0
@put hannah hannah street 22 6 c1_hannah !
@put sofia sofia street 13 10 c1_sofia !
@put miriam miriam street 4 5 c1_miriam !
@goal 把邀請卡送給漢娜、蘇菲亞、米莉安（0/3）。她們都在街上。

:: c1_clara_wait
Miss Clara: 邀請卡送完了嗎？漢娜在街的東邊，蘇菲亞在水果攤，米莉安在西邊的公寓門口。

:: c1_hannah
@label hannah c1_hannah2
Hannah: 俱樂部？我一天縫十二個小時的衣服，晚上只想睡覺。
Rosa: 克萊拉小姐說，會有熱咖啡。
Hannah: ……熱咖啡？好吧。但我先說好，如果很無聊我就走。
@goto c1_invite

:: c1_hannah2
Hannah: 星期二，我記得了。有熱咖啡。

:: c1_sofia
@label sofia c1_sofia2
> 蘇菲亞站在水果攤旁邊，低著頭，什麼也沒說。
Rosa: 這是給你的。星期二晚上，我也會去。
Sofia: ……（小聲）我英文不好。
Rosa: 我也是。我們可以一起不好。
> 蘇菲亞第一次抬起頭，微微笑了一下。
@goto c1_invite

:: c1_sofia2
Sofia: ……星期二。（點點頭）

:: c1_miriam
@label miriam c1_miriam2
Miriam: 邀請卡？哇，我這輩子第一次收到邀請卡！要穿禮服嗎？我只有這一件衣服。
Rosa: 穿你現在這件就好。
Miriam: 太好了，反正我也沒有別件。
@goto c1_invite

:: c1_miriam2
Miriam: 我正在想星期二要講什麼笑話。

:: c1_invite
@inc invites
@goal 把邀請卡送給漢娜、蘇菲亞、米莉安（{invites}/3）。
@if invites>=3 c1_invites_done

:: c1_invites_done
> 星期二到了。
@del hannah
@del sofia
@del miriam
@del clara
@del note
@put greta greta club 8 3 -
@put hannah hannah club 9 5 -
@put miriam miriam club 3 5 -
@put sofia sofia club 5 6 -
@put clara clara club 6 2 -
@zone meet1 club 0 0 13 9 c1_meeting
@goal 星期二晚上七點。到 Hull House 的俱樂部房間（大廳左上的門）。

:: c1_meeting
@unzone meet1
@music tick
@pos 7 6 up
Greta: 你們就是其他人？我是葛蕾塔。我本來以為會有更多人。
> ……
> ……
> ……
Old Rosa (VO): 第一次聚會，沒有人知道該說什麼。每個人都在偷看別人，猜自己能不能在這裡安全地做自己。
@note convening
@music warm
Miss Clara: 我們來做一件簡單的事。每個人說自己的名字，還有一樣你家鄉的東西。
Greta: 葛蕾塔。德國。麵包。很硬的麵包。
Hannah: 漢娜。波蘭。……我媽媽唱的歌。
Miriam: 米莉安。俄國。冬天。相信我，你們不會想要的。
> 大家都笑了。連蘇菲亞都摀著嘴。
Rosa: 蘿莎。義大利。海。……我好久沒看到海了。
Sofia: ……蘇菲亞。希臘。橄欖樹。
Miss Clara: 謝謝大家。現在，這個俱樂部要做什麼？不是我決定，是你們決定。
Greta: 我們來演戲！聖誕節演給整條街的人看！
Hannah: 服裝要錢。我們沒有錢。
Miriam: 那我們就先賺錢，再演戲。我可以賣笑話，一個一分錢。
Miss Clara: 所以你們的 **common goal**（共同目標）是：籌錢做服裝，聖誕節演一齣戲。對嗎？
Everyone: 對！
@note common_goal
Miss Clara: 那我們需要規則。你們想要什麼規則？
Hannah: 一：錢放在鐵盒子裡，大家一起數。
Sofia: （很小聲）……二：每個人都可以說話。不可以笑別人的英文。
Rosa: 三：在俱樂部裡說的秘密，就留在俱樂部裡。
Miss Clara: 第三條很重要。這叫 **confidentiality**（保密）。記住了。
@note confidentiality
Miriam: 還缺一個名字！我們星期二聚會，就叫「星期二俱樂部」。
Greta: 這是世界上最懶的名字。
Miriam: 所以才好記啊。
Old Rosa (VO): 那天晚上，我們說的話比任何一天都多。你說一句，我回一句，彼此影響。後來我才知道，這叫 **interaction**（互動）。
@note interaction
@title 第二週|Week 2
Greta: 我來當導演。沒有人反對吧？……很好。
@title 第三週|Week 3
Hannah: 鐵盒子裡現在有一塊二毛。米莉安，你的笑話只賺了三分錢。
Miriam: 品質比數量重要。
@title 第四週|Week 4
Miss Clara: 蘿莎，你聽得最仔細。這本筆記本給你，你來當我們的記錄員。
@item 新筆記本（就是 1935 年的那一本）
Old Rosa (VO): 每個人都有了自己的位置。我們開始對別人說「我是星期二俱樂部的」。那是我第一次覺得，我屬於某個地方。
@note formation
@note identification
@goal
@quiz q1
@quiz q2
@pause p1
@goto ch2

// ======================= CHAPTER 2 =======================
:: ch2
@save
@clear
@tint none
@music warm
@player rosa
@title 第二章：鐵盒子|Chapter 2 · The Tin Box
@put greta greta club 8 3 -
@put hannah hannah club 9 5 -
@put miriam miriam club 3 5 -
@put sofia sofia club 5 6 -
@put clara clara club 6 2 -
@put tin D:101 club 10 2 -
@map club 7 6 up
@goal
Old Rosa (VO): 第六週的時候，一切都太順利了。順利到我們忘了，團體不會永遠這麼平靜。
> 叩、叩。有人敲門。
@put bridget bridget club 6 7 -
Bridget: 這裡……是女孩的俱樂部嗎？我叫布莉姬。我在洗衣房工作。我想加入。
Greta: 我們已經滿了。克萊拉小姐說過，第二週以後就不收新人。
Bridget: 我晚上沒有地方可以去。房東把燈關了，我只能坐在樓梯上。
Miriam: （小聲對蘿莎）她是愛爾蘭人。我哥哥說愛爾蘭人很愛打架。
Hannah: 米莉安，你哥哥也說過月亮是起司做的。
Hannah: （看著布莉姬，皺眉）……我好像在哪裡見過你。
Miss Clara: 布莉姬，謝謝你來。這不是我一個人能決定的事。下週二，請大家一起決定。
@move bridget 10 3
> 布莉姬走出去之前，在放鐵盒子的架子旁邊停了一下，看了看那些服裝。
@move bridget 6 7
@del bridget
Greta: 你們看到了嗎？她一直盯著錢盒子。
> 這一週，你在街上走了很多次。
@del hannah
@del miriam
@del sofia
@del clara
@label greta c2_greta !
@put addams addams hall 9 4 c2_hall !
@put clara clara hall 10 4 c2_hall !
@put hannah hannah street 20 6 c2_hannah !
@put miriam miriam street 4 5 c2_miriam
@put sofia sofia street 19 14 c2_sofia !
@goal 這個星期在附近走走，聽聽大家怎麼說。一定要找到蘇菲亞（藥房附近）。

:: c2_hall
@label addams -
@label clara -
> 你經過大廳，聽到亞當斯小姐和克萊拉小姐在說話。
Jane Addams: 克萊拉，那個洗衣房的女孩，晚上真的沒有地方去。
Miss Clara: 我知道。可是女孩們約好了這是 closed group。如果我自己說「讓她進來」，那這還是她們的俱樂部嗎？
Jane Addams: 那就讓她們自己想清楚。你的工作不是替她們決定，是幫她們能夠好好決定。
@note self_determination
> 你悄悄走開，沒有被發現。

:: c2_hannah
@label hannah c2_hannah2
Hannah: 我想起來了。去年在工廠，有人掉了錢，工頭說是布莉姬偷的。她被罵了一整天。
Rosa: 是她嗎？
Hannah: 不是。後來發現是工頭自己拿的。可是沒有人跟她道歉。

:: c2_hannah2
Hannah: 沒有證據，就不能說是誰。

:: c2_greta
@label greta c2_greta2
Greta: 蘿莎，你過來看。上週我們有一塊五毛，現在只剩一塊。少了五毛錢。
Greta: 布莉姬來的那天，我親眼看到她站在錢盒旁邊。不是她，還會是誰？

:: c2_greta2
Greta: 我一定要在星期二說出來。

:: c2_miriam
Miriam: 我在練新笑話，可是大家最近都笑不出來。

:: c2_sofia
@label sofia -
> 蘇菲亞站在藥房門口，手裡握著一個咖啡色的小瓶子，在哭。
Rosa: 蘇菲亞？你怎麼了？
Sofia: ……蘿莎。不要生氣，好嗎？
Sofia: 我媽媽發燒三天了。巷子裡的垃圾都沒有人收，好多小孩也生病了。醫生說要買這個藥。
Sofia: 我們家一毛錢都沒有了。所以我……從鐵盒子裡拿了五毛錢。
Rosa: ……
Sofia: 我會還的！我發誓我會還！可是求求你，不要告訴大家。葛蕾塔會恨我，大家都會覺得我是小偷。
Sofia: 你說過的。在俱樂部裡說的秘密，就留在俱樂部裡。
Old Rosa (VO): 那天晚上我睡不著。保守秘密，布莉姬會被冤枉。說出秘密，蘇菲亞會失去所有朋友。
@del sofia
@zone meet2 club 0 0 13 9 c2_meeting
@goal 星期二到了。回到俱樂部房間（還可以先找其他人聊聊）。

:: c2_meeting
@unzone meet2
@music stop
@goal
@put greta greta club 8 3 -
@put hannah hannah club 9 5 -
@put miriam miriam club 3 5 -
@put sofia sofia club 5 6 -
@put clara clara club 6 2 -
@put bridget bridget club 4 3 -
@pos 7 6 up
Greta: 在決定讓不讓布莉姬加入之前，我要先說：錢盒少了五毛錢。
Bridget: ……又來了。每個地方都一樣。只要少了東西，就是愛爾蘭人拿的。
Greta: 我又沒說是你！……可是你那天確實站在錢盒旁邊。
Hannah: 葛蕾塔，你沒有證據。你知道被冤枉是什麼感覺嗎？
Greta: 那你知道我縫了多少個晚上才賺到那些錢嗎？
Miriam: 呃……要不要聽個笑話？
Greta and Hannah: 不要！
Greta: 她跟我們不一樣。她年紀比較大，她不是我們這條街的人。她會毀掉這個俱樂部。
Miss Clara: 成員之間太像，大家就學不到新東西；差太多，又很難互相理解。這是團體的 **homogeneity**（同質性）問題。你們覺得布莉姬是「太不一樣」，還是「剛好不一樣」？
@note homogeneity
> 沒有人回答。蘇菲亞盯著地板。
Greta: 蘿莎，你是記錄員。你什麼都看得到。你一定知道錢去哪裡了。
> 所有人都轉過頭來看你。
Rosa: 我……
Old Rosa (VO): 那是我們第一次真正的吵架。後來我才知道，每個團體都會走到這一步。
@note conflict
Miss Clara: （轉向你）如果你是我，你會怎麼做？
@quiz q3
@quiz q4
@pause p2
@goto ch3

// ======================= CHAPTER 3 =======================
:: jump3
@pause pick3
@goto ch3

:: ch3
@save
@clear
@tint none
@music quiet
@player rosa
@title 第三章：最後一個星期二|Chapter 3 · The Last Tuesday
@put greta greta club 8 3 -
@put hannah hannah club 9 5 -
@put miriam miriam club 3 5 -
@put sofia sofia club 5 6 -
@put clara clara club 6 2 -
@put tin D:101 club 10 2 -
@map club 7 6 up
@goal
@if choice2=A c3_a
@if choice2=B c3_b
@if choice2=D c3_d
@goto c3_c

:: c3_a
Hannah: 你們就這樣讓她走了？
@move hannah 6 7
@del hannah
> 漢娜追了出去。
Old Rosa (VO): 布莉姬走了。俱樂部變得很安靜，可是那不是平靜，是每個人都不敢說話。
@title 一週後|One week later
@put hannah hannah club 9 5 -
Sofia: （站起來，聲音發抖）……錢是我拿的。不是布莉姬。我們要去跟她道歉。
> 那天晚上，大家一起去洗衣房找布莉姬，把她請了回來。
@goto c3_join

:: c3_b
@put bridget bridget club 4 3 -
Rosa: ……是蘇菲亞拿的。她媽媽生病了。
> 蘇菲亞臉色發白，跑出房間。
@move sofia 6 7
@del sofia
Miss Clara: （之後，私下對你）說真話沒有錯。可是那是蘇菲亞的故事，應該由她自己決定要不要說。
> 你在巷口找到蘇菲亞。
Rosa: 對不起。我破壞了我們的第三條規則。
Sofia: ……我也破壞了第一條。我們一起回去吧。
@goto c3_join

:: c3_c
@put bridget bridget club 4 3 -
@move clara 6 7
@move sofia 5 7
Miss Clara: （在走廊，對蘇菲亞小聲說）我不會替你說。你想怎麼做，我陪你。
Sofia: 如果我說了，她們還會要我嗎？
Miss Clara: 我不知道。可是我知道，一個團體可以承受的，往往比我們以為的多。
@title 下週二|Next Tuesday
@put clara clara club 6 2 -
@put sofia sofia club 5 6 -
Sofia: （站起來）……我有話要跟大家說。
@goto c3_join

:: c3_d
@put bridget bridget club 4 3 -
@put addams addams club 6 7 -
Jane Addams: 克萊拉把這件事交給我？不行。這是你們的俱樂部，不是我的。
Greta: 可是我們解決不了！
Jane Addams: 你們還沒試過一起解決。去吧，我在樓下等你們的消息。
@move addams 6 8
@del addams
Sofia: （深呼吸）……我有話要跟大家說。
@goto c3_join

:: c3_join
@put greta greta club 8 3 -
@put hannah hannah club 9 5 -
@put miriam miriam club 3 5 -
@put sofia sofia club 5 6 -
@put clara clara club 6 2 -
@put bridget bridget club 4 3 -
@pos 7 6 up
Sofia: 錢是我拿的。我媽媽發燒，醫生說要買藥。我很害怕，我不知道還能找誰。
> ……
> ……
> ……
Greta: ……你為什麼不跟我們說？
Sofia: 因為你一定會生氣。
Greta: 我是會生氣。（停頓）可是我更氣的是，你覺得你只能一個人扛。
Greta: （轉向布莉姬，很不情願）布莉姬……對不起。我錯怪你了。
Bridget: 嗯。你是第一個跟我道歉的人。
Miriam: 那我可以說笑話了嗎？
Everyone: （終於笑出來）說吧！
Miss Clara: 那布莉姬的事呢？我們說好是 closed group。現在要不要改，由你們決定。
> 大家一個一個舉起手。葛蕾塔最後一個。
@music warm
Hannah: 等一下。蘇菲亞的媽媽為什麼會生病？
Sofia: 巷子的垃圾。好幾個星期沒人收了。隔壁的小孩也在發燒。
Hannah: 那我們幫完蘇菲亞一家，下一個生病的又是誰家？
Miss Clara: 這是個好問題。你們想怎麼做？
Bridget: 我可以幫蘇菲亞家免費洗衣服。
Miriam: 我把這個月賣笑話的錢都捐出來。一共七分錢。
Greta: 亞當斯小姐正在收集大家的連署，要去市政府抗議垃圾的事。我們也去！
Old Rosa (VO): 我們開始一起想辦法，也一起把事情做好。那是我們吵得最兇的一個月，也是從那時候開始，我們才真的變成一個團體。
@note maintenance
@note problem_solving
@note social_action
@item 連署書 Petition
@set sigs 0
@put greco greco street 26 13 c3_greco !
@put man man street 20 6 c3_man !
@put tommaso tommaso street 6 15 c3_tommaso !
@put mamma mamma home 2 3 c3_mamma !
@put addams addams hall 7 4 c3_addams_wait
@goal 收集四個連署簽名（0/4）：巷子、街上、家裡都找找看。

:: c3_greco
@label greco c3_greco2
Mr Greco: 連署？簽了有什麼用！市政府從來不管我們這一區。
Rosa: 一個人說沒有用。可是如果整條街一起說呢？
Mr Greco: ……哼。拿來。我簽大一點，讓他們看清楚。
@goto c3_sig

:: c3_greco2
Mr Greco: 簽了就簽了。垃圾最好真的有人來收。

:: c3_man
@label man c3_man2
Man in line: 是你！上次排隊的那個小姑娘。我現在在上夜間英文班了。
Man in line: 我上個月還不會寫字。現在我會寫自己的名字了。讓我簽。
@goto c3_sig

:: c3_man2
Man in line: 下一課要學寫地址呢。

:: c3_tommaso
@label tommaso c3_tommaso2
Tommaso: 我也要簽！我也會寫名字！……雖然 M 是反的。
@goto c3_sig

:: c3_tommaso2
Tommaso: 我的 M 很好看吧？

:: c3_mamma
@label mamma c3_mamma2
Mamma: （在窗邊縫衣服）這是什麼？
Rosa: 媽，這是為了巷子的垃圾。蘇菲亞的媽媽就是因為那樣生病的。
Mamma: （看了很久）……你在那個俱樂部，學會跟大人講道理了。
> 媽媽簽下了她的名字。
@goto c3_sig

:: c3_mamma2
Mamma: 去吧。九點以前回來。

:: c3_sig
@inc sigs
@goal 收集四個連署簽名（{sigs}/4）。
@if sigs>=4 c3_sigs_done

:: c3_sigs_done
@label addams c3_addams !
@goal 把連署書交給亞當斯小姐（Hull House 大廳）。

:: c3_addams_wait
Jane Addams: 連署書收齊了嗎？每一個名字都很重要。

:: c3_addams
@label addams -
Jane Addams: 四十幾個名字。很好。明天我會帶著它去市政府。你們幾個女孩，願意一起去嗎？
Rosa: 願意！
@goal
@title 聖誕節|Christmas
@clear
@music bright
@put greta greta hall 5 3 -
@put hannah hannah hall 6 3 -
@put bridget bridget hall 8 3 -
@put sofia sofia hall 9 3 -
@put miriam miriam hall 10 3 -
@put mamma mamma hall 5 6 -
@put tommaso tommaso hall 6 6 -
@put mother old_woman hall 7 6 -
@put man man hall 8 6 -
@put greco greco hall 9 6 -
@put addams addams hall 10 6 -
@put clara clara hall 4 6 -
@map hall 7 3 down
Old Rosa (VO): 那年聖誕節，我們真的演了那齣戲。葛蕾塔當導演，罵了每一個人。漢娜管錢，一分都沒少。布莉姬演國王，因為她最高。
Old Rosa (VO): 蘇菲亞的媽媽病好了，坐在第一排。蘇菲亞說了一句台詞。只有一句。可是整個大廳的人都聽見了。
Sofia: 「我們不是一個人！」
> 掌聲。
@title 第十二週|Week 12
@clear
@music quiet
@put greta greta club 8 3 -
@put hannah hannah club 9 5 -
@put miriam miriam club 3 5 -
@put sofia sofia club 5 6 -
@put clara clara club 6 2 -
@put bridget bridget club 4 3 -
@map club 7 6 up
Miss Clara: 今天是我們最後一次聚會。結束很難，所以我想好好地結束。
Miss Clara: 每個人說一件你在這裡學到的事，還有一件你要帶走的東西。
Greta: 我學會……閉嘴聽別人說話。有時候。
Hannah: 我學會，不用什麼都自己扛。我要帶走蘇菲亞畫的海報。
Bridget: 我第一次有一個地方，晚上可以去。我要帶走……你們的名字。我會記得。
Miriam: 我學會一個笑話：七個女孩走進 Hull House，出來的時候，變成了一家人。……好吧，這不好笑。可是是真的。
Sofia: 我學會在很多人面前說話。（停頓）我要帶走蘿莎說的那句話：「我們可以一起不好。」
Miss Clara: 蘿莎，你呢？
@choice
? 我學會了聽。
? 我學會了保守秘密，也學會了什麼時候不該替別人說。
? 我學會了，我屬於這裡。
@note socialization
Miss Clara: 謝謝你們。這個俱樂部會結束，但你們學到的不會。
Miss Clara: 蘿莎，你是記錄員。最後一頁，由你來寫。
> 你在最後一頁寫下：「星期二俱樂部，最後一天。我們吵過架，也和好了。我們不是一個人。」
@note termination
@quiz q5
@quiz q6
@pause p3
@goto epilogue

// ======================= EPILOGUE =======================
:: epilogue
@save
@clear
@tint sepia
@music quiet
@player old_rosa
@title 1935 年 5 月|May 1935
@put box D:89 club 10 2 -
@map club 10 3 up
@goal
Old Rosa: 「我們不是一個人。」……十四歲的我，寫得還不錯。
> 一張摺起來的紙從封底滑了出來。是另一個人的筆跡。
Old Rosa: 這是……克萊拉小姐的字。
> 「蘿莎：這十二週，我幾乎沒有替你們做過任何決定。這不是我偷懶。我的工作，是讓你們發現自己做得到。——克萊拉」
Old Rosa: 那時候我不懂。我以為她什麼都沒做。
Old Rosa: 現在我自己在醫院帶團體了，才知道「不替別人做決定」有多難。
Old Rosa: 後來的學者把克萊拉小姐那種做法叫做 **social goals model**（社會目標模式）：透過團體學習民主、承擔公民責任、一起改變社會。
@note social_goals_model
Old Rosa: 而她的角色，叫做 **enabler**（使能者）。不是英雄，是幫別人變成自己的英雄的人。
@note enabler
> 你把筆記本放回箱子裡，輕輕蓋上。
Old Rosa: 謝謝你，亞當斯小姐。謝謝你，克萊拉小姐。
Old Rosa: 明天是星期二。我的團體在等我。
@end
`
};

"""Story script, pauses and jump codes for 隔壁那一家 The Family Next Door. build_data.py imports this file.
Edit here, then run: python3 tools/build_data.py

Jump codes (type on the title screen if a student changes device):
  LIBRARY    -> the library, before the bachelor's (BSW) exam
  MASTER     -> after the BSW, before the master's (MSW) exam
  HOMECOMING -> back on Peace Lane as a social worker
"""

JUMPS = {'LIBRARY': 'lib', 'MASTER': 'msw', 'HOMECOMING': 'sw'}

PAUSES = {
    'talk1': {
        'head': '💬 討論時間 Discussion', 'ready': True, 'go': '繼續 Continue',
        'html': '''<p><b>阿哲試了六個辦法，為什麼每一個都失敗了？你自己最常用哪一種「沒有查證」的方法來做決定？</b></p>
<p class="en">Ah-Zhe tried six ideas. Why did each one fail? Which unchecked way of knowing do you use most often?</p>
<p class="small">和旁邊的同學討論，再按「繼續」。 Talk with the classmate next to you, then tap Continue.</p>'''},
    'oops': {
        'head': ' ', 'over': True, 'ready': True, 'go': '再試一次 Try again',
        'html': '''<div class="gameover">GUESSING AGAIN</div>
<p>又在猜了！這不是研究。</p>
<p class="en">That is a guess, not research.</p>
<p class="small">回到這一步，再選一次。 Go back and choose again.</p>'''},
    'final': {
        'head': '💬 最後討論 Final Discussion', 'ready': True, 'go': '看結局 Finish',
        'html': '''<p><b>想一想你的社區、宿舍或校園裡的一個問題。在動手解決之前，你會問什麼研究問題？你會蒐集哪些資料？</b></p>
<p class="en">Think of one problem in your neighborhood, dorm or campus. Before you try to fix it, what research question would you ask? What data would you collect?</p>
<p class="small">和旁邊的同學討論，再按「看結局」。 Discuss, then tap Finish.</p>'''},
}

# ------------------------------------------------------------------ reusable scene pieces
LIGHTS = [(8, 5), (15, 5), (22, 5), (34, 5)]
TRASH = [(3, 11), (8, 11), (4, 16), (9, 15), (3, 14), (9, 12)]

def lights(on):
    return '\n'.join(f'@put L{i} X:{1 if on else 0} lane {x} {y} -' for i, (x, y) in enumerate(LIGHTS, 1))

def trash():
    return '\n'.join(f'@put t{i} X:2 lane {x} {y} -' for i, (x, y) in enumerate(TRASH, 1))

BSW_BOOKS = [(1, 4), (3, 4), (5, 4), (2, 6), (4, 6)]
MSW_BOOKS = [(11, 4), (13, 4), (15, 4), (12, 6), (14, 6)]

def books(kind, state):
    """state: 'new' (! marker), 'read' (no marker), 'locked'."""
    pos = BSW_BOOKS if kind == 'b' else MSW_BOOKS
    out = []
    for i, (x, y) in enumerate(pos, 1):
        spr = 'D:63' if i % 2 else 'D:75'
        lab = 'bk_locked' if state == 'locked' else f'bk_{kind}{i}'
        out.append(f"@put {kind}k{i} {spr} library {x} {y} {lab}{' !' if state == 'new' else ''}")
    return '\n'.join(out)

def hall_students():
    return '\n'.join(f'@put s{i} {spr} hall {x} 5 -' for i, (spr, x) in enumerate([('v2', 2), ('v4', 4), ('v8', 10), ('v9', 12)], 1))

LANE_MID = f'''{lights(False)}
{trash()}
@put agong agong lane 15 9 a2_agong
@put yu yu lane 6 12 a2_yu
@door lane/chen lock 陳家。家裡沒人應門。
@door lane/jay lock 家。媽媽出門買菜了。'''

# ------------------------------------------------------------------ books: text shared by first reading and re-reading
BOOK_TEXT = {
    'b1': '''> 📘〈什麼是研究？ What Is Research?〉
> 我們常用五種方法「知道」事情：個人直覺與經驗、權威、傳統、常識、邏輯推理。它們很方便，可是都沒有經過查證。
> **實證研究** empirical research 不一樣：有系統地蒐集資料、分析資料，用證據回答問題。
> 還要小心**月暈效應**：一個人某方面很強，不代表他每一方面都對。
Me: 原來我那個夏天，一直在用「沒有查證」的方法。
@note empirical''',
    'b2': '''> 📘〈研究的五個目的 Five Purposes of Research〉
> 研究像爬樓梯，一共五階：① 敘述 describe：發生了什麼？（小宇一個月蹺幾天課？）
> ② 解釋 explain：**為什麼**？（小宇為什麼蹺課？）③ 預測 predict：接下來會怎樣？
> ④ 介入與處遇 intervene：我們該怎麼做？⑤ 比較與評估 evaluate：做了以後，有沒有用？
@note purposes''',
    'b3': '''> 📘〈算一算，還是懂一懂？ Quantitative and Qualitative〉
> **量化研究**用數字：問卷、統計。可以知道「有多少人」，也可以比較、預測。
> **質性研究**用文字：訪談、觀察。在自然的情境裡，了解一個人的經驗和想法。
Me: 所以請全巷子的人填問卷，是量化；坐下來聽阿公說他的故事，是質性。
@note quantitative
@note qualitative''',
    'b4': '''> 📘〈兩個方向 Two Directions〉
> **演繹法**：從理論出發 → 提出假設 → 用資料檢驗。量化研究常常這樣做。
> **歸納法**：從資料出發 → 找出模式 → 建立新的想法。質性研究常常這樣做。
@note deductive
@note inductive''',
    'b5': '''> 📘〈從問題開始 Questions and Hypotheses〉
> 好的**研究問題**：清楚、可以用資料回答，而且重要。
> ✘「小宇是不是壞孩子？」　✔「是什麼原因讓小宇不去上學？」
> **研究假設**是可以被檢驗的預測，常寫成「如果……，那麼……」：如果長輩參加每週運動團體，那麼他們會比較少跌倒。
@note research_question
@note hypothesis''',
    'm1': '''> 📗〈研究的六個步驟 Six Steps of Research〉
> ① 選定研究問題 → ② 檢閱文獻 → ③ 提出研究設計 → ④ 蒐集資料 → ⑤ 分析資料 → ⑥ 撰寫研究報告。
> 第一步永遠是問題。質性研究通常不會先提出假設。
@note six_steps''',
    'm2': '''> 📗〈先看看別人怎麼說 The Literature Review〉
> 開始之前，先查：關於這個問題，已經有哪些研究？哪些方法試過？有沒有用？這叫**文獻探討**。
> 來源要可信：經過同儕審查的期刊論文和研究回顧，比網紅影片、口耳相傳可靠得多。
@note lit_review''',
    'm3': '''> 📗〈研究倫理 Research Ethics〉
> 研究的對象是人。① 自願參加，可以隨時退出。② **知情同意**：先說清楚目的、過程和風險，對方了解並同意了才開始。
> ③ **保密**：不公開可以認出參與者的資料。④ 不傷害：研究不能讓人變得更糟。
@note informed_consent
@note confidentiality''',
    'm4': '''> 📗〈實證為基礎的實務 Evidence-Based Practice〉
> 好的社工實務結合三件事：最好的研究證據 ＋ 社工的專業經驗 ＋ 案主的價值與偏好。
> 研究證據很重要，但不能取代案主自己的聲音。
@note ebp''',
    'm5': '''> 📗〈這個方案有用嗎？ Program Evaluation〉
> 方案開始之前，先做**需求評量**：大家真正需要什麼？
> 結束的時候，分清楚**產出**（辦了幾次課）和**成效**（生活改變了多少）。
> 想確定改變是方案造成的？找一群情況相似、但沒有參加的人，當作**比較組**。
@note needs_assessment
@note output_outcome
@note comparison_group''',
}
BOOK_TITLE = {'b1': '〈什麼是研究？〉', 'b2': '〈研究的五個目的〉', 'b3': '〈算一算，還是懂一懂？〉', 'b4': '〈兩個方向〉', 'b5': '〈從問題開始〉',
              'm1': '〈研究的六個步驟〉', 'm2': '〈先看看別人怎麼說〉', 'm3': '〈研究倫理〉', 'm4': '〈實證為基礎的實務〉', 'm5': '〈這個方案有用嗎？〉'}

def book_blocks():
    out = []
    for key, text in BOOK_TEXT.items():
        kind, n = key[0], key[1]
        cnt = 'bswread' if kind == 'b' else 'mswread'
        out.append(f''':: bk_{key}
@if read_{key}=1 bk_{key}_text
@set read_{key} 1
@inc {cnt}
@goto bk_{key}_text
:: bk_{key}_text
@label {kind}k{n} bk_{key}
{text}
@goto {kind}_book_after''')
    return '\n\n'.join(out)

def exam_fail_chain(kind):
    """After a failed exam: name each missed question's book and put a ! back on it."""
    qs = ['e1', 'e2', 'e3', 'e4', 'e5'] if kind == 'b' else ['f1', 'f2', 'f3', 'f4', 'f5']
    pre = 'bsw' if kind == 'b' else 'msw'
    out = []
    for i, q in enumerate(qs, 1):
        nxt = f'{pre}_c{i + 1}' if i < 5 else f'{pre}_back'
        out.append(f''':: {pre}_c{i}
@if ok_{q}=0 {pre}_x{i}
@goto {nxt}
:: {pre}_x{i}
> 第 {i} 題答錯了 → 回去讀{BOOK_TITLE[kind + str(i)]}
@label {kind}k{i} bk_{kind}{i} !
@goto {nxt}''')
    return '\n'.join(out)

SCRIPT = r'''
// ======================= OPENING: HOME =======================
:: intro
@save
@clear
@tint none
@music warm
@player me
@title 和平巷，那年夏天|Peace Lane · one summer
@put mom jaymom jay 3 4 i_mom !
@map jay 5 6 up
> 高中畢業後的暑假。阿哲（就是你）終於有空了。
Mom: 阿哲，你過來一下。
@goal 和媽媽說話。

:: i_mom
Mom: 隔壁陳家最近好辛苦。陳媽媽一個人做兩份工作，常常半夜才回家。
Mom: 小宇放學後都在空地晃，聽說又蹺課了。陳阿公上個月跌倒了兩次。
Mom: 我們這條巷子也越來越不好住：路燈壞了好幾盞，空地堆滿了垃圾……
Me: 媽，我現在有空，我去幫他們！我一定想得到辦法。
Mom: 好孩子。去吧。
> 你走出家門。
@goto a1

// ======================= ACT 1: SIX GOOD IDEAS, NO RESEARCH =======================
:: a1
@save
@clear
@tint none
@music warm
@set tried 0
{{LIGHTS_OFF}}
{{TRASH}}
@put chenma chenma lane 11 5 a1_chenma !
@put agong agong lane 15 9 a1_agong !
@put yu yu lane 6 12 a1_yu !
@put wang wang lane 10 10 a1_wang !
@put chief chief lane 24 8 a1_chief !
@put lee lee lane 17 9 a1_lee !
@put huang huang lane 30 8 a1_huang !
@put star star lane 21 10 a1_star !
@door lane/library lock 圖書館。你心想：「看書太慢了，我要馬上幫上忙！」
@door lane/univ lock 山城大學。放暑假，校門關著。
@door lane/chen lock 陳家。家裡沒人應門。
@door lane/jay lock 家。你已經出門了，先去幫忙吧！
@map lane 5 5 down
> 和平巷的路燈壞了好幾盞，空地堆滿垃圾。頭上有 ! 的人，都有話要說。
@goal 和陳家、鄰居們聊聊，試試大家的辦法（試過 {tried} / 6 個）

:: a1_next
@if tried>=6 a1_end
@goal 和陳家、鄰居們聊聊，試試大家的辦法（試過 {tried} / 6 個）

:: a1_chenma
@label chenma a1_chenma2
ChenMa: 阿哲？……謝謝你關心。我要趕去上晚班了。
ChenMa: 小宇不聽話，阿公一直跌倒，巷子晚上又那麼暗……我真的不知道該從哪裡開始。
Me: 陳媽媽，交給我！我一定會想到辦法。

:: a1_chenma2
ChenMa: 阿哲，謝謝你。我得走了，晚班要遲到了。

:: a1_agong
@label agong a1_agong2
Agong: 年輕人，坐。……我上個月在浴室跌倒，前幾天又在巷口跌了一次。
Agong: 現在我都不太敢出門了。一個人坐在家裡，好悶。

:: a1_agong2
Agong: 你要幫忙？好啊。可是……你知道我們真正需要什麼嗎？

:: a1_agong_weak
Agong: 躺了三個星期，腳反而更沒力了……

// ---- 1. intuition & experience
:: a1_yu
@label yu a1_yu_done
Yu: ……幹嘛？
Me: 小宇，你為什麼不去上學？
> 小宇不說話，一直踢著地上的寶特瓶。
Me: （我小時候也蹺過課，因為上課很無聊。我的直覺告訴我：他只是需要好玩的東西！）
Me: 小宇，我把我的舊遊戲機送你！你乖乖去上學，回家就可以玩。
Yu: ……真的？謝謝哥哥！
@title 第二天|The next day
> 小宇打電動打到凌晨三點。第二天早上，他根本起不來，又沒去上學。
> 你的直覺來自你自己的經驗。可是小宇不是你。你從來沒有問過他「為什麼」。
@note intuition
@inc tried
@goto a1_next

:: a1_yu_done
Yu: ……遊戲機很好玩啊。上學？不想去。

// ---- 2. authority
:: a1_chief
@label chief a1_chief_done
Chief: 阿哲啊！聽說你要幫陳家？
Chief: 我當里長二十年了，聽我的準沒錯：老人家跌倒，就是要多躺在床上、少走動！
Me: 里長這麼有經驗，說的一定對。我去跟阿公說！
@title 三個星期後|Three weeks later
> 陳阿公很聽話，整天躺在床上。三個星期後，他的腿變得更沒力氣。
> 有一天晚上，他起床上廁所，又跌倒了。
Agong: ……躺越久，腳越軟。
> 里長很有地位，可是「有地位」不等於「有證據」。
@label agong a1_agong_weak
@note authority
@inc tried
@goto a1_next

:: a1_chief_done
Chief: 怎麼樣？老人家還是要多躺啦！

// ---- 3. tradition
:: a1_wang
@label wang a1_wang_wait
Wang: 空地的垃圾喔？簡單啦！
Wang: 我們這條巷子三十年來都是這樣做：貼一張「禁止亂丟垃圾」的告示，就好了。
Wang: 來，告示牌給你。去空地中間立起來吧。
@item 「禁止亂丟垃圾」告示牌
@zone signz lane 5 13 3 2 a1_sign
@goal 把告示牌立在空地中間（走到小宇附近）。

:: a1_wang_wait
Wang: 告示牌立好了嗎？空地中間，大家才看得到。

:: a1_sign
@unzone signz
@label wang a1_wang_done
@put sign T:83 lane 6 15 -
> 你把告示牌立好。「禁止亂丟垃圾！」很醒目。
@title 一個星期後|One week later
@put t7 X:2 lane 5 15 -
@put t8 X:2 lane 7 15 -
@put t9 X:2 lane 7 16 -
> 告示牌還在……只是現在，它被三袋新的垃圾圍住了。
Wang: 奇怪，以前都有用啊……
> 「一直都是這樣做」不代表「這樣做有用」。三十年來，從來沒有人檢查過。
@note tradition
@inc tried
@goto a1_next

:: a1_wang_done
Wang: 唉，現在的人都不看告示了。

// ---- 4. common sense
:: a1_lee
@label lee a1_lee_done
Lee: 路燈壞了？這是常識嘛：晚上那麼暗，很危險，大家晚上不要出門就好了。
Me: 有道理！我去告訴每一戶。
@title 那天晚上|That night
@tint night
@music quiet
> 晚上十一點，整條巷子空蕩蕩的，每一戶都關緊了門。
@put cm2 chenma lane 35 7 -
@move cm2 22 7
> 陳媽媽下了晚班，一個人走進漆黑的巷子。一台機車從黑暗中衝出來，差一點撞到她。
ChenMa: ……好可怕。以前晚上至少還有人在外面乘涼。
@move cm2 13 7
@del cm2
@tint none
@music warm
> 「大家都知道」的常識，反而讓巷子變得更空、更危險。
@note common_sense
@inc tried
@goto a1_next

:: a1_lee_done
Lee: 晚上不要出門，這是常識啊。

// ---- 5. logic
:: a1_huang
@label huang a1_huang_done
Huang: 小宇的事？我用邏輯幫你想。
Huang: 第一：蹺課的小孩都是壞孩子。第二：小宇蹺課。所以：小宇是壞孩子。
Huang: 叫巷子裡的小孩都離他遠一點，免得被帶壞。
Me: ……聽起來很有道理。好，我去跟大家說。
@title 兩個星期後|Two weeks later
> 巷子裡沒有小孩願意和小宇玩了。放學後，他一個人待在空地，待得更晚。
Yu: ……反正大家都說我是壞孩子。
> 推理的形式沒有錯，可是第一句話（前提）從來沒有人查證過。
@note logic
@inc tried
@goto a1_next

:: a1_huang_done
Huang: 邏輯就是邏輯，不會錯的。

// ---- 6. halo effect
:: a1_star
@label star a1_star_done
Star: 嘿！我是小飛，籃球網紅，兩百萬人追蹤！我在這裡拍影片。
Me: 小飛！我是你的粉絲！我鄰居家有好多問題……你覺得該怎麼辦？
Star: 簡單！快樂家庭的祕密：每天早上五點起床跑步，再喝我代言的能量飲料！
Star: 我就是這樣變成籃球高手的！
Me: 小飛說的，一定沒錯！
@item 一箱能量飲料（花光了你的打工錢）
@title 一個月後|One month later
> 陳媽媽上完夜班，五點根本起不來。陳阿公的腳不能跑步。小宇把飲料拿去空地，賣給別的小孩。
> 什麼都沒有改變。只有你的錢包變空了。
> 小飛籃球打得很好，但這不代表他懂家庭的問題。
@note halo
@inc tried
@goto a1_next

:: a1_star_done
Star: 記得按讚、訂閱、開啟小鈴鐺！

// ---- the end of the summer
:: a1_end
@goal
@music quiet
@title 夏天快結束了|The end of summer
> 你坐在空地旁的長椅上，覺得好累。
Me: 我試了六個辦法……每一個都失敗了。
Yu: 哥哥。
> 小宇不知道什麼時候站到了你旁邊。
Yu: 你每次都用「猜」的。你從來沒有問過我，為什麼不想去學校。
Agong: 年輕人，你有心，很好。可是幫人不能只靠熱心。
Agong: 你有沒有真的去問、去看、去算過？巷子底的圖書館，你進去過嗎？
@pause talk1
Me: 好。這一次，我不要再猜了。
> 你站起來，走向巷子底的圖書館。
@goto lib

// ======================= ACT 2: THE LIBRARY AND THE BACHELOR'S DEGREE =======================
:: lib
@save
@clear
@tint none
@music quiet
@set bswread 0
@set bswTries 0
@set bswdone 0
@set read_b1 0
@set read_b2 0
@set read_b3 0
@set read_b4 0
@set read_b5 0
{{LANE_MID}}
@door lane/univ lock 山城大學。先把圖書館左邊書架的書讀完，才有能力申請。
@put lib librarian library 8 6 b_lib !
{{BSW_NEW}}
{{MSW_LOCKED}}
@map library 8 10 up
@goal 和圖書館的溫館員說話。

:: bk_locked
> 這一排是研究所的書。先把左邊書架的書讀完吧。

:: a2_agong
Agong: 去圖書館了？好，好。

:: a2_yu
Yu: 哥哥你在讀書喔？……奇怪的人。

:: b_lib
@label lib b_lib2
Lib: 歡迎！你看起來很煩惱。
Me: 我想幫隔壁一家人。我試了六個辦法，全部失敗了。
Me: 我用了直覺、聽了里長的話、照著傳統、靠常識、用邏輯推理……還相信了一個網紅。
Lib: 那些都是「沒有查證」的知道方法。社會工作需要的是另一種：**研究**。
Lib: 研究不只是教授在做的事。研究就是：不要猜，去查證。有系統地蒐集資料、分析資料。
Lib: 左邊那排書架，是社會工作研究的入門書。五本都讀完，你就可以去申請巷子南邊的山城大學。
@goal 讀完左邊書架的五本書（{bswread} / 5）

:: b_lib2
@if bswread>=5 b_all_read
Lib: 左邊的書架，一共五本。讀完再去申請大學。

:: b_book_after
@if bswdone=1 noop
@if bswread>=5 b_all_read
@goal 讀完左邊書架的五本書（{bswread} / 5）

:: noop
// nothing more to do

:: b_all_read
@door lane/univ reset
@put prof D:88 hall 7 3 bsw_exam !
{{STUDENTS}}
@if bswTries>=1 b_retake_ready
Lib: 五本都讀完了！你已經懂研究的基本功了。
Lib: 去巷子南邊的山城大學報名社會工作學系吧。四年後的畢業考，五題要全部答對喔。
@goal 去山城大學（巷子南邊的紅色建築），參加社工學士畢業考。

:: b_retake_ready
Lib: 複習好了嗎？回大學找張教授重考吧。
@goal 回山城大學，找張教授重考學士畢業考。

{{BOOKS}}

:: bsw_exam
@label prof bsw_exam
@if bswTries>=1 bsw_go
@title 山城大學 社會工作學系|Hillside University · Department of Social Work
> 阿哲考上了社工系。四年裡，他上課、實習，也常常回到巷子底的圖書館讀書。
@title 四年後|Four years later
@goto bsw_go
:: bsw_go
Prof: 今天是社會工作學士的畢業考。一共五題，**每一題都要答對**，才能畢業。
Prof: 考試的時候，我不會告訴你答對還是答錯。準備好了嗎？開始！
@set bsw 0
@inc bswTries
@quiz e1
@quiz e2
@quiz e3
@quiz e4
@quiz e5
@if bsw>=5 bsw_pass
@music quiet
Prof: 你答對了 {bsw} / 5 題。社工要幫助真實的人，所以一題都不能錯。
@goto bsw_c1
{{BSW_FAIL}}
:: bsw_back
Prof: 回圖書館，把標了 ! 的書再讀一次，再回來找我重考。
@label prof bsw_exam !
@goal 回圖書館複習標了 ! 的書，再回大學重考（已經考了 {bswTries} 次）
@map library 8 10 up

:: bsw_pass
@music bright
Prof: 五題全對！恭喜你，阿哲。
@title 🎓 畢業典禮|Bachelor of Social Work · 社會工作學士
@item 🎓 社會工作學士學位證書 BSW
@set bswdone 1
Prof: 你已經會研究的基本功了。可是要替一整條巷子設計方案、評估成效，你還需要更多。
Prof: 去讀研究所吧。圖書館右邊那排書架，是研究所的書。葉教授會在這裡等你。
> 畢業後，你又回到了圖書館。
@goto msw

// ======================= ACT 2b: THE MASTER'S DEGREE =======================
:: msw
@save
@clear
@tint none
@music quiet
@set bswdone 1
@set mswread 0
@set mswTries 0
@set read_m1 0
@set read_m2 0
@set read_m3 0
@set read_m4 0
@set read_m5 0
{{LANE_MID}}
@door lane/univ reset
@put lib librarian library 8 6 m_lib !
{{BSW_READ}}
{{MSW_NEW}}
@put prof2 D:100 hall 7 3 msw_wait
{{STUDENTS}}
@map library 8 10 up
@title 研究所|Graduate school
@goal 讀完右邊書架的五本書（{mswread} / 5）

:: m_lib
@label lib m_lib2
Lib: 恭喜你畢業！你現在是社工學士了。
Lib: 右邊書架是研究所的書，一共五本。讀完以後，葉教授會在大學等你考碩士畢業考。

:: m_lib2
@if mswread>=5 m_all_read
Lib: 右邊的書架，一共五本。

:: m_book_after
@if mswread>=5 m_all_read
@goal 讀完右邊書架的五本書（{mswread} / 5）

:: m_all_read
@label prof2 msw_exam !
@if mswTries>=1 m_retake_ready
Lib: 五本都讀完了！去大學找葉教授吧。碩士畢業考，也是五題全對才能畢業。
@goal 去山城大學，找葉教授參加社工碩士畢業考。

:: m_retake_ready
Lib: 複習好了嗎？回大學找葉教授重考吧。
@goal 回山城大學，找葉教授重考碩士畢業考。

:: msw_wait
ProfYe: 你好，我是葉教授。先把圖書館右邊的五本書讀完，再來找我。

:: msw_exam
@label prof2 msw_exam
@if mswTries>=1 msw_go
@title 研究所兩年|Two years of graduate school
> 兩年裡，阿哲在社福機構實習，跟著葉教授做了一個真正的研究。
@goto msw_go
:: msw_go
ProfYe: 今天是社會工作碩士的畢業考。一樣五題，**每一題都要答對**。開始吧。
@set msw 0
@inc mswTries
@quiz f1
@quiz f2
@quiz f3
@quiz f4
@quiz f5
@if msw>=5 msw_pass
@music quiet
ProfYe: 你答對了 {msw} / 5 題。差一點點，但社工的方案會影響很多人的生活。
@goto msw_c1
{{MSW_FAIL}}
:: msw_back
ProfYe: 回圖書館，把標了 ! 的書再讀一次，再回來找我。
@label prof2 msw_exam !
@goal 回圖書館複習標了 ! 的書，再回大學重考（已經考了 {mswTries} 次）
@map library 8 10 up

:: msw_pass
@music bright
ProfYe: 五題全對。恭喜你，阿哲。
@title 🎓 畢業典禮|Master of Social Work · 社會工作碩士
@item 🎓 社會工作碩士學位證書 MSW
ProfYe: 你準備好成為一位會用研究的社工了。去吧，回到需要你的地方。
@goto sw

// ======================= ACT 3: BACK ON PEACE LANE =======================
:: sw
@save
@clear
@tint none
@music warm
@title 幾年後|Some years later
{{LIGHTS_OFF}}
{{TRASH}}
@put t7 X:2 lane 5 15 -
@put t8 X:2 lane 7 15 -
@put mom jaymom lane 6 5 a3_mom
@put chenma chenma chen 3 4 a3_s1 !
@put agong agong chen 8 4 a3_wait_agong
@put yu yu chen 8 2 a3_wait_yu
@put wang wang lane 20 5 a3_wait_n
@put lee lee lane 15 16 a3_wait_n
@put huang huang lane 33 16 a3_wait_n
@put liu liu lane 30 8 a3_wait_n
@put chief chief lane 24 8 a3_wait_n
@put lib librarian library 8 6 a3_lib_wait
@door lane/chen reset
@door lane/library reset
@door lane/univ lock 山城大學。你已經畢業了。
@door lane/jay lock 家。媽媽在門口。
@map lane 5 5 down
> 阿哲在城裡的社會福利中心當了幾年社工。這一天，他被派回自己長大的地方：和平巷。
> 巷子的路燈還是壞的，空地的垃圾更多了。
Mom: 阿哲！你回來了。陳家……還是很辛苦。小宇現在讀國中，常常蹺課；阿公又跌倒了好幾次。
Me: 媽，這一次，我不會再用猜的。
@goal 去陳家看看（就在隔壁）。

:: a3_mom
Mom: 陳家就在隔壁。加油！

:: a3_wait_agong
Agong: 阿哲？長這麼大了。

:: a3_wait_yu
Yu: ……

:: a3_wait_n
> 他們好像在忙。你可以晚一點再來。

:: a3_lib_wait
Lib: 阿哲！好久不見。需要查資料，隨時來找我。

// ---- research step 1: a research question
:: a3_s1
@label chenma a3_cm_wait
ChenMa: 阿哲？你現在是社工了！太好了，快告訴我們該怎麼辦！
Me: （研究的第一步是……）
@goto a3_s1_ask
:: a3_s1_ask
@choice
? 「我早就知道了：小宇太懶，阿公年紀太大，多休息就好。」 -> a3_s1_bad1
? 「我先不下結論。我們一起想一個研究問題：是什麼讓這個家和這條巷子這麼辛苦？什麼才幫得上忙？」 -> a3_s1_ok
? 「我去問里長怎麼辦，里長說了算。」 -> a3_s1_bad2

:: a3_s1_bad1
> 小宇聽到「懶」這個字，甩門出去了。陳媽媽的臉也沉了下來。
> 這是那年夏天的直覺，又回來了。
@pause oops
@goto a3_s1_ask

:: a3_s1_bad2
> 里長說：「老人家就是要躺床！」……這句話，你好像聽過。
@pause oops
@goto a3_s1_ask

:: a3_cm_wait
ChenMa: 慢慢來，我們都願意幫忙。

:: a3_s1_ok
ChenMa: 研究問題？……好，你問吧。
Me: 研究的第一步，是一個好的**研究問題**：清楚、可以用資料回答，而且重要。
Me: 我想先和你們每一個人聊聊。不過在開始之前——
@goto a3_s2_ask
// ---- ethics
:: a3_s2_ask
@choice
? 「我先說明我想做什麼、會怎麼使用你們說的話。要不要參加由你們決定，名字不會公開，隨時可以停。」 -> a3_s2_ok
? 「我偷偷用手機錄音，這樣你們說話比較自然。」 -> a3_s2_bad1
? 「我把你們的故事和照片貼上臉書，馬上就會有人捐錢！」 -> a3_s2_bad2

:: a3_s2_bad1
> 阿公發現你的手機在錄音。「你把我們當成什麼？」他再也不肯跟你說話。
> 沒有同意的研究，會失去信任，也違反研究倫理。
@pause oops
@goto a3_s2_ask

:: a3_s2_bad2
> 貼文被分享了一千次。小宇在學校被同學認出來，被笑了一整個星期。
> 研究不能傷害參與者，也必須保密。
@pause oops
@goto a3_s2_ask

:: a3_s2_ok
Agong: 你肯先問我們，我很高興。我願意。
ChenMa: 我也願意。小宇……你自己決定。
Yu: ……好啦。
Me: 謝謝你們。這就是**知情同意**和**保密**。
@set iv 0
@label agong a3_iv_agong !
@label chenma a3_iv_cm !
@label yu a3_iv_yu !
@goal 訪談陳家三個人（{iv} / 3）

// ---- qualitative interviews
:: a3_iv_agong
@label agong a3_iv_agong_done
Me: 阿公，可以說說您跌倒的事嗎？
Agong: 我不是不想動，是怕。上次跌倒以後，我就不敢一個人出門。
Agong: 巷子那麼暗，也沒有人陪。以前我很會下棋、種菜……現在什麼都不做，腳就越來越沒力。
Me: （記下來：怕跌倒、晚上太暗、沒有人陪、想做點事。）
@inc iv
@goto a3_iv_next

:: a3_iv_agong_done
Agong: 想到什麼，再來問我。

:: a3_iv_cm
@label chenma a3_iv_cm_done
ChenMa: 我一天做兩份工作。小宇放學以後，家裡沒有大人。
ChenMa: 我很想陪他寫功課，可是回到家都十一點了。巷子那麼暗，我每天走回來都好怕。
Me: （記下來：家裡沒有大人、工作時間長、晚上回家不安全。）
@inc iv
@goto a3_iv_next

:: a3_iv_cm_done
ChenMa: 謝謝你願意聽。

:: a3_iv_yu
@label yu a3_iv_yu_done
Yu: ……我不是懶。數學我完全聽不懂，回家也沒有人可以問。
Yu: 去學校只是坐著聽不懂，所以我乾脆不去。放學以後，除了空地，也沒有地方可以去。
Me: （記下來：功課跟不上、沒有人可以問、放學後沒有地方去。）
@inc iv
@goto a3_iv_next

:: a3_iv_yu_done
Yu: ……你真的有在聽耶。

:: a3_iv_next
@if iv>=3 a3_iv_done
@goal 訪談陳家三個人（{iv} / 3）

:: a3_iv_done
Me: 這些是**質性資料**：我聽到了他們的經驗和理由。
Me: 可是這只是一家人。巷子裡其他人也這樣嗎？關於這些問題，別人已經研究出什麼了？
@label lib a3_lit !
@goal 去圖書館找溫館員，做文獻探討。

// ---- literature review and design
:: a3_lit
@label lib a3_lib_wait
Lib: 阿哲！要查什麼？
Me: 長輩跌倒、孩子放學後沒地方去、巷子太暗、空地都是垃圾。我想知道已經有哪些研究。
Lib: 這叫**文獻探討**。我這裡的資料很多，你要相信哪一種？
@goto a3_lit_ask
:: a3_lit_ask
@choice
? 「籃球網紅小飛的爆紅影片，三百萬次觀看！」 -> a3_lit_bad1
? 「經過同儕審查的研究論文和研究回顧。」 -> a3_lit_ok
? 「巷子裡大家一直以來的說法就夠了。」 -> a3_lit_bad2

:: a3_lit_bad1
> 觀看次數很多，不代表內容是對的。這是月暈效應。
@pause oops
@goto a3_lit_ask

:: a3_lit_bad2
> 「一直以來的說法」……就是那年被垃圾淹沒的告示牌。
@pause oops
@goto a3_lit_ask

:: a3_lit_ok
Lib: 很好。來，看看研究怎麼說：
> 📄 有平衡和肌力訓練的運動方案，可以減少長輩跌倒（Sherrington et al., 2019）。
> 📄 規劃良好的課後方案，能提升孩子的社交能力和對學校的連結（Durlak et al., 2010）。
> 📄 改善路燈照明，和犯罪減少有關（Welsh & Farrington, 2008）。
> 📄 把閒置空地清乾淨、種上綠地，附近居民覺得更安全（Branas et al., 2018）。
Me: 原來這些問題都有人研究過！不用從零開始猜。
Lib: 下一步是研究設計。你打算怎麼蒐集和平巷的資料？
@goto a3_design_ask
:: a3_design_ask
@choice
? 「只問我媽就好，她認識每一個人。」 -> a3_design_bad1
? 「混合方法：每一戶都填一份簡短的問卷（量化），再加上剛剛的訪談（質性）。」 -> a3_design_ok
? 「不用蒐集了，研究都說好了，直接照做。」 -> a3_design_bad2

:: a3_design_bad1
> 只問一個人，就只聽到一個人的看法。媽媽不等於全巷子。
@pause oops
@goto a3_design_ask

:: a3_design_bad2
> 別的地方的研究很重要，可是和平巷的人真正需要什麼？你還不知道。
@pause oops
@goto a3_design_ask

:: a3_design_ok
Lib: 量化告訴你「有多少」，質性告訴你「為什麼」。這叫**混合研究方法**。
@note mixed_methods
Me: 這份問卷也是一份**需求評量**：在設計方案之前，先了解大家真正需要什麼。
@set sv 0
@label wang a3_sv_wang !
@label lee a3_sv_lee !
@label huang a3_sv_huang !
@label liu a3_sv_liu !
@label mom a3_sv_mom !
@goal 請巷子裡五戶人家填問卷（{sv} / 5）

// ---- quantitative survey (anonymous and voluntary)
:: a3_sv_wang
@label wang a3_sv_done
Me: 王阿姨，這是一份不記名的問卷，大約三分鐘。要不要填，由您決定。
Wang: 好啊！我勾：路燈太暗、空地垃圾、孩子放學後沒地方去。
Wang: 對了，我退休前是小學老師，教數學的喔。
@inc sv
@goto a3_sv_next

:: a3_sv_lee
@label lee a3_sv_done
Me: 李先生，這是一份不記名的問卷，要不要填由您決定。
Lee: 不記名喔？好。我勾：路燈太暗、空地垃圾。我爸也很少出門，他怕跌倒。
@inc sv
@goto a3_sv_next

:: a3_sv_huang
@label huang a3_sv_done
Me: 黃伯伯，可以請您填一份不記名的問卷嗎？不填也沒關係。
Huang: 問卷？……好吧。路燈太暗。我孫子放學後也沒地方去。我自己啊，也怕跌倒。
@inc sv
@goto a3_sv_next

:: a3_sv_liu
@label liu a3_sv_done
Me: 劉小姐，這是一份不記名的問卷，大約三分鐘。
Liu: 我剛搬來。最怕晚上回家，巷子太暗了。還有那片空地，好多垃圾和蚊子。
@inc sv
@goto a3_sv_next

:: a3_sv_mom
@label mom a3_mom
Me: 媽，問卷也請您填一份。不記名，不想填也可以喔。
Mom: 當然要填！路燈太暗、空地垃圾、孩子放學後沒地方去。還有，我也想多認識鄰居，大家都關在家裡。
@inc sv
@goto a3_sv_next

:: a3_sv_done
> 謝謝你的協助！問卷已經收好了。

:: a3_sv_next
@if sv>=5 a3_analyze
@goal 請巷子裡五戶人家填問卷（{sv} / 5）

// ---- analysis
:: a3_analyze
@title 分析資料|Analyzing the data
> 你把五份問卷和三次訪談整理好。
> 📊 5 / 5 戶：巷子太暗，晚上不敢出門。　📊 4 / 5 戶：空地垃圾多、不安全。
> 📊 3 / 5 戶：孩子放學後沒地方去。　📊 2 / 5 戶：家裡長輩怕跌倒、很少出門。
> 💬 訪談的主題：怕跌倒、沒有人陪；功課跟不上、放學後沒有大人；晚上回家不安全。
Me: 這些資料告訴我什麼？
@goto a3_an_ask
:: a3_an_ask
@choice
? 「小宇是壞孩子，問題都是他造成的。」 -> a3_an_bad1
? 「五戶人家的結果，可以證明全台灣都是這樣。」 -> a3_an_bad2
? 「這些問題連在一起：巷子太暗、空地沒人管、孩子沒地方去、長輩不敢出門。陳家的困難，也是整條巷子的困難。」 -> a3_an_ok

:: a3_an_bad1
> 資料裡沒有任何一句話說小宇是「壞孩子」。這是黃伯伯那年的「邏輯」。
@pause oops
@goto a3_an_ask

:: a3_an_bad2
> 五戶人家只能說明和平巷。想說「全台灣」，需要更大、更有代表性的樣本。
@pause oops
@goto a3_an_ask

:: a3_an_ok
Me: 「發生什麼」（敘述）和「為什麼」（解釋）都有了。下一步：和大家一起決定怎麼介入。
@label wang -
@label lee -
@label huang -
@label liu -
@label mom -
@label chief a3_meet !
@goal 找里長召開社區會議。

// ---- intervention: evidence-based practice with the neighbors
:: a3_meet
@label chief -
Chief: 阿哲，聽說你在做調查？好，我把大家都叫來，就在空地旁邊開會！
@title 社區會議|A neighborhood meeting
@put chief chief lane 12 9 -
@put agong agong lane 15 9 -
@put yu yu lane 16 10 -
@put chenma chenma lane 13 11 -
@put wang wang lane 17 9 -
@put lee lee lane 17 10 -
@put huang huang lane 14 11 -
@put liu liu lane 16 11 -
@put mom jaymom lane 12 11 -
@pos 14 8 down
Me: 謝謝大家填問卷。結果是：五戶都覺得巷子太暗，四戶覺得空地不安全，三戶的孩子放學後沒地方去。
Me: 研究也告訴我們哪些方法有用。不過要怎麼做，大家的想法一樣重要。
Agong: 我以前很會種菜，也會下棋。
Wang: 我退休前是小學數學老師喔！
Yu: ……如果空地有地方可以寫功課，我可以去。
Me: （最好的研究證據＋我的專業經驗＋大家的想法和需要。）
@goto a3_plan_ask
:: a3_plan_ask
@choice
? 「每一家發一箱小飛代言的能量飲料！」 -> a3_plan_bad1
? 「我已經都設計好了，大家照我的計畫做就好。」 -> a3_plan_bad2
? 「我們一起做：把空地清乾淨變成菜園，阿公教大家種菜；王阿姨帶課後功課班；長輩每週一起做平衡運動、散步；我帶著問卷資料去市公所，申請修路燈。」 -> a3_plan_ok

:: a3_plan_bad1
> ……那一年夏天，你已經試過了。
@pause oops
@goto a3_plan_ask

:: a3_plan_bad2
> 大家安靜地聽完。散會以後，沒有一個人出現。沒有案主的聲音，計畫就只是你一個人的計畫。
@pause oops
@goto a3_plan_ask

:: a3_plan_ok
Everyone: 好！一起來！
Chief: 有數字，我去市公所講話就有力了！
Me: 這就是**實證為基礎的實務**：研究證據、專業經驗，加上大家的價值和想法。
@title 三個月後|Three months later
{{LIGHTS_ON}}
{{NO_TRASH}}
@put g1 X:3 lane 3 12 -
@put g2 X:3 lane 5 12 -
@put g3 X:3 lane 3 14 -
@put g4 X:3 lane 5 14 -
@put f1 X:4 lane 8 11 -
@put f2 X:4 lane 3 16 -
@put f3 X:4 lane 9 16 -
@put desk D:72 lane 8 14 -
@put agong agong lane 4 13 a3_after_agong
@put yu yu lane 8 13 a3_after_yu
@put wang wang lane 9 14 a3_after_wang
@put lee lee lane 6 16 a3_after_lee
@put huang huang lane 7 12 a3_after_huang
@put chief chief lane 24 8 a3_after_chief
@put liu liu lane 30 8 a3_after_liu
@put mom jaymom lane 6 5 a3_after_mom
@put chenma chenma lane 12 8 a3_eval !
@music bright
> 路燈修好了。空地變成了「和平菜園」，阿公每天早上帶著長輩在這裡做運動、種菜。
> 下午四點，王阿姨在菜園旁的桌子帶孩子寫功課。晚上，巷子裡又有人散步、聊天了。
@title 六個月後|Six months later
@goal 評估方案的成效：去找陳媽媽談談。

:: a3_after_agong
Agong: 今天的青菜長得真好！我們運動團體現在有八個人了。

:: a3_after_yu
Yu: 王老師教的分數，我終於懂了！

:: a3_after_wang
Wang: 退休以後，好久沒有這麼開心了。

:: a3_after_lee
Lee: 我爸現在每天早上都來散步。

:: a3_after_huang
Huang: 我錯了。小宇不是壞孩子，他只是需要有人教。

:: a3_after_chief
Chief: 市公所說，下個月要來參觀！

:: a3_after_liu
Liu: 現在晚上回家，一點都不怕了。

:: a3_after_mom
Mom: 你看，大家都出來了。

// ---- evaluation and report
:: a3_eval
@label chenma a3_eval_done
ChenMa: 阿哲，大家都說方案很成功！你要寫報告給市公所嗎？
Me: 對。最後要評估，再寫成報告。我要怎麼證明方案真的有用？
@goto a3_eval_ask
:: a3_eval_ask
@choice
? 「我們辦了 96 次功課班、48 次運動團體。數字這麼大，一定成功！」 -> a3_eval_bad1
? 「大家看起來都很開心，就代表有用。」 -> a3_eval_bad2
? 「比較方案前後的成效（小宇的出席、阿公跌倒的次數），也和附近情況相似、但沒有方案的光明巷比較。」 -> a3_eval_ok

:: a3_eval_bad1
> 那是**產出**：你「做了多少」。市公所想知道的是**成效**：大家的生活「改變了多少」。
@pause oops
@goto a3_eval_ask

:: a3_eval_bad2
> 「看起來」不是資料。也許只是剛好天氣變好了呢？
@pause oops
@goto a3_eval_ask

:: a3_eval_done
ChenMa: 謝謝你，阿哲。

:: a3_eval_ok
@title 評估結果|Evaluation results
> 📊 小宇：一個月蹺課 12 天 → 1 天。數學從 38 分進步到 71 分。
> 📊 阿公：方案前半年跌倒 4 次 → 最近三個月 0 次。運動團體的長輩，跌倒都變少了。
> 📊 晚上在巷子裡散步的鄰居：幾乎沒有 → 每晚十幾個人。
> 📊 比較組「光明巷」：同樣的六個月，幾乎沒有改變。
Me: 方案前後有差別，和比較組也有差別。現在我比較有把握：是這個方案帶來了改變。
Me: 最後一步：撰寫研究報告，交給市公所，也講給巷子裡的每一個人聽。
@title 一年後|One year later
> 市公所讀了報告，決定把「和平菜園」的做法帶到另外五條巷子。
@goto a3_final

:: a3_final
@goal
@music quiet
Yu: 哥哥。……謝謝你這次有先問我。
Yu: 我以後也想當社工。
Agong: 年輕人，這一次，你沒有用猜的。
Agong: 有心，再加上研究，才真的幫得上忙。
Me: （直覺、權威、傳統、常識、邏輯……都不能代替查證。研究，是社工幫助人的工具。）
@pause final
@end
'''

SCRIPT = (SCRIPT
          .replace('{{LANE_MID}}', LANE_MID)
          .replace('{{LIGHTS_OFF}}', lights(False))
          .replace('{{LIGHTS_ON}}', lights(True))
          .replace('{{TRASH}}', trash())
          .replace('{{NO_TRASH}}', '\n'.join(f'@del t{i}' for i in range(1, 10)) + '\n@del sign')
          .replace('{{BSW_NEW}}', books('b', 'new'))
          .replace('{{BSW_READ}}', books('b', 'read'))
          .replace('{{MSW_NEW}}', books('m', 'new'))
          .replace('{{MSW_LOCKED}}', books('m', 'locked'))
          .replace('{{STUDENTS}}', hall_students())
          .replace('{{BOOKS}}', book_blocks())
          .replace('{{BSW_FAIL}}', exam_fail_chain('b'))
          .replace('{{MSW_FAIL}}', exam_fail_chain('m')))
assert '{{' not in SCRIPT

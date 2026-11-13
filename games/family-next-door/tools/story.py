"""Story script, pauses and jump codes for 隔壁那一家 The Family Next Door. build_data.py imports this file.
Edit here, then run: python3 tools/build_data.py

Shape of the story
  Act 1  The last five days of summer. Six well-meant ideas, time for only five; every one is a guess. On the last
         night Xiao Yu goes missing in the dark lane. Mini-game: cleaning the lot (trash sort) plants the first clue.
  Act 2  The library: find the research books among the junk, pass the BSW exam (card-sort mini-game), then the MSW.
  Act 3  Six years later the city will pave the lot unless the neighbors win a town hall in 30 days. Four investigations
         in any order, each costs days: interviews (trust mini-game), night watch (stakeout), survey, literature
         (source detective). Each success is an evidence card. Town hall: answer four claims (mini-game).
         Ending depends on the cards: 4 = everything saved, 2-3 = half, 0-1 = paved (with a chance to replay the month).
  Two twists: the trash is dumped by a construction truck at 2 a.m., and Xiao Yu skips school because he gets up
  every night to help Grandpa, who falls in the dark hallway.

Jump codes (title screen, for a student who changes device):
  LIBRARY    -> the library, before the bachelor's (BSW) exam
  MASTER     -> after the BSW, before the master's (MSW) exam
  HOMECOMING -> back on Peace Lane, the 30-day countdown
"""

JUMPS = {'LIBRARY': 'lib', 'MASTER': 'msw', 'HOMECOMING': 'sw'}

PAUSES = {
    'talk1': {
        'head': '💬 討論時間 Discussion', 'ready': True, 'go': '繼續 Continue',
        'html': '''<p><b>阿哲這個暑假的辦法，為什麼都失敗了？你自己最常用哪一種「沒有查證」的方法來做決定？</b></p>
<p class="en">Why did all of Ah-Zhe's ideas fail? Which unchecked way of knowing do you use most often?</p>
<p><b>猜猜看：小宇為什麼半夜一個人在外面？</b></p>
<p class="en">Guess: why was Xiao Yu out alone in the dark? (Keep your guess. You will find out.)</p>
<p class="small">和旁邊的同學討論，再按「繼續」。 Talk with your partner, then tap Continue.</p>'''},
    'oops': {
        'head': ' ', 'over': True, 'ready': True, 'go': '再試一次 Try again',
        'html': '''<div class="gameover">GUESSING AGAIN</div>
<p>又在猜了！這不是研究。</p>
<p class="en">That is a guess, not research.</p>
<p class="small">回到這一步，再選一次。 Go back and choose again.</p>'''},
    'final': {
        'head': '💬 最後討論 Final Discussion', 'ready': True, 'go': '看結局 Finish',
        'html': '''<p><b>阿哲在第一個暑假，和六年後，最大的不同是什麼？</b></p>
<p class="en">What changed most between Ah-Zhe's first summer and six years later?</p>
<p><b>想一想你的社區、宿舍或校園裡的一個問題。在動手解決之前，你會問什麼研究問題？會蒐集哪些資料？</b></p>
<p class="en">Pick one problem near you. Before fixing it, what would you ask, and what data would you collect?</p>
<p class="small">和旁邊的同學討論，再按「看結局」。 Discuss, then tap Finish.</p>'''},
}

# ------------------------------------------------------------------ reusable scene pieces
LIGHTS = [(8, 5), (15, 5), (22, 5), (34, 5)]
TRASH = [(3, 11), (8, 11), (4, 16), (9, 15), (3, 14), (9, 12)]

def lights(on):
    return '\n'.join(f'@put L{i} X:{1 if on else 0} lane {x} {y} -' for i, (x, y) in enumerate(LIGHTS, 1))

def trash(extra=False):
    pos = TRASH + ([(5, 15), (7, 15), (7, 16)] if extra else [])
    return '\n'.join(f'@put t{i} X:2 lane {x} {y} -' for i, (x, y) in enumerate(pos, 1))

# library shelves: ten places; five hold the BSW books, the other five hold junk (and later the MSW books)
SHELVES = [(1, 4), (3, 4), (5, 4), (2, 6), (4, 6), (11, 4), (13, 4), (15, 4), (12, 6), (14, 6)]
BSW_AT = {'b1': 1, 'b2': 7, 'b3': 4, 'b4': 9, 'b5': 3}           # book -> shelf number (1-based)
MSW_AT = {'m1': 2, 'm2': 6, 'm3': 5, 'm4': 10, 'm5': 8}
JUNK = {2: 'd1', 5: 'd2', 6: 'd3', 8: 'd4', 10: 'd5'}

def shelves(phase):
    """phase 'bsw': BSW books + junk, no ! marks (a search). 'msw': BSW books read, MSW books marked !."""
    out = []
    for n, (x, y) in enumerate(SHELVES, 1):
        spr = 'D:63' if n % 2 else 'D:75'
        if phase == 'bsw':
            book = next((b for b, s in BSW_AT.items() if s == n), None)
            lab = f'bk_{book}' if book else f'junk_{JUNK[n]}'
            out.append(f'@put sh{n} {spr} library {x} {y} {lab}')
        else:
            book = next((b for b, s in {**BSW_AT, **MSW_AT}.items() if s == n))
            out.append(f"@put sh{n} {spr} library {x} {y} bk_{book}{' !' if book[0] == 'm' else ''}")
    return '\n'.join(out)

def hall_students():
    return '\n'.join(f'@put s{i} {spr} hall {x} 5 -' for i, (spr, x) in enumerate([('v2', 2), ('v4', 4), ('v6', 10), ('v9', 12)], 1))

LANE_MID = f'''{lights(False)}
{trash(True)}
@put agong agong lane 15 9 a2_agong
@put yu yu lane 6 12 a2_yu
@door lane/chen lock 陳家。家裡沒人應門。
@door lane/jay lock 家。媽媽出門買菜了。'''

# ------------------------------------------------------------------ books
BOOK_TEXT = {
    'b1': '''> 📘〈什麼是研究？ What Is Research?〉
> 我們常用五種方法「知道」事情：個人直覺與經驗、權威、傳統、常識、邏輯推理。它們很方便，可是都沒有經過查證。
> 還要小心**月暈效應**：一個人某方面很強，不代表他每一方面都對。
> **實證研究** empirical research 不一樣：有系統地蒐集資料、分析資料，用證據回答問題。
Me: 原來我那個暑假的每一個辦法，都是用「沒有查證」的方法想出來的。
@note intuition
@note authority
@note tradition
@note common_sense
@note logic
@note halo
@note empirical''',
    'b2': '''> 📘〈研究的五個目的 Five Purposes of Research〉
> 研究像爬樓梯，一共五階：① 敘述 describe：發生了什麼？（小宇一個月蹺幾天課？）
> ② 解釋 explain：**為什麼**？（小宇為什麼蹺課？）③ 預測 predict：接下來會怎樣？
> ④ 介入與處遇 intervene：我們該怎麼做？⑤ 比較與評估 evaluate：做了以後，有沒有用？
Me: 我那年夏天，跳過了前面四階，直接想「該怎麼做」。
@note purposes''',
    'b3': '''> 📘〈算一算，還是懂一懂？ Quantitative and Qualitative〉
> **量化研究**用數字：問卷、統計。可以知道「有多少人」，也可以比較、預測。
> **質性研究**用文字：訪談、觀察。在自然的情境裡，了解一個人的經驗和想法。
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
JUNK_TEXT = {
    'd1': '> 📕《讓你的貓幫你理財》……跟研究一點關係也沒有。放回去。',
    'd2': '> 📕《一百個名人幸運小撇步》名人說的就一定對？這是月暈效應。放回去。',
    'd3': '> 📕《阿嬤說的都對》「一直都是這樣」不等於「有用」。放回去。',
    'd4': '> 📕《三分鐘看懂人生》太簡單的答案，通常不可信。放回去。',
    'd5': '> 📕《我的直覺從來不會錯》……這個暑假，你已經試過了。放回去。',
}

def book_blocks():
    out = []
    for key, text in BOOK_TEXT.items():
        kind = key[0]
        cnt = 'bswread' if kind == 'b' else 'mswread'
        shelf = (BSW_AT if kind == 'b' else MSW_AT)[key]
        out.append(f''':: bk_{key}
@if read_{key}=1 bk_{key}_text
@set read_{key} 1
@inc {cnt}
@goto bk_{key}_text
:: bk_{key}_text
@label sh{shelf} bk_{key}
{text}
@goto {kind}_book_after''')
    for key, text in JUNK_TEXT.items():
        out.append(f':: junk_{key}\n{text}')
    return '\n\n'.join(out)

def exam_fail_chain(kind):
    """After a failed exam: put a ! back on each book whose cards were wrong."""
    books = ['b1', 'b2', 'b3', 'b4', 'b5'] if kind == 'b' else ['m1', 'm2', 'm3', 'm4', 'm5']
    pre = 'bsw' if kind == 'b' else 'msw'
    at = BSW_AT if kind == 'b' else MSW_AT
    out = []
    for i, bk in enumerate(books, 1):
        nxt = f'{pre}_c{i + 1}' if i < 5 else f'{pre}_back'
        out.append(f''':: {pre}_c{i}
@if miss_{bk}=1 {pre}_x{i}
@goto {nxt}
:: {pre}_x{i}
@label sh{at[bk]} bk_{bk} !
@goto {nxt}''')
    return '\n'.join(out)

HUB_GOAL = '⏳ 市民大會倒數 **{days}** 天 · 🗂️ 證據卡 **{ev} / 4**'

SCRIPT = r'''
// ======================= OPENING: HOME =======================
:: intro
@save
@clear
@tint none
@music warm
@player me
@title 和平巷，暑假最後五天|Peace Lane · the last five days of summer
@put mom jaymom jay 3 4 i_mom !
@map jay 5 6 up
> 高中剛畢業。下星期一，阿哲（就是你）就要去城裡的工廠上班了。
Mom: 阿哲，你過來一下。
@goal 和媽媽說話。

:: i_mom
Mom: 隔壁陳家最近好辛苦。陳媽媽一個人做兩份工作，晚上都在上夜班。
Mom: 小宇又蹺課了，學校打了好幾次電話。奇怪，那孩子最近老是在打哈欠。
Mom: 陳阿公前幾天晚上又在家裡跌倒了。巷子裡的路燈也壞了，空地堆滿垃圾……
Me: 媽，我還有五天。五天，我一定能幫他們想到辦法！
Mom: 好孩子。去吧。
@goto a1

// ======================= ACT 1: FIVE DAYS, SIX IDEAS =======================
:: a1
@save
@clear
@tint none
@music warm
@set day 1
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
@door lane/library lock 圖書館。你心想：「看書太慢了，我只有五天！」
@door lane/univ lock 山城大學。放暑假，校門關著。
@door lane/chen lock 陳家。家裡沒人應門。
@door lane/jay lock 家。你已經出門了，先去幫忙吧！
@map lane 5 5 down
> 頭上有 ! 的人，都有辦法要告訴你。可是每試一個辦法，就要花掉一天。你只有五天。
@goal 📅 暑假第 **{day} / 5** 天 · 和鄰居聊聊，選一個辦法試試看

:: a1_next
@inc day
@inc tried
@if day>=6 a1_night
@goal 📅 暑假第 **{day} / 5** 天 · 還有辦法可以試（已經試了 {tried} 個）

:: a1_chenma
@label chenma a1_chenma2
ChenMa: 阿哲？……謝謝你關心。我要趕去上夜班了。
ChenMa: 小宇不聽話，阿公一直跌倒，巷子晚上又那麼暗……我真的不知道該從哪裡開始。
Me: 陳媽媽，交給我！五天之內，我一定想到辦法。

:: a1_chenma2
ChenMa: 阿哲，謝謝你。我得走了。

:: a1_agong
@label agong a1_agong2
Agong: 年輕人，坐。……前幾天晚上，我又在家裡跌倒了。
Agong: 現在我都不太敢一個人走動。好悶啊。

:: a1_agong2
Agong: 你要幫忙？好啊。可是……你知道我們真正需要什麼嗎？

:: a1_agong_weak
Agong: 躺了幾天，腳反而更沒力了……

// ---- intuition & experience
:: a1_yu
@label yu a1_yu_done
Yu: ……（打了一個大哈欠）幹嘛？
Me: 小宇，你為什麼不去上學？
> 小宇不說話，一直踢著地上的寶特瓶。
Me: （我小時候也蹺過課，因為上課很無聊。我的直覺告訴我：他只是需要好玩的東西！）
Me: 小宇，我把我的舊遊戲機送你！你乖乖去上學，回家就可以玩。
Yu: ……喔。謝謝。
> 隔天早上，學校又打電話來：小宇沒去。遊戲機還在盒子裡，他根本沒拆。
> 奇怪……那他到底在忙什麼？你從來沒有問過他「為什麼」。
@note intuition
@goto a1_next

:: a1_yu_done
Yu: ……（又打了一個哈欠）

// ---- authority
:: a1_chief
@label chief a1_chief_done
Chief: 阿哲啊！聽說你要幫陳家？
Chief: 我當里長二十年了，聽我的準沒錯：老人家跌倒，就是要多躺在床上、少走動！
Me: 里長這麼有經驗，說的一定對。我去跟阿公說！
> 陳阿公很聽話，整天躺在床上。兩天後，他的腿反而更沒力氣，晚上起床又差點跌倒。
Agong: ……躺越久，腳越軟。
> 里長很有地位，可是「有地位」不等於「有證據」。
@label agong a1_agong_weak
@note authority
@goto a1_next

:: a1_chief_done
Chief: 怎麼樣？老人家還是要多躺啦！

// ---- tradition (mini-game: clean up the lot)
:: a1_wang
@label wang a1_wang_done
Wang: 空地的垃圾喔？簡單啦！我們這條巷子三十年來都是這樣做：
Wang: 把垃圾清乾淨，再貼一張「禁止亂丟垃圾」的告示。一直都有用！
Me: 好，我現在就去清！
@mini trash debris
@put sign T:83 lane 6 14 -
@del t1
@del t2
@del t3
> 你清了一整天，還立好了告示牌。
> 第二天早上，空地又多了一堆垃圾……而且又是磚塊、水泥袋和油漆桶。
Wang: 奇怪，以前都有用啊……誰會丟這種東西？
> 「一直都是這樣做」不代表「這樣做有用」。三十年來，從來沒有人查過垃圾是誰丟的。
{{TRASH_BACK}}
@note tradition
@goto a1_next

:: a1_wang_done
Wang: 磚塊……水泥……真奇怪。

// ---- common sense
:: a1_lee
@label lee a1_lee_done
Lee: 路燈壞了？這是常識嘛：晚上那麼暗，很危險，大家晚上不要出門就好了。
Lee: 而且每天半夜都有大車開進來，轟隆轟隆的，吵死了。晚上關好門窗就對了。
Me: 有道理！我去告訴每一戶。
@tint night
@music quiet
> 當天晚上，整條巷子空蕩蕩的，每一戶都關緊了門。
@put cm2 chenma lane 35 7 -
@move cm2 22 7
> 陳媽媽下了夜班，一個人走進漆黑的巷子。一台沒開車燈的大卡車從黑暗中衝出來，差一點撞到她。
ChenMa: ……好可怕。以前晚上至少還有人在外面乘涼。
@move cm2 13 7
@del cm2
@tint none
@music warm
> 「大家都知道」的常識，反而讓巷子變得更空、更危險。那台卡車……半夜來這裡做什麼？
@note common_sense
@goto a1_next

:: a1_lee_done
Lee: 晚上不要出門，這是常識啊。

// ---- logic
:: a1_huang
@label huang a1_huang_done
Huang: 小宇的事？我用邏輯幫你想。
Huang: 第一：蹺課的小孩都是壞孩子。第二：小宇蹺課。所以：小宇是壞孩子。空地的垃圾，搞不好也是他丟的。
Huang: 叫巷子裡的小孩都離他遠一點，免得被帶壞。
Me: ……聽起來很有道理。好，我去跟大家說。
> 第二天開始，巷子裡沒有小孩願意和小宇說話了。
Yu: ……反正大家都說我是壞孩子。
> 推理的形式沒有錯，可是第一句話（前提）從來沒有人查證過。
@note logic
@goto a1_next

:: a1_huang_done
Huang: 邏輯就是邏輯，不會錯的。

// ---- halo effect
:: a1_star
@label star a1_star_done
Star: 嘿！我是小飛，籃球網紅，兩百萬人追蹤！我在這裡拍影片。
Me: 小飛！我是你的粉絲！我鄰居家有好多問題……你覺得該怎麼辦？
Star: 簡單！快樂家庭的祕密：每天早上五點起床跑步，再喝我代言的能量飲料！
Me: 小飛說的，一定沒錯！
@item 一箱能量飲料（花光了你的打工錢）
> 陳媽媽上完夜班，五點根本起不來。陳阿公的腳不能跑步。小宇把飲料放在門口，一瓶也沒喝。
> 小飛籃球打得很好，但這不代表他懂家庭的問題。
@note halo
@goto a1_next

:: a1_star_done
Star: 記得按讚、訂閱、開啟小鈴鐺！

// ---- the last night: Xiao Yu is missing
:: a1_night
@goal
@title 暑假的最後一晚|The last night of summer
@tint night
@music quiet
@put chenma chenma lane 6 5 a1_cm_night
@del yu
@del star
@del wang
@del chief
@del lee
@del huang
@del agong
@put yu yu lane 9 17 a1_found
@pos 5 5 down
@light 2.6
ChenMa: 阿哲！小宇不見了！他沒有在家，手機也不接！
ChenMa: 我要去上夜班了，阿公一個人在家……拜託你，幫我找找他！
@goal 🔦 在漆黑的巷子裡找到小宇。

:: a1_cm_night
ChenMa: 拜託你了……

:: a1_found
@light off
@label yu -
Me: 小宇！大家都在找你！你一個人在這裡做什麼？
Yu: ……出來透氣而已。家裡……算了，你不會懂。
Me: 我送你遊戲機、叫阿公躺床、清垃圾、叫大家晚上別出門……我做了這麼多……
Yu: 哥哥，你這五天，一直在「猜」我們需要什麼。
Yu: 你從來沒有問過我。一次也沒有。
@put agong agong lane 9 15 -
Agong: 小宇，回家吧。……年輕人，謝謝你。你有心，很好。
Agong: 可是幫人不能只靠熱心。巷子底的圖書館，你進去過嗎？
@pause talk1
Me: ……下星期一，我不去工廠了。這一次，我不要再猜。
@goto lib

// ======================= ACT 2: THE LIBRARY AND TWO DEGREES =======================
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
@door lane/univ lock 山城大學。先把圖書館裡的五本研究入門書找出來。
@put lib librarian library 8 6 b_lib !
{{SHELVES_BSW}}
@map library 8 10 up
> 隔天一早，你走進了巷子底的圖書館。
@goal 和圖書館的溫館員說話。

:: a2_agong
Agong: 去圖書館了？好，好。

:: a2_yu
Yu: 哥哥你在讀書喔？……奇怪的人。

:: b_lib
@label lib b_lib2
Lib: 歡迎！你看起來很煩惱。
Me: 我想幫隔壁一家人，試了好多辦法，全部失敗了。
Lib: 你都是怎麼想出那些辦法的？
Me: 直覺、里長說的、照傳統、靠常識、用邏輯……還有，相信了一個網紅。
Lib: 那些都是「沒有查證」的知道方法。社會工作需要的是另一種：**研究**。
Lib: 糟糕的是，研究入門的五本書，被人放亂了，和一堆亂七八糟的書混在一起。
Lib: 你一個一個書架找找看吧。找齊五本、讀完，就可以去申請巷子南邊的山城大學。
@goal 📚 在書架上找出五本研究入門書（{bswread} / 5）

:: b_lib2
@if bswread>=5 b_all_read
Lib: 一個一個書架找找看。小心那些看起來很吸引人的書喔。

:: b_book_after
@if bswdone=1 noop
@if bswread>=5 b_all_read
@goal 📚 在書架上找出五本研究入門書（{bswread} / 5）

:: noop
// nothing more to do

:: b_all_read
@door lane/univ reset
@put prof D:88 hall 7 3 bsw_exam !
{{STUDENTS}}
@if bswTries>=1 b_retake_ready
Lib: 五本都找到、也讀完了！你已經懂研究的基本功了。
Lib: 去山城大學吧。四年後的畢業考，每一張卡都要放對喔。
@goal 去山城大學（巷子南邊的紅色建築），找張教授。

:: b_retake_ready
Lib: 複習好了嗎？回大學找張教授重考吧。
@goal 回山城大學，找張教授重考。

{{BOOKS}}

:: bsw_exam
@label prof bsw_exam
@if bswTries>=1 bsw_go
Prof: 歡迎來到社工系，阿哲。……時間過得真快，一轉眼就四年了。
@goto bsw_go
:: bsw_go
Prof: 今天是學士畢業考：把每一張情境卡放進正確的分類。**每一張都要放對**，才能畢業。
@inc bswTries
@mini exam bswpass bsw
@if bswpass=1 bsw_pass
@music quiet
Prof: 還差一點。社工要幫助真實的人，所以一張都不能錯。
@goto bsw_c1
{{BSW_FAIL}}
:: bsw_back
Prof: 回圖書館，把標了 ! 的書再讀一次，再回來找我。
@label prof bsw_exam !
@goal 回圖書館複習標了 ! 的書，再回大學重考（已經考了 {bswTries} 次）
@map library 8 10 up

:: bsw_pass
@music bright
Prof: 全部正確！恭喜你，阿哲。
@item 🎓 社會工作學士 BSW
@set bswdone 1
Prof: 要替一整條巷子設計方案、評估成效，你還需要更多。研究所的書，溫館員已經幫你準備好了。
@goto msw

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
{{SHELVES_MSW}}
@put prof2 D:100 hall 7 3 msw_wait
{{STUDENTS}}
@map library 8 10 up
@goal 📚 讀完研究所的五本書（{mswread} / 5），再去大學找葉教授。

:: m_lib
@label lib m_lib2
Lib: 恭喜畢業！那些亂七八糟的書我都清掉了，換上研究所的五本書，標了 ! 的就是。

:: m_lib2
@if mswread>=5 m_all_read
Lib: 標了 ! 的書架，一共五本。

:: m_book_after
@if mswread>=5 m_all_read
@goal 📚 讀完研究所的五本書（{mswread} / 5），再去大學找葉教授。

:: m_all_read
@label prof2 msw_exam !
@if mswTries>=1 m_retake_ready
Lib: 五本都讀完了！去大學找葉教授吧。
@goal 去山城大學，找葉教授參加碩士畢業考。

:: m_retake_ready
Lib: 複習好了嗎？回大學找葉教授重考吧。
@goal 回山城大學，找葉教授重考。

:: msw_wait
ProfYe: 你好，我是葉教授。先把圖書館裡研究所的五本書讀完，再來找我。

:: msw_exam
@label prof2 msw_exam
ProfYe: 兩年的研究所，你在社福機構實習，也跟著我做了真正的研究。今天是碩士畢業考。
ProfYe: 先把研究步驟排好，再判斷每一張卡。一樣，**每一張都要對**。
@inc mswTries
@mini exam mswpass msw
@if mswpass=1 msw_pass
@music quiet
ProfYe: 還差一點。社工的方案會影響很多人的生活，不能出錯。
@goto msw_c1
{{MSW_FAIL}}
:: msw_back
ProfYe: 回圖書館，把標了 ! 的書再讀一次，再回來找我。
@label prof2 msw_exam !
@goal 回圖書館複習標了 ! 的書，再回大學重考（已經考了 {mswTries} 次）
@map library 8 10 up

:: msw_pass
@music bright
ProfYe: 全部正確。恭喜你，阿哲。
@item 🎓 社會工作碩士 MSW
ProfYe: 你準備好成為一位會用研究的社工了。回到需要你的地方吧。
@goto sw

// ======================= ACT 3: THIRTY DAYS =======================
:: sw
@save
@clear
@tint none
@music warm
@title 六年後|Six years later
@set days 30
@set ev 0
@set ev_truck 0
@set ev_carer 0
@set ev_survey 0
@set ev_research 0
@set consent 0
@set ivyu 0
@set ivag 0
@set sv 0
@set svon 0
{{LIGHTS_OFF}}
{{TRASH_ALL}}
@put mom jaymom lane 6 5 a3_mom !
@put chief chief lane 12 9 a3_chief
@put chenma chenma chen 3 4 a3_cm_hi
@put agong agong chen 8 4 a3_wait_agong
@put yu yu chen 8 2 a3_wait_yu
@put wang wang lane 20 5 a3_busy
@put lee lee lane 15 16 a3_busy
@put huang huang lane 33 16 a3_busy
@put liu liu lane 30 8 a3_busy
@put tsai v4 lane 26 17 a3_busy
@put lib librarian library 8 6 a3_lib_hi
@door lane/chen reset
@door lane/library reset
@door lane/univ lock 山城大學。你已經畢業了。
@door lane/jay lock 家。媽媽在門口。
@map lane 5 5 down
> 阿哲在城裡的社會福利中心當了幾年社工。這一天，他被派回自己長大的地方：和平巷。
> 路燈還是壞的。空地的磚塊和水泥袋，堆得比以前更高了。
@goal 和媽媽說話。

:: a3_mom
@label mom a3_mom2
Mom: 阿哲！你回來得正好。出大事了！
Mom: 市政府要把空地賣給開發商高董，蓋成停車場。高董在電視上說，垃圾都是巷子裡的小孩丟的，像小宇。
Mom: 里長在空地旁邊，快去問他！
@label chief a3_chief !
@goal 去空地旁邊找里長。

:: a3_mom2
Mom: 小宇現在讀國中了，還是常常蹺課……阿公也跌倒了好幾次。

:: a3_chief
@label chief a3_chief_hub
Chief: 阿哲，你是社工了吧？聽我說，市政府給我們三十天。
Chief: 三十天後開市民大會。要是我們拿不出比停車場更好的計畫，還有**證據**，空地就要變成停車場了。
Chief: 高董很會講話，又上過電視。光靠我說，沒有用。
Me: 三十天……好。這一次，我們用資料說話。
> 你在筆記本上寫下四件要查的事。每一件都要花時間，三十天不多，順序由你決定：
> 💬 陳家發生了什麼事？（訪談）　🌙 垃圾到底是誰丟的？（夜間觀察）
> 📊 巷子裡的人需要什麼？（問卷）　📗 研究怎麼說？（文獻探討）
@label chenma a3_chen !
@label liu a3_liu !
@label lib a3_lib !
@label chief a3_chief_hub !
@label mom a3_survey_start !
@goal {{HUB}}

:: a3_hub
@if days>=1 a3_hub2
@goto a3_timeup

:: a3_hub2
@goal {{HUB}}
@if ev>=4 a3_allcards

:: a3_allcards
@label chief a3_chief_hub !
> 四張證據卡都到手了。準備好了，就去找里長召開市民大會。

:: a3_timeup
> 三十天到了。不管準備好了沒有，市民大會就是今天。
@goto townhall

:: a3_chief_hub
Chief: 還剩 {days} 天。你手上有 {ev} 張證據卡。
@choice
? 「還沒，我要繼續蒐集資料。」 -> a3_chief_wait
? 「準備好了。召開市民大會吧！」 -> townhall

:: a3_chief_wait
Chief: 好，時間不多，加油！

:: a3_busy
> 他好像在忙。也許你蒐集問卷的時候，再來找他。

:: a3_cm_hi
ChenMa: 阿哲？你回來了！……里長在找你，先去找他吧。

:: a3_lib_hi
Lib: 阿哲！好久不見。

:: a3_wait_agong
Agong: 阿哲？長這麼大了。

:: a3_wait_yu
Yu: ……

// ---- investigation 1: the Chen family (ethics, then two interviews)
:: a3_chen
@if consent=1 a3_chen_again
ChenMa: 阿哲！你現在是社工了。電視上那個高董，說我們小宇在空地亂丟垃圾……我們怎麼辦？
Me: 我想了解你們家真正的情況。不過在開始之前——
@goto a3_s2_ask
:: a3_s2_ask
@choice
? 「我先說明我要做什麼、會怎麼使用你們說的話。要不要參加由你們決定，名字不會公開，隨時可以停。」 -> a3_s2_ok
? 「我偷偷用手機錄音，這樣你們說話比較自然。」 -> a3_s2_bad1
? 「我把你們的故事和照片貼上臉書，馬上就會有人支持你們！」 -> a3_s2_bad2

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
@set consent 1
ChenMa: 你肯先說清楚，我放心了。你去問阿公和小宇吧，他們願意的話。
Me: 這就是**知情同意**和**保密**。
@label chenma a3_chen_again
@label agong a3_iv_agong !
@label yu a3_iv_yu !
@goal {{HUB}} · 💬 訪談小宇和阿公

:: a3_chen_again
ChenMa: 阿公和小宇都在家。他們願意聊的話，就聊吧。

:: a3_iv_yu
@if ivyu=1 a3_iv_yu_done
> 訪談要花時間：三天。
@add days -3
@mini interview ivyu yu
@if ivyu=1 a3_iv_yu_ok
@label yu a3_iv_yu !
@goto a3_hub

:: a3_iv_yu_ok
@label yu a3_iv_yu_done
@goto a3_iv_check

:: a3_iv_yu_done
Yu: 謝謝你……真的有在聽。

:: a3_iv_agong
@if ivag=1 a3_iv_agong_done
> 訪談要花時間：三天。
@add days -3
@mini interview ivag agong
@if ivag=1 a3_iv_agong_ok
@label agong a3_iv_agong !
@goto a3_hub

:: a3_iv_agong_ok
@label agong a3_iv_agong_done
@goto a3_iv_check

:: a3_iv_agong_done
Agong: 小宇是個好孩子。

:: a3_iv_check
@if ivyu=1 a3_iv_check2
@goto a3_hub
:: a3_iv_check2
@if ivag=1 a3_iv_both
@goto a3_hub

:: a3_iv_both
@set ev_carer 1
@inc ev
@music bright
Me: 小宇不是懶。他是一個**年輕照顧者**：每天半夜起來照顧在黑暗走廊上跌倒的阿公。
Me: 阿公跌倒，也不是因為「年紀大」，而是晚上太暗、沒有人陪。兩個問題，其實是同一個問題。
> 🗂️ 獲得證據卡：💬 訪談：小宇與阿公。這是**質性資料**。
@note qualitative
@music warm
@goto a3_hub

// ---- investigation 2: the night watch
:: a3_liu
@if ev_truck=1 a3_liu_done
Liu: 你在查空地的垃圾？我是護理師，上夜班，常常半夜才回家。
Liu: 我家的陽台正對著空地。要不要找一個晚上，在我家陽台觀察？
Me: 好！用**觀察法**：照時間記下看到的每一件事，不靠猜。
> 觀察要花時間：三天。
@add days -3
@tint night
@music quiet
@mini stakeout seen
@tint none
@music warm
@if seen=1 a3_liu_ok
Liu: 沒記到嗎？卡車通常每隔幾天才來一次。你可以再試一次，不過又要花幾天喔。
@label liu a3_liu !
@goto a3_hub

:: a3_liu_ok
@set ev_truck 1
@inc ev
@label liu a3_liu_done
@note observation
> 🗂️ 獲得證據卡：🚚 夜間觀察紀錄（凌晨 2:14，工程卡車傾倒建築廢料）。
Liu: 那台卡車……車身上的公司名字，跟高董的建設公司一樣耶。
@goto a3_hub

:: a3_liu_done
Liu: 紀錄要收好，那是證據。

// ---- investigation 3: the survey (design choice, then five households)
:: a3_survey_start
@if svon=1 a3_survey_go
Mom: 你要問巷子裡大家的意見？我幫你一起問！
Me: 巷子裡的人，到底需要什麼？我要怎麼蒐集資料？
@goto a3_design_ask
:: a3_design_ask
@choice
? 「只問我媽就好，她認識每一個人。」 -> a3_design_bad1
? 「每一戶都填一份簡短的不記名問卷（量化），再配合陳家的訪談（質性）。」 -> a3_design_ok
? 「不用問了，我知道大家要什麼。」 -> a3_design_bad2

:: a3_design_bad1
> 只問一個人，就只聽到一個人的看法。媽媽不等於全巷子。
@pause oops
@goto a3_design_ask

:: a3_design_bad2
> 這句話，你六年前也說過。
@pause oops
@goto a3_design_ask

:: a3_design_ok
@set svon 1
Me: 量化告訴我「有多少」，質性告訴我「為什麼」。這叫**混合研究方法**。這份問卷也是一份**需求評量**。
@note mixed_methods
@note needs_assessment
@label wang a3_sv_wang !
@label lee a3_sv_lee !
@label huang a3_sv_huang !
@label tsai a3_sv_tsai !
@label mom a3_sv_mom !
@goto a3_survey_go

:: a3_survey_go
@goal {{HUB}} · 📊 問卷 {sv} / 5 戶（每戶一天）

:: a3_sv_wang
@label wang a3_sv_done
@add days -1
Me: 王阿姨，這是一份不記名的問卷，大約三分鐘。要不要填，由您決定。
Wang: 好啊！我勾：路燈太暗、空地垃圾、孩子放學後沒地方去。我退休前是小學數學老師喔。
@goto a3_sv_next

:: a3_sv_lee
@label lee a3_sv_done
@add days -1
Me: 李先生，這是一份不記名的問卷，要不要填由您決定。
Lee: 不記名喔？好。我勾：路燈太暗、空地垃圾。我爸也很少出門，他怕跌倒。
@goto a3_sv_next

:: a3_sv_huang
@label huang a3_sv_done
@add days -1
Me: 黃伯伯，可以請您填一份不記名的問卷嗎？不填也沒關係。
Huang: 問卷？……好吧。路燈太暗。我孫子放學後也沒地方去。我以前說小宇的那些話……唉。
@goto a3_sv_next

:: a3_sv_tsai
@label tsai a3_sv_done
@add days -1
Me: 蔡太太，這是一份不記名的問卷，要不要填由您決定。
Tsai: 我剛搬來。最怕晚上回家，巷子太暗了。還有那片空地，好多垃圾和蚊子。
@goto a3_sv_next

:: a3_sv_mom
@label mom a3_sv_done
@add days -1
Mom: 當然要填！路燈太暗、空地垃圾、孩子放學後沒地方去。還有，我想多認識鄰居。
@goto a3_sv_next

:: a3_sv_done
> 謝謝你的協助！問卷已經收好了。

:: a3_sv_next
@inc sv
@if sv>=5 a3_sv_all
@goto a3_hub

:: a3_sv_all
@set ev_survey 1
@inc ev
> 📊 5 / 5 戶：巷子太暗。　4 / 5 戶：空地不安全。　3 / 5 戶：孩子放學後沒地方去。
> 🗂️ 獲得證據卡：📊 五戶問卷結果。這是**量化資料**。
@note quantitative
@goto a3_hub

// ---- investigation 4: the literature (source detective)
:: a3_lib
@if ev_research=1 a3_lib_done
Lib: 阿哲！好久不見。聽說高董說「路燈、菜園都沒用」？我們來查查研究怎麼說。
Lib: 不過要小心：網路上的東西，不是每一個都可信。
> 文獻探討要花時間：三天。
@add days -3
@mini sources src
@if src>=8 a3_lib_ok
@label lib a3_lib !
@goto a3_hub

:: a3_lib_ok
@set ev_research 1
@inc ev
@label lib a3_lib_done
@note lit_review
> 🗂️ 獲得證據卡：📗 四篇可靠的研究（跌倒預防、路燈、空地綠化、課後方案）。
@goto a3_hub

:: a3_lib_done
Lib: 研究都幫你整理好了。市民大會加油！

// ======================= TOWN HALL =======================
:: townhall
@goal
@title 市民大會|Town hall
@clear
{{LIGHTS_OFF}}
{{TRASH_ALL}}
@put chief chief lane 12 9 -
@put kao v8 lane 13 11 -
@put agong agong lane 15 9 -
@put yu yu lane 16 10 -
@put chenma chenma lane 14 11 -
@put wang wang lane 17 9 -
@put lee lee lane 17 10 -
@put huang huang lane 18 11 -
@put liu liu lane 16 11 -
@put mom jaymom lane 12 11 -
@map lane 14 8 down
@music quiet
Chief: 各位鄰居，今天要決定空地的未來。高董，請。
Kao: 大家好，我是高董，常上電視的那個。停車場對大家最好，我有四個理由。
@mini townhall pts
@music warm
Chief: 好，請高董和阿哲都說完了。阿哲，那你的計畫是什麼？
Me: （最好的研究證據，加上我的專業經驗，再加上大家的想法和需要。）
Agong: 我以前很會種菜，也會下棋。
Wang: 我退休前是小學數學老師喔！
@goto th_plan
:: th_plan
@choice
? 「每一家發一箱小飛代言的能量飲料！」 -> th_plan_bad1
? 「我已經都設計好了，大家照我的計畫做就好。」 -> th_plan_bad2
? 「我們一起做：舉發傾倒廢料的卡車、修好路燈；空地變菜園，阿公教大家種菜；王老師帶課後功課班；長輩每週一起做平衡運動；居家照顧員晚上來幫阿公，讓小宇可以睡覺。」 -> th_plan_ok

:: th_plan_bad1
> ……六年前那個夏天，你已經試過了。
@pause oops
@goto th_plan

:: th_plan_bad2
> 大家安靜地聽完，沒有人舉手。沒有案主的聲音，計畫就只是你一個人的計畫。
@pause oops
@goto th_plan

:: th_plan_ok
Everyone: ……
Me: 這就是**實證為基礎的實務**：研究證據、專業經驗，加上大家的價值和想法。
@note ebp
Chief: 好，投票！
@if pts>=4 end_full
@if pts>=2 end_half
@goto end_lost

// ======================= ENDINGS =======================
:: end_full
@music bright
> 投票結果：全場舉手支持。高董的公司因為傾倒廢料被開罰，停車場計畫取消了。
@title 一年後|One year later
@clear
{{LIGHTS_ON}}
{{GARDEN}}
@put agong agong lane 4 13 -
@put yu yu lane 8 13 -
@put wang wang lane 9 14 -
@put lee lee lane 6 16 -
@put chenma chenma lane 12 8 ev_ask !
@map lane 12 10 up
> 路燈修好了。空地變成了「和平菜園」。下午四點，王老師在菜園旁的桌子帶孩子寫功課。
> 晚上有居家照顧員來幫阿公，小宇終於可以好好睡覺了。
@goal 和陳媽媽談談：方案真的有用嗎？

:: ev_ask
@label chenma -
ChenMa: 阿哲，大家都說方案很成功！市政府要你寫報告？
Me: 對。要怎麼證明方案真的有用？
@goto ev_ask2
:: ev_ask2
@choice
? 「我們辦了 96 次功課班。數字這麼大，一定成功！」 -> ev_bad1
? 「大家看起來都很開心，就代表有用。」 -> ev_bad2
? 「比較方案前後的成效，也和情況相似、但沒有方案的光明巷比較。」 -> ev_ok

:: ev_bad1
> 那是**產出**：你「做了多少」。市政府想知道的是**成效**：大家的生活「改變了多少」。
@pause oops
@goto ev_ask2

:: ev_bad2
> 「看起來」不是資料。也許只是剛好天氣變好了呢？
@pause oops
@goto ev_ask2

:: ev_ok
@note output_outcome
@note comparison_group
> 📊 小宇：一個月蹺課 12 天 → 1 天。數學從 38 分進步到 71 分。
> 📊 阿公：跌倒從半年 4 次 → 0 次。　📊 晚上在巷子散步的鄰居：幾乎沒有 → 每晚十幾個人。
> 📊 比較組「光明巷」：同樣的一年，幾乎沒有改變。
Me: 前後有差別，和比較組也有差別。現在我比較有把握：是這個方案帶來了改變。
Yu: 哥哥。……謝謝你這次有先問我。我以後也想當社工。
Agong: 年輕人，這一次，你沒有用猜的。有心，再加上研究，才真的幫得上忙。
@pause final
@end

:: end_half
@music warm
> 投票結果：一半一半。最後的決定是：空地的一半蓋停車場，另一半留給大家。
@title 一年後|One year later
@clear
{{LIGHTS_ON}}
@put g1 X:3 lane 3 12 -
@put g2 X:3 lane 5 12 -
@put agong agong lane 4 13 -
@put yu yu lane 6 13 half_yu !
@map lane 6 10 down
> 路燈修好了，菜園小小的。有些事情做到了，有些證據，那天你沒有拿出來。
@goal 和小宇說話。

:: half_yu
@label yu -
@if ev_carer=1 half_yu_good
Yu: ……學校還是一直打電話來。半夜還是我起來扶阿公。沒有人知道。
Me: （那天，我沒有聽到小宇真正的故事。）
@goto half_end
:: half_yu_good
Yu: 現在晚上有照顧員來幫阿公，我可以睡覺了。謝謝你，哥哥。
@goto half_end
:: half_end
Me: 如果我那時候多蒐集一張證據……結果會不會不一樣？
@goto replay

:: end_lost
@music quiet
> 投票結果：停車場通過了。
@title 半年後|Six months later
@clear
{{LIGHTS_OFF}}
@put agong agong lane 12 9 lost_agong !
@map lane 12 11 up
> 空地鋪上了柏油。半夜，卡車改到別的巷子倒垃圾了。
@goal 和阿公說話。

:: lost_agong
@label agong -
Agong: 阿哲，你有心，大家都知道。可是那天，高董講什麼，大家就信什麼。
Me: ……因為我手上沒有足夠的證據。
@goto replay

:: replay
@choice
? 「讓我重來這三十天。」 -> sw
? 「結束遊戲，和大家討論。」 -> replay_end

:: replay_end
@pause final
@end
'''

GARDEN = '''@put g1 X:3 lane 3 12 -
@put g2 X:3 lane 5 12 -
@put g3 X:3 lane 3 14 -
@put g4 X:3 lane 5 14 -
@put f1 X:4 lane 8 11 -
@put f2 X:4 lane 3 16 -
@put f3 X:4 lane 9 16 -
@put desk D:72 lane 8 14 -'''

SCRIPT = (SCRIPT
          .replace('{{LANE_MID}}', LANE_MID)
          .replace('{{LIGHTS_OFF}}', lights(False))
          .replace('{{LIGHTS_ON}}', lights(True))
          .replace('{{TRASH}}', trash())
          .replace('{{TRASH_ALL}}', trash(True))
          .replace('{{TRASH_BACK}}', trash(True))
          .replace('{{GARDEN}}', GARDEN)
          .replace('{{SHELVES_BSW}}', shelves('bsw'))
          .replace('{{SHELVES_MSW}}', shelves('msw'))
          .replace('{{STUDENTS}}', hall_students())
          .replace('{{BOOKS}}', book_blocks())
          .replace('{{BSW_FAIL}}', exam_fail_chain('b'))
          .replace('{{MSW_FAIL}}', exam_fail_chain('m'))
          .replace('{{HUB}}', HUB_GOAL))
assert '{{' not in SCRIPT

"""The story script, pauses and passwords for 青溪颱風夜. build_data.py imports this file.
Change the passwords and the discussion questions here, then run build_data.py.
(The opening password is in ../index.html, look for GATE_PASSWORD.)"""

# Password that unlocks Path 2 after the discussion (also works as a jump code on the title screen).
DISCUSS_PASSWORD = 'ABCD'

DISCUSS_QUESTION = '''<p><b>需求為本的做法帶來了哪些好處？為什麼一年以後，青溪里反而什麼都沒有留下？</b></p>
<p class="en">What did the need-based approach do well? Why, one year later, was nothing left in Clear Creek?</p>'''

FINAL_QUESTION = '''<p><b>如果你是青溪里的社工，你會選哪一條路？外部資源（例如縣府的經費）在以資產為基礎的社區發展中，應該扮演什麼角色？</b></p>
<p class="en">If you were Clear Creek's social worker, which path would you take? In asset-based community development, what role should outside resources play?</p>'''

PAUSES = {
    'discuss1': {
        'head': '⏸ 討論時間 Discussion',
        'code': DISCUSS_PASSWORD,
        'html': DISCUSS_QUESTION + '''<p class="small">請放下手機，和旁邊的同學討論。老師公布密碼後，輸入密碼繼續。<br>
Put your phone down and discuss with your classmates. Enter the password from your teacher to continue.</p>'''},
    'over': {
        'head': ' ', 'over': True, 'ready': True, 'go': '再試一次 Try Again',
        'html': '''<div class="gameover">GAME OVER</div>
<p>這樣做，社區的資產沒有被看見，居民也沒有成為貢獻者。</p>
<p class="en">The community's assets were not seen, and residents did not become contributors.</p>
<p class="small">回到「第二條路」的開頭，再試一次。 Try again from the start of Path 2.</p>'''},
    'final': {
        'head': '💬 最後討論 Final Discussion', 'ready': True, 'go': '看結局 Finish',
        'html': FINAL_QUESTION + '<p class="small">和旁邊的同學討論，再按「看結局」。 Discuss with your classmates, then tap Finish.</p>'},
}

JUMPS = {DISCUSS_PASSWORD: 'abcd'}

SCRIPT = r'''
// ======================= OPENING: THE LECTURE HALL =======================
:: intro
@save
@clear
@tint none
@music quiet
@player me
@title 社會工作概論，星期二早上|Introduction to Social Work · Tuesday morning
{{CLASSROOM}}
@put teacher D:88 classroom 10 2 cls_teacher
@map classroom 16 18 up
Teacher: Good morning, everyone. Today we're talking about community development: Chapter 6.
Teacher: Kretzmann and McKnight describe two paths. One starts from a community's needs and deficits...
Teacher: ...and the other starts from the assets and capacities that are already there.
> 台上的老師用英文講得飛快。你看了看四周，六十幾位同學，有一半已經在偷偷打哈欠。
@goal 和旁邊的同學說說話（頭上有 ! 的同學）。

:: cls_teacher
Teacher: In a need-based approach, outside experts survey the problems and deliver services from the top down...
> 你努力抄筆記，可是「top down」後面那一句，你完全沒聽懂。

:: cls_a
@label s{{A}} cls_done
Classmate: deficits 是什麼意思？……我只聽懂 community。
Classmate: 老師講好快，我連課本第六章的標題都還沒翻到。
@goto cls_count

:: cls_b
@label s{{B}} cls_done
Classmate: 我昨天打工到半夜一點……英文聽起來好像催眠曲。
> 他說完，就趴在桌上睡著了。
@goto cls_count

:: cls_c
@label s{{C}} cls_done
Classmate: 欸，你聽得懂嗎？asset、capacity、deficit……這些字我查了也記不住。
Classmate: 算了，我先睡五分鐘，等一下借我筆記。
@goto cls_count

:: cls_done
> Zzz……

:: cls_count
@inc talked
@if talked>=3 cls_storm

:: cls_storm
Teacher: ...so if we only see a community through its needs, what happens to the people who live there?
> 教室裡一片安靜。一大半的同學都已經趴在桌上了。
> 你的眼皮也越來越重……
@tint storm
@music tick
Phone: 【颱風警報】強烈颱風今晚登陸，中部山區將有豪雨。
> 窗外忽然閃過一道白光。轟隆！
@tint night
> 啪！整間教室停電了。
Teacher: Everyone, stay calm, the power will be back in a—
@music stop
> 一片黑暗裡，你聽到風聲、雨聲……還有公車的煞車聲？
@goto nbcd

// ======================= PATH 1: STARTING FROM NEEDS =======================
:: nbcd
@save
@clear
@tint none
@music warm
@player me
@title 第一條路：從「需求」開始|Path 1 · Starting from needs
@door village/tunnelN lock 隧道口用木板封著。
@door village/tunnelS lock 隧道口用木板封著。
@put driver D:86 village 32 7 n_driver !
@put zhou D:85 village 29 7 -
@put stop T:83 village 33 5 c1_stop
@put an an village 33 7 an_hint
@map village 33 8 up
@follow an
> 你睜開眼睛。眼前不是教室，而是一個山裡的公車站。
An: 欸？你是誰？剛剛明明只有我一個人下車……
> 你結結巴巴地解釋：你在上社會工作概論，教室停電了，然後……
An: 然後你就掉進來了？……好吧，好像只有我看得到你。司機完全沒看到你。
An: 我是小安，今天第一天來青溪里當社區社工。你就跟著我吧。
@goal 跟著小安，和公車司機說話。

:: an_hint
An: 頭上有 ! 的人或東西，我們去看看。

:: n_driver
@label driver n_driver2
Driver: 到了，青溪里，終點站。你是新來的社工吧？
Driver: 這條路線一天兩班，客運說一直虧錢。下個月……可能就停了。
Driver: 那位穿西裝的，是縣政府的人。
@label zhou n_zhou !
@goal 和縣府的周專員說話（司機左邊）。

:: n_driver2
Driver: 氣象說有颱風要來，你自己小心喔。

:: n_zhou
@label zhou -
Zhou: 你就是新來的社區社工？我是縣府的周專員。這是我們請專家做的調查報告。
@item 縣府報告 The County Report
> 報告封面寫著：「青溪里：一個需求很多的衰退社區」。
> 人口外流、老化、國小廢校、雜貨店關門、公車虧損、獨居長者沒吃飯……
An: 專家的報告寫得這麼清楚，照縣府的方法做，應該不會錯吧？
Zhou: 很好。你只要把每一戶的「需求」調查清楚，剩下的交給縣府和專家。
@move zhou 34 7
@del zhou
@note nbcd
An: 走吧，我們去做需求調查。
@set survey 0
@put lin lin lin 5 3 n_lin !
@put li li coop 5 3 n_li !
@put chen chen chen 5 3 n_chen !
@goal 跟著小安做需求調查（{survey}/3）：林阿姨家（左上）、茶農合作社（右上）、陳奶奶家（過橋）。

:: c1_stop
> 公車站牌：「青溪里　每日 7:10、16:40」。下面貼著一張紙：「本路線將於下月停駛」。

:: n_lin
@label lin n_lin2
An: 林阿姨您好，我是新來的社工，來做需求調查。您一個人住嗎？有沒有慢性病？
Lin: 我？我以前在醫院當了三十年護理師……
An: 好的。（寫下：獨居、高齡、需要居家護理。）下一題……
Lin: ……好吧。你說我需要什麼，就是什麼吧。
> 你注意到，小安的表格上只有兩個欄位：「問題」和「需要」。
@goto n_count

:: n_lin2
Lin: 有專業的人來照顧，也好啦……

:: n_li
@label li n_li2
An: 李大哥，合作社最近有什麼困難嗎？
Li: 茶價不好，年輕人又少……
An: （寫下：產業沒落、收入不足、需要轉業輔導。）縣府有轉業補助，我幫你們申請！
Li: 轉業？我們種了一輩子的茶……算了，有補助總比沒有好。
@goto n_count

:: n_li2
Li: 補助申請好了，就通知我們吧。

:: n_chen
@label chen n_chen2
An: 奶奶，您一個人住在溪對面，很危險吧？
Chen: 我在這條溪邊住了八十二年，哪裡會淹水、哪裡有路，我都知道……
An: （寫下：高齡獨居、交通不便、高血壓。）縣府可以幫您申請城裡的安養機構，那裡有專業照顧。
Chen: 機構……喔。那我的家呢？
> 陳奶奶好像還想說什麼，最後沒有說出口。
@goto n_count

:: n_chen2
Chen: 城裡的機構啊……

:: n_count
@inc survey
@goal 跟著小安做需求調查（{survey}/3）：林阿姨家、茶農合作社、陳奶奶家。
@if survey>=3 n_survey_done

:: n_survey_done
An: 好了！需求清單完成：一共三十七項需求。我傳給周專員。
> 小安按下傳送鍵。手機螢幕忽然閃了一下。
Phone: 【颱風警報】強烈颱風今晚登陸，中部山區將有豪雨，請民眾提早做好準備。
@goto n_storm

:: n_storm
@save
@clear
@tint storm
@music tick
@player me
@title 颱風夜|Typhoon Night
@zone in1 school 0 0 15 10 c2_indoor
@zone storm village 0 0 36 26 c2_out
@put chief chief school 7 3 n_chief !
@put mei mei school 3 6 -
@put lin lin school 10 4 -
@put hao hao school 4 4 -
@put an an school 6 6 an_hint
@map school 7 7 up
@follow an
> 晚上九點，停電了。村民陸續來到活動中心避難。
@goal 和黃里長說話。

:: c2_out
@tint storm

:: c2_indoor
@tint night

:: n_chief
@label chief -
Chief: 社工！橋被沖壞了，陳奶奶在溪的對岸，電話一直打不通！
Hao: 我可以在群組問問大家，有沒有人知道別的路……
An: 不用了，太危險了。專業的事交給專業的人。我已經通報縣府，我們等救援隊。
Lin: 我是護理師，我可以——
An: 林阿姨，您年紀大了，先休息吧。救援隊有專業的醫護人員。
> 大家安靜下來，一起等。外面的風雨越來越大。
> 你想開口，可是在這個世界裡，只有小安聽得到你……而小安正忙著打電話給縣府。
@title 第二天中午|The next day, at noon
> 救援隊終於到了。消防隊員用橡皮艇，把陳奶奶從溪的對岸接出來。
> 她的血壓太高，被直接送進城裡的醫院。
Chief: 還好救援隊來了。專業的，就是不一樣。
@goto n_aid

:: n_aid
@save
@clear
@tint none
@music bright
@player me
@title 救援物資湧進青溪里|The aid pours in
@put zhou D:85 village 21 5 n_zhou2 !
@put an an village 22 7 an_hint
@map village 21 8 up
@follow an
@goal 和周專員說話。

:: n_zhou2
@label zhou n_zhou3
Zhou: 好消息！縣府撥了一大筆緊急經費。專家團隊已經把三十七項需求全部列入計畫。
Zhou: 城裡的送餐公司，每天中午送便當給每一位長輩。
Zhou: 專業的居家護理團隊，每週來兩次。
Zhou: 縣府還包了一台接駁車。公車停駛？完全不用擔心。
Zhou: 救災物資也已經堆滿活動中心了！
An: 太好了！才幾天，所有問題都有人解決了！
@set pros 0
@put mei mei village 16 8 n_p_mei !
@put driver D:86 village 30 7 n_p_driver !
@put chief chief village 12 7 n_p_chief !
@put lin lin village 7 7 n_p_lin !
@goal 看看村民們的反應（{pros}/4）。

:: n_zhou3
Zhou: 有任何需求，打電話給縣府就對了。

:: n_p_mei
@label mei n_p_done
Mei: 每天中午都有熱騰騰的便當送到家門口，好方便！
@goto n_p_count

:: n_p_driver
@label driver n_p_done
Driver: 縣府出錢的接駁車，又新又有冷氣！
@goto n_p_count

:: n_p_chief
@label chief n_p_done
Chief: 物資多到倉庫都放不下了，我這輩子沒看過這麼多東西！
@goto n_p_count

:: n_p_lin
@label lin n_p_done
Lin: 護理團隊的血壓計是電子的，比我那台舊的厲害多了。
@goto n_p_count

:: n_p_done
> 大家都笑得很開心。

:: n_p_count
@inc pros
@goal 看看村民們的反應（{pros}/4）。
@if pros>=4 n_p_end

:: n_p_end
An: 你看，外部的資源又快、又專業、又充足。這就是需求為本的好處吧？
> 看起來，真的什麼問題都解決了。
@goto n_year

:: n_year
@save
@clear
@tint sepia
@music quiet
@player me
@title 一年後|One year later
@set yr 0
@put an an village 22 7 an_hint
@put chief chief village 21 5 n_y_chief !
@put lin lin village 7 7 n_y_lin !
@put wu wu village 13 6 n_y_wu !
@put li li village 30 7 n_y_li !
@put mei mei village 16 8 n_y_mei !
@map village 21 8 up
@follow an
> 一年過去了。
@goal 看看青溪里現在怎麼樣了（{yr}/5）。

:: n_y_chief
@label chief n_y_done
Chief: 縣府的經費用完了。下個月起，送餐、護理團隊、接駁車……全部停止。
Chief: 這一年來，大家都習慣等縣府送東西來。現在，我也不知道該怎麼辦了。
@goto n_y_count

:: n_y_lin
@label lin n_y_done
Lin: 我已經一年沒幫鄰居量血壓了。反正有專業的人會來。
Lin: 現在他們不來了，我才發現，我連誰最需要照顧都不知道了。
@goto n_y_count

:: n_y_wu
@label wu n_y_done
Wu: 燈籠夜？去年縣府請了城裡的表演團體來辦晚會。今年沒有經費，就停辦了。
Wu: 沒有人來學做燈籠。這門手藝，大概就到我為止了。
@goto n_y_count

:: n_y_li
@label li n_y_done
Li: 合作社解散了。大家都領了轉業補助，貨車也賣了。
Li: 現在補助停了，茶園也荒了。
@goto n_y_count

:: n_y_mei
@label mei n_y_done
Mei: 阿豪回臺北了。他說這裡沒有人需要他，群組一整年都沒人講話。
Mei: 陳奶奶出院以後，就直接被送到城裡的安養機構。她的房子到現在還空著。
@goto n_y_count

:: n_y_done
> ……

:: n_y_count
@inc yr
@goal 看看青溪里現在怎麼樣了（{yr}/5）。
@if yr>=5 n_y_end

:: n_y_end
An: 我們解決了報告上的每一個問題……
An: 可是一年過去，青溪里自己什麼都沒有長出來。外面的援助一停，大家反而什麼都不會了。
@note dependency
@quiz qn
An: （小安轉過頭看著你。）你說……我是不是從一開始，就看錯了這個村子？
@pause discuss1
@goto abcd

// ======================= PATH 2: STARTING FROM ASSETS =======================
:: abcd
@save
@clear
@tint sepia
@music quiet
@player me
@title 時間倒轉，回到三天前|Rewind · three days earlier
@tint none
@music warm
@title 第二條路：從「資產」開始|Path 2 · Starting from assets
@door village/tunnelN lock 隧道口用木板封著。陳奶奶說過，這條舊水圳隧道已經很多年沒人走了。
@door village/tunnelS lock 隧道口用木板封著。
@put zhou D:85 village 29 7 a_zhou !
@put stop T:83 village 33 5 c1_stop
@put an an village 33 7 an_hint
@map village 33 8 up
@follow an
An: 你也記得，對吧？那一年……
An: 這一次，我需要你的幫忙。每到重要的時候，告訴我該怎麼做。
@goal 和周專員說話。

:: a_zhou
@label zhou -
Zhou: 你就是新來的社工？這是專家的調查報告：青溪里是「一個需求很多的衰退社區」。
Zhou: 三天後是燈籠夜。拿不出像樣的社區計畫，我就停掉經費，把長輩送去城裡的機構。
@move zhou 34 7
@del zhou
An: 又是這份報告……（小安看著你。）我的第一步，該怎麼做？
@choice
? 照著報告，把每一戶的需求調查清楚，交給縣府處理。 -> go_needs
? 先走進社區，找出居民和社區已經有的資產。 -> a_start
? 我自己先寫一份完整的計畫書，交給周專員。 -> go_plan

:: go_needs
> 小安又拿出了需求調查表……
> 一年後，援助停了，青溪里什麼都沒有留下。這條路，你已經看過了。
@pause over
@goto abcd

:: go_plan
> 小安熬夜寫了一份五十頁的計畫書。周專員說寫得很好。
> 可是從頭到尾，沒有一位村民參與。燈籠夜那天，沒有人知道計畫在寫什麼，也沒有人願意出來做。
@pause over
@goto abcd

:: a_start
An: 對！這一次，我們從「已經有的」開始。
@put chief chief school 7 3 a_ch1 !
@goal 到村子中間的社區活動中心（舊國小，紅色大屋頂）找黃里長。

:: a_ch1
@label chief c1_chief_wait
@put kitchen D:72 school 11 2 a_kitchen !
@put lin lin lin 5 3 a_lin !
@put wu wu wu 5 3 a_wu !
@put hao hao village 12 12 a_hao !
@put li li coop 5 3 a_li !
@put chen chen chen 5 3 a_chen !
@put mei mei village 14 8 c1_mei
Chief: 你就是新來的社工？歡迎、歡迎！我是黃里長。
Chief: 周專員給你看報告了吧？唉，他只看到我們缺什麼。
An: 里長，我想先好好認識這個**社區**。
An: 課本說，社區有四項基本要素：個人、團體或組織；地方；社會互動；還有心理認同或歸屬。
Chief: 喔……所以社區不只是一塊地，還是一群彼此有來往、覺得「這裡是我家」的人。
@note community
An: 而且**社區工作**不只看一個人的問題，也看整個環境和社會結構。
@note community_work
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
Mei: 你們在找村子的資產？去溪對面問問陳奶奶吧，過橋就到了。她知道村裡所有的故事。
Mei: 還有，舊學校裡面的廚房，你們看過了嗎？

:: a_kitchen
@label kitchen a_kitchen2
> 舊國小的廚房：兩口大鍋、瓦斯爐，隔壁教室還可以坐五十個人吃飯。
An: 學校關了，可是廚房和教室都還在。這是**地方與設施**。
@item 資產卡：舊學校的廚房和教室（地方與設施）
@goto a_count

:: a_kitchen2
> 大鍋擦得很乾淨，好像隨時可以再煮一頓大餐。

:: a_lin
Lin: 你是新來的社工？來，先量個血壓。
Lin: 我在醫院當了三十年護理師。退休以後，每個星期天幫鄰居量血壓。
An: （小安小聲問你：）我該怎麼回應林阿姨？
@choice
? 「阿姨，您一個人住，有什麼需要我們幫您申請的嗎？」 -> a_lin_bad
? 「阿姨，您這麼會照顧人，願意和我們一起照顧村裡的長輩嗎？」 -> a_lin_good

:: a_lin_bad
Lin: ……喔。原來在你眼裡，我也只是一個「需要被照顧的老人」。
> 林阿姨默默收起了血壓計。從那天起，她再也沒有幫鄰居量過血壓。
@pause over
@goto abcd

:: a_lin_good
@label lin a_lin2
Lin: 我？當然願意！誰的血壓高、誰最近吃不下飯，我都知道。
An: 林阿姨，您是這個村子的健康守護者！
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
An: 陳奶奶，您就是一本活的地圖。
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
Chief: 六個？你們真的找到六個？
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

:: ch2
@clear
@tint storm
@music tick
@player me
@title 颱風夜（第二條路）|Typhoon Night · Path 2
@set team 0
@set kid 0
@set tun 0
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
@put an an school 6 6 an_hint
@zone storm village 0 0 36 26 c2_out
@zone dark tunnel 0 0 18 9 c2_in
@zone in1 school 0 0 15 10 c2_indoor
@zone in2 wu 0 0 11 8 c2_indoor
@zone in3 coop 0 0 11 8 c2_indoor
@zone in4 lin 0 0 11 8 c2_indoor
@zone in5 chen 0 0 11 8 c2_indoor
@map school 7 7 up
@follow an
> 晚上九點。狂風暴雨打在活動中心的窗戶上。
> 停電了。村民拿著手電筒，陸續來到活動中心避難。
@goal 和黃里長說話。

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
An: （小安看著你。）這一次，我們該怎麼做？
@choice
? 等縣府的救援隊明天來處理。 -> c2_wait
? 把村民召集起來，一起想辦法。 -> c2_gather

:: c2_wait
Chief: 也是，這種事還是交給專業的人……
> 大家等了一整夜。第二天中午，救援隊才終於到達。陳奶奶的血壓太高，被送進城裡的醫院。
> 青溪里，又走回了需求為本的老路。
@pause over
@goto abcd

:: c2_gather
Chief: 好！大家聽我說——
An: （小安小聲問你：）接下來，我該怎麼跟大家說？
@choice
? 「我是社工，我來分配工作，大家照我說的做。」 -> c2_boss
? 「這是大家的村子，要怎麼做，由大家一起決定。我來幫忙。」 -> c2_gather_ok

:: c2_boss
> 小安開始分配工作。村民們互看了一眼。
Li: 你才來一天，就要指揮我們？
> 大家照著做，卻沒有人說出自己知道的事，包括那條舊水圳隧道。
> 天亮以後，救援隊才到。陳奶奶被送進了醫院。
@pause over
@goto abcd

:: c2_gather_ok
An: 這是大家的村子。要怎麼做，由大家一起決定。我會幫忙，但不會替大家決定。
@note self_det
Everyone: 好！
Chief: 第一件事：我們要確定每一戶都平安。
@label hao c2_hao !
@goal 請阿豪用村民群組確認大家是否平安。

:: c2_chief_wait
Chief: 大家都在等你們。我們一起想辦法！

:: c2_mei
Mei: 我家阿弟……剛剛說要去找小狗，到現在還沒回來……

:: c2_mei2
Mei: 謝謝你們找到阿弟！

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
An: 陳奶奶！我們來接您了！
Chen: 你們……怎麼過來的？橋不是斷了嗎？
An: 走您告訴我的那條舊水圳隧道。
@put lin lin chen 7 3 -
Lin: 奶奶，我先幫您量血壓……有點高，先把藥吃了。
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

:: ch3
@clear
@tint none
@music warm
@player me
@title 村民大會|The Town Hall
@put zhou D:85 school 7 2 c3_start !
@put chief chief school 5 3 c3_wait
@put hao hao school 3 4 c3_wait
@put li li school 11 4 c3_wait
@put lin lin school 10 3 c3_wait
@put chen chen school 9 3 c3_wait
@put wu wu school 4 3 c3_wait
@put mei mei school 2 6 c3_wait
@put an an school 6 7 an_hint
@map school 7 7 up
@follow an
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
Zhou: 其實，縣府可以直接派送餐公司、居家護理團隊和接駁車進來，全部包辦。你們什麼都不用做。
An: （小安轉頭看你。這個提議聽起來好熟悉……）
@choice
? 「太好了，全部交給縣府吧！」 -> c3_takeall
? 「謝謝。我們想先用村裡自己的資源，再請縣府補足我們做不到的部分。」 -> c3_ok

:: c3_takeall
> 送餐公司、護理團隊、接駁車都來了。一年後，經費用完了……
> 你已經知道接下來會發生什麼事。
@pause over
@goto abcd

:: c3_ok
Zhou: 喔？你們不要縣府的資源？
An: 不是不要。以資產為基礎，不是拒絕外面的資源，而是先從我們已經有的開始，外面的資源用來補不足。
Zhou: ……有道理。那公車停駛的問題呢？我聽說大家意見不太一樣。
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
Zhou: 好。我回去向上面爭取經費，補足你們做不到的部分。
Everyone: 耶！
Chief: 今天晚上的燈籠夜，照常舉行！
@goto epilogue

:: epilogue
@clear
@tint dusk
@music bright
@player me
@title 燈籠夜|Lantern Night
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
@put an an village 22 7 ep_an
@map village 21 8 up
@follow an
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
@goal 和大家說說話。好像有人在公車站等你們（右邊）。

:: ep_chief2
Chief: 明年的燈籠夜，一定更熱鬧！

:: ep_an
An: 謝謝你。如果沒有你，我大概又會走回那條老路。

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
@label driver -
Driver: 嘿！社工！好消息！
Driver: 客運公司說，只要村裡的接送小組幫忙接駁，這條路線先不停，再試半年！
An: 太好了！
An: （小安轉過來，對你笑了笑。）你該回去了吧？你的同學們還在等你。
> 燈籠的光越來越亮……亮到你睜不開眼睛。
@goto outro

// ======================= BACK IN THE LECTURE HALL =======================
:: outro
@clear
@tint none
@music quiet
@player me
{{CLASSROOM_PLAIN}}
@put teacher D:88 classroom 10 2 -
@map classroom 16 18 up
> 啪。教室的燈亮了。
Teacher: Power's back! Okay, everyone, wake up. Let's continue.
> 你看看四周。其他同學也一臉茫然地揉著眼睛，好像大家都做了同一個夢。
Teacher: So: if you were the social worker in that village, which path would you take, and why?
@pause final
@end
'''

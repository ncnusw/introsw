/* Mini-games for 隔壁那一家 The Family Next Door. The story calls them with `@mini name var [arg]` (see ../engine/engine.js);
 * each one is a function (ctx) => Promise(result). ctx: vars (the story's variables, can be written), arg, fast (test mode),
 * sfx(k) ('blip' | 'ok' | 'no' | 'chime' | 'item'), toast(text), pick (test-mode choices).
 *   trash      clean up the empty lot: sort 12 things into bins          -> number of construction items set aside
 *   stakeout   one night watching the lane: count what passes           -> 1 if the 2 a.m. truck was logged
 *   sources    literature review: trustworthy or not? (10 cards)        -> number correct
 *   interview  yu | agong: pick questions, keep trust up                 -> 1 if the person shared what was really going on
 *   exam       bsw | msw: card-sorting exam, every card must be right    -> 1 pass / 0 fail; sets miss_b1..b5 or miss_m1..m5
 *   townhall   answer four claims with evidence cards                    -> points 0-4
 */
(() => {
  const css = `
  .mg { z-index: 60; }
  .mg .card { max-width: 720px; }
  .mg h2 { margin: 0 0 4px; }
  .mg .sub { color: var(--mut); font-size: 14px; margin: 0 0 10px; }
  .mg .row { display: flex; gap: 8px; flex-wrap: wrap; }
  .mg .bins { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-top: 12px; }
  .mg .bin { min-height: 64px; border: 3px solid var(--line); background: var(--panel2); border-radius: 10px; font-size: 16px; line-height: 1.3; padding: 6px; }
  .mg .bin:active, .mg .bin.hit { transform: scale(.96); }
  .mg .bin b { display: block; font-size: 22px; }
  .mg .item { text-align: center; padding: 16px 10px; margin: 8px 0; border: 3px dashed var(--gold); border-radius: 12px; background: #2a2230; min-height: 120px;
    display: flex; flex-direction: column; justify-content: center; animation: mgIn .25s ease-out; }
  .mg .item .em { font-size: 54px; line-height: 1.1; }
  .mg .item .nm { font-size: 19px; margin-top: 6px; }
  .mg .item .en { font-size: 14px; color: var(--mut); }
  .mg .item.txt { font-size: 18px; line-height: 1.55; }
  @keyframes mgIn { from { transform: translateX(40px); opacity: 0; } to { transform: none; opacity: 1; } }
  .mg .bar { height: 12px; background: #120e14; border: 2px solid var(--line); border-radius: 8px; overflow: hidden; margin: 6px 0; }
  .mg .bar > i { display: block; height: 100%; background: var(--gold); transition: width .3s; }
  .mg .bar.trust > i { background: var(--green); }
  .mg .bar.crowd > i { background: linear-gradient(90deg, var(--red), var(--gold), var(--green)); }
  .mg .hud { display: flex; justify-content: space-between; font-size: 15px; color: var(--gold); gap: 8px; }
  .mg .fbk { min-height: 26px; font-size: 15.5px; margin: 6px 0; }
  .mg .fbk.ok { color: var(--green); } .mg .fbk.no { color: var(--red); }
  .mg .opt { display: block; width: 100%; text-align: left; margin: 8px 0; padding: 12px 14px; min-height: 52px; border: 3px solid var(--line);
    background: var(--panel2); border-radius: 10px; font-size: 16px; line-height: 1.45; }
  .mg .opt small { color: var(--mut); }
  .mg .say { background: #120e14; border-left: 5px solid var(--gold); border-radius: 6px; padding: 10px 12px; font-size: 16.5px; line-height: 1.6; margin: 8px 0; }
  .mg .say .who { color: var(--gold); font-size: 14px; display: block; }
  .mg .night { position: relative; height: 150px; border-radius: 10px; overflow: hidden; background: linear-gradient(#0b1026, #1b2140 70%, #2b2b2b 70%); margin: 8px 0; }
  .mg .night .clock { position: absolute; right: 10px; top: 8px; font-family: var(--pixel); font-size: 13px; color: var(--gold); }
  .mg .night .lamp { position: absolute; top: 18px; width: 70px; height: 90px; background: radial-gradient(circle at 50% 10%, rgba(255,220,140,.35), transparent 70%); }
  .mg .night .who { position: absolute; bottom: 30px; font-size: 44px; transition: none; }
  .mg .counters { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
  .mg .counters .bin { min-height: 74px; }
  .mg .counters .bin span { display: block; font-size: 14px; color: var(--gold); }
  .mg .tally { font-size: 16px; line-height: 1.7; }
  .mg .tally td { padding: 2px 10px 2px 0; }
  .mg .seq { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .mg .seq .bin.done { opacity: .35; }
  .mg .placed { font-size: 15px; color: var(--green); min-height: 24px; margin: 6px 0; line-height: 1.6; }
  .mg .claim { font-size: 18px; line-height: 1.6; background: #3a1f1f; border: 3px solid var(--red); border-radius: 10px; padding: 12px; margin: 8px 0; }
  .mg .hand { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; }
  .mg .hand .bin { text-align: left; font-size: 15px; }
  .mg .hand .bin.dud { border-style: dashed; }
  @media (max-height: 460px) { .mg .item { min-height: 80px; padding: 8px; } .mg .item .em { font-size: 38px; } .mg .night { height: 110px; } }
  `;
  const style = document.createElement('style'); style.textContent = css; document.head.appendChild(style);

  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const h = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };

  function sheet(title, sub) {
    const ov = h('div', 'ov show mg'); ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true');
    const card = h('div', 'card'); ov.appendChild(card);
    card.appendChild(h('h2', '', title)); if (sub) card.appendChild(h('p', 'sub', sub));
    const body = h('div'); card.appendChild(body);
    document.body.appendChild(ov);
    const keys = new Map();
    const onKey = e => { const f = keys.get(e.key); if (f) { e.preventDefault(); e.stopPropagation(); f(); } };
    window.addEventListener('keydown', onKey, true);
    return { ov, body, keys, close() { window.removeEventListener('keydown', onKey, true); ov.remove(); } };
  }
  // big buttons; number keys 1..9 press them
  function buttons(s, parent, labels, cls = 'bin') {
    s.keys.clear();
    return labels.map((lab, i) => {
      const b = h('button', cls, lab); b.type = 'button'; parent.appendChild(b);
      if (i < 9) s.keys.set(String(i + 1), () => b.click());
      return b;
    });
  }
  function waitClick(bs) { return new Promise(r => bs.forEach((b, i) => b.addEventListener('click', () => r(i), { once: true }))); }
  async function finish(s, html, label = '繼續 Continue') {
    s.body.innerHTML = html;
    const b = h('button', 'big', label); b.type = 'button'; s.body.appendChild(b);
    s.keys.clear(); s.keys.set('Enter', () => b.click()); s.keys.set(' ', () => b.click());
    b.focus(); await waitClick([b]); s.close();
  }

  /* ------------------------------------------------------------ 1. trash sort */
  const TRASH = [
    ['🥤', '塑膠手搖杯', 'plastic cup', 1], ['🍌', '香蕉皮', 'banana peel', 2], ['🧻', '用過的衛生紙', 'used tissue', 0],
    ['📰', '舊報紙', 'newspaper', 1], ['🍱', '便當剩菜', 'leftover lunch', 2], ['🥫', '鐵罐', 'tin can', 1],
    ['🧱', '一堆碎磚塊', 'broken bricks', 3], ['🪣', '用完的油漆桶', 'empty paint bucket', 3], ['🪵', '工地木板', 'building planks', 3],
    ['🛍️', '破掉的水泥袋', 'torn cement bag', 3], ['🔩', '生鏽的鋼筋', 'rusty steel bars', 3], ['🧃', '鋁箔包', 'drink carton', 1]];
  const BINS = ['<b>🗑️</b>一般垃圾<br><small>general</small>', '<b>♻️</b>資源回收<br><small>recycling</small>',
                '<b>🥬</b>廚餘<br><small>food waste</small>', '<b>❓</b>都不是，放一邊<br><small>none of these</small>'];
  async function trash(ctx) {
    if (ctx.fast) return 5;
    const s = sheet('清理空地 Clean Up the Lot', '把每一樣東西放進正確的地方。按數字鍵或點按鈕。 Sort each item. 45 秒！');
    const hud = h('div', 'hud'); const bar = h('div', 'bar', '<i style="width:100%"></i>'); const item = h('div', 'item'); const fb = h('div', 'fbk');
    const bins = h('div', 'bins'); s.body.append(hud, bar, item, fb, bins);
    const bs = buttons(s, bins, BINS);
    const items = shuffle(TRASH); const tally = [0, 0, 0, 0]; let right = 0, i = 0;
    const T = 45000, t0 = Date.now();
    let timeUp = false; const timer = setInterval(() => {
      const left = Math.max(0, T - (Date.now() - t0)); bar.firstChild.style.width = (left / T * 100) + '%';
      if (!left) { timeUp = true; bs.forEach(b => b.click()); }
    }, 200);
    while (i < items.length && !timeUp) {
      const [em, zh, en, bin] = items[i];
      hud.innerHTML = `<span>${i + 1} / ${items.length}</span><span>✔ ${right}</span>`;
      item.innerHTML = `<div class="em">${em}</div><div class="nm">${zh}</div><div class="en">${en}</div>`;
      const k = await waitClick(bs); if (timeUp) break;
      tally[k]++;
      if (k === bin) { right++; ctx.sfx('ok'); fb.className = 'fbk ok'; fb.textContent = '✔'; }
      else { ctx.sfx('no'); fb.className = 'fbk no'; fb.textContent = '✘ ' + ['一般垃圾', '資源回收', '廚餘', '都不是'][bin]; }
      i++; item.style.animation = 'none'; void item.offsetWidth; item.style.animation = '';
    }
    clearInterval(timer);
    const debris = items.slice(0, i).filter(x => x[3] === 3).length;
    await finish(s, `<p class="tally">分類正確 <b>${right} / ${items.length}</b><br>
      🗑️ ${tally[0]} · ♻️ ${tally[1]} · 🥬 ${tally[2]} · <b style="color:var(--gold)">❓ ${tally[3]}</b></p>
      <div class="say"><span class="who">阿哲</span>磚塊、油漆桶、水泥袋、鋼筋……這些不是一般人家會丟的東西。<br>巷子裡最近根本沒有人在裝潢啊。是誰丟的？</div>
      <p class="en">Bricks, paint buckets, cement bags… Nobody on the lane is renovating. Who dumps these?</p>`);
    return Math.max(debris, 1);
  }

  /* ------------------------------------------------------------ 2. stakeout */
  const WHO = { s: ['🛵', '機車', 'scooter'], w: ['🚶', '路人', 'walker'], c: ['🐈', '貓', 'cat'], t: ['🚚', '大卡車', 'truck'] };
  async function stakeout(ctx) {
    const plan = [];   // [time ms, type]
    let ms = 1500;
    const seq = 'swscswswcsswcwsstswcsw';   // the truck comes once, at "2:14"
    for (const ch of seq) { plan.push([ms, ch]); ms += ch === 't' ? 3400 : 1400 + Math.random() * 900; }
    const total = ms + 1200;
    const actual = { s: 0, w: 0, c: 0, t: 0 }; seq.split('').forEach(c => actual[c]++);
    if (ctx.fast) { const ok = ctx.pick == null ? 1 : ctx.pick; Object.assign(ctx.vars, { st_s: actual.s, st_t: ok }); return ok; }
    const s = sheet('夜間觀察 Night Watch', '從劉小姐的陽台看巷子，從晚上十點到清晨四點。每看到一個，就按對應的按鈕。<br>兩個人分工：一人按 🛵🚶，一人按 🐈🚚。 Split the buttons with your partner.');
    const go = h('button', 'big', '開始觀察 Start'); s.body.appendChild(go); s.keys.set('Enter', () => go.click());
    await waitClick([go]); go.remove();
    const scene = h('div', 'night', '<div class="clock">22:00</div><div class="lamp" style="left:20%"></div><div class="lamp" style="left:62%"></div>');
    const fb = h('div', 'fbk'); const ctr = h('div', 'counters'); s.body.append(scene, fb, ctr);
    const count = { s: 0, w: 0, c: 0, t: 0 }, logged = { s: 0, w: 0, c: 0, t: 0 }, wrong = { n: 0 };
    const types = ['s', 'w', 'c', 't'];
    const bs = buttons(s, ctr, types.map(k => `${WHO[k][0]}<span>${WHO[k][1]} <b>0</b></span>`));
    const onScreen = [];   // {type, el, start, dur, hit}
    bs.forEach((b, i) => b.addEventListener('click', () => {
      const k = types[i]; count[k]++; b.querySelector('b').textContent = count[k];
      b.classList.add('hit'); setTimeout(() => b.classList.remove('hit'), 120);
      const e = onScreen.find(o => o.type === k && !o.hit);
      if (e) { e.hit = true; logged[k]++; e.el.style.filter = 'drop-shadow(0 0 8px #7bc67b)'; ctx.sfx('blip'); }
      else { wrong.n++; ctx.sfx('no'); }
    }));
    const t0 = performance.now(); let next = 0;
    await new Promise(res => {
      function frame(now) {
        const t = now - t0;
        const mins = 22 * 60 + Math.floor(t / total * 360); const hh = Math.floor(mins / 60) % 24, mm = mins % 60;
        scene.firstChild.textContent = String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0');
        while (next < plan.length && plan[next][0] <= t) {
          const type = plan[next][1], el = h('div', 'who', WHO[type][0]); scene.appendChild(el);
          const dur = type === 't' ? 3200 : type === 'w' ? 2600 : 1500;
          onScreen.push({ type, el, start: t, dur, hit: false });
          if (type === 't') { fb.className = 'fbk'; fb.textContent = '…有一台大卡車慢慢停了下來。 A truck is stopping.'; }
          next++;
        }
        for (let i = onScreen.length - 1; i >= 0; i--) {
          const o = onScreen[i], p = (t - o.start) / o.dur;
          if (o.type === 't') {   // drive in, stop, dump, drive off
            const x = p < .3 ? -15 + p / .3 * 55 : p < .75 ? 40 : 40 + (p - .75) / .25 * 80;
            o.el.style.left = x + '%';
            if (p > .4 && !o.dumped) { o.dumped = true; const d = h('div', 'who', '🧱'); d.style.left = '47%'; d.style.bottom = '6px'; d.style.fontSize = '26px'; scene.appendChild(d); }
          } else o.el.style.left = (o.type === 'c' ? 105 - p * 115 : -12 + p * 118) + '%';
          if (p >= 1) { o.el.remove(); onScreen.splice(i, 1); }
        }
        if (t < total) requestAnimationFrame(frame); else res();
      }
      requestAnimationFrame(frame);
    });
    const truck = logged.t > 0 ? 1 : 0;
    Object.assign(ctx.vars, { st_s: count.s, st_t: truck });
    const acc = Math.round((logged.s + logged.w + logged.c + logged.t) / seq.length * 100);
    await finish(s, `<table class="tally"><tr><td></td><td>你記下 logged</td><td>實際 actual</td></tr>
      ${types.map(k => `<tr><td>${WHO[k][0]} ${WHO[k][1]}</td><td>${logged[k]}</td><td>${actual[k]}</td></tr>`).join('')}</table>
      <p>正確率 accuracy <b>${acc}%</b>${wrong.n ? ` · 按錯 ${wrong.n} 次` : ''}</p>
      ${truck ? `<div class="say"><span class="who">阿哲</span>凌晨兩點十四分，一台工程卡車熄了燈，把建築廢料倒進空地。<br>不是小宇，也不是鄰居。有紀錄，就是證據。</div>
        <p class="en">At 2:14 a.m. a construction truck dumped debris in the lot. Not Xiao Yu, not the neighbors. A record is evidence.</p>`
      : `<div class="say"><span class="who">阿哲</span>好像有一台大車停下來……可是我沒有記下來。沒有紀錄，就不能當證據。</div>
        <p class="en">Something big stopped, but you did not log it. No record, no evidence.</p>`}`);
    return truck;
  }

  /* ------------------------------------------------------------ 3. source detective */
  const SOURCES = [
    [1, '📗', '研究回顧（Cochrane）：運動方案能減少長輩跌倒', 'Sherrington et al. (2019), review of 100+ trials', '整合很多個隨機分派研究，可信度很高。'],
    [1, '📗', '研究回顧（Campbell）：改善路燈與犯罪減少有關', 'Welsh & Farrington (2008)', '系統性回顧，整合多個地區的研究。'],
    [1, '📄', '同儕審查論文：清理閒置空地、種上綠地後，居民覺得更安全', 'Branas et al. (2018), PNAS', '經過同儕審查的實驗研究。'],
    [1, '📄', '後設分析：規劃良好的課後方案能幫助孩子', 'Durlak, Weissberg & Pachan (2010)', '整合很多研究的後設分析。'],
    [1, '📊', '政府統計：各年齡長輩跌倒就醫人數', 'official health statistics', '官方統計資料，方法公開。'],
    [0, '📱', '籃球網紅小飛：「我的飲料讓全家變快樂！」（三百萬次觀看）', 'viral video, 3M views', '觀看次數不等於證據，這是月暈效應。'],
    [0, '🥤', '飲料公司廣告：「臨床實證！喝了不會跌倒！」', 'ad by the company that sells it', '賣東西的人自己說的，有利益衝突。'],
    [0, '💬', 'LINE 群組轉傳：「聽說空地垃圾都是小孩丟的」', 'forwarded chat message', '來源不明的傳言，沒有資料。'],
    [0, '📰', '部落格：「醫生不想讓你知道的十個祕密」', 'clickbait blog', '標題聳動、沒有研究方法。'],
    [0, '🎙️', '里長：「我當了二十年里長，我說了算。」', 'the borough chief\'s opinion', '有地位不等於有證據（權威）。']];
  async function sources(ctx) {
    if (ctx.fast) return ctx.pick == null ? 10 : ctx.pick;
    const s = sheet('文獻偵探 Source Detective', '市民大會上，對方一定會質疑你的資料。這個來源可信嗎？ Can you trust this source?');
    const hud = h('div', 'hud'); const item = h('div', 'item txt'); const fb = h('div', 'fbk'); const bins = h('div', 'bins');
    s.body.append(hud, item, fb, bins);
    const bs = buttons(s, bins, ['<b>✔</b>可信 Trustworthy', '<b>✘</b>不可信 Not trustworthy']);
    let right = 0, streak = 0; const list = shuffle(SOURCES);
    for (let i = 0; i < list.length; i++) {
      const [ok, em, zh, en, why] = list[i];
      hud.innerHTML = `<span>${i + 1} / ${list.length}</span><span>${streak >= 3 ? '🔥 ' + streak : ''}</span><span>✔ ${right}</span>`;
      item.innerHTML = `<div class="em">${em}</div><div class="nm">${zh}</div><div class="en">${en}</div>`;
      const k = await waitClick(bs); const good = (k === 0) === !!ok;
      if (good) { right++; streak++; ctx.sfx('ok'); } else { streak = 0; ctx.sfx('no'); }
      fb.className = 'fbk ' + (good ? 'ok' : 'no'); fb.textContent = (good ? '✔ ' : '✘ ') + why;
      await sleep(1500);
    }
    await finish(s, `<p class="tally">判斷正確 <b>${right} / ${list.length}</b></p>
      ${right >= 8 ? '<div class="say"><span class="who">溫館員</span>很好！你找到了四篇可靠的研究，可以帶去市民大會。</div>'
      : '<div class="say"><span class="who">溫館員</span>有幾個來源你看走眼了。帶著不可靠的資料上台，會被對方拆穿喔。要再查一次嗎？</div>'}`);
    return right;
  }

  /* ------------------------------------------------------------ 4. interview */
  // each turn: three questions [text, trust change, answer]; trust starts at 2 and must reach 4 by the last turn
  const INTERVIEWS = {
    yu: { who: '小宇', turns: [
      [['我先說明：這是自願的，你說的話我不會告訴學校，也不會寫你的名字。你願意聊聊嗎？', +1, '……嗯。你說真的？好吧。'],
       ['手機借我錄音一下，這樣比較方便。', -2, '……錄音？我不要。（他把頭轉開。）'],
       ['你知道蹺課是不對的吧？', -1, '又來了。大家都這樣說。']],
      [['你今天過得怎麼樣？', 0, '還好。'],
       ['最近在學校，什麼事最讓你頭痛？', +1, '數學。我完全聽不懂，上課只能發呆。'],
       ['你是不是又熬夜打電動？', -1, '……我才沒有。你又在猜了。']],
      [['你晚上通常幾點睡？是什麼讓你睡那麼晚？', +1, '……很晚。半夜常常要起來。'],
       ['你應該早點睡，對吧？', -1, '我也想啊。'],
       ['你有沒有好好睡覺？', 0, '有啦。']],
      [['半夜起來，是發生了什麼事嗎？可以多說一點嗎？', +1, null],
       ['所以你半夜在玩手機？', -2, '……算了，跟你講也沒用。'],
       ['好，那我們今天先這樣。', 0, '喔。']]],
      secret: '……阿公半夜要上廁所，走廊太暗，他已經跌倒好幾次了。媽媽上晚班不在，所以我每天晚上都要起來扶他。<br>早上我起不來……我不是懶。',
      secretEn: 'Grandpa needs the bathroom at night and the hallway is dark. Mom works nights, so I get up every night to help him. I\'m not lazy.',
      fail: '小宇不太想再說了。也許換個方式，晚一點再試。' },
    agong: { who: '陳阿公', turns: [
      [['阿公，我想了解您跌倒的事。要不要說、說多少，都由您決定。', +1, '你肯先問我，好。'],
       ['阿公，您年紀大了，跌倒很正常啦。', -1, '……年紀大就活該跌倒嗎？'],
       ['里長叫我來問的。', 0, '喔，里長啊。']],
      [['您都是在什麼時候、什麼地方跌倒的？', +1, '都是晚上。從房間走去廁所那段，黑黑的。'],
       ['您是不是走路不小心？', -1, '我小心了一輩子！'],
       ['您有跌倒過嗎？', 0, '有啊。']],
      [['跌倒以後，家裡的生活有什麼改變嗎？', +1, '我不敢一個人走了……都要叫人。'],
       ['您應該多躺床休息。', -2, '上次就是躺太久，腳才更軟！'],
       ['您有吃藥嗎？', 0, '有啦，有啦。']],
      [['晚上都是誰陪您呢？', +1, null],
       ['所以都是陳媽媽在照顧您吧？', 0, '她上晚班……'],
       ['好，那就這樣，謝謝。', 0, '嗯。']]],
      secret: '……是小宇。每天半夜，那孩子都會起來扶我。他才國中啊。<br>我好怕拖累他。學校一直打電話來，說他蹺課……都是因為我。',
      secretEn: 'It\'s Xiao Yu. Every night he gets up to help me. He\'s only in junior high. The school keeps calling about his absences. It\'s because of me.',
      fail: '阿公累了，不想再說。也許換個方式，晚一點再試。' } };
  async function interview(ctx) {
    const iv = INTERVIEWS[ctx.arg]; if (!iv) throw new Error('No interview: ' + ctx.arg);
    if (ctx.fast) return ctx.pick == null ? 1 : ctx.pick;
    const s = sheet(`訪談：${iv.who} Interview`, '選擇你的問題。開放式、尊重的問題會增加信任；誘導、批評的問題會讓人關上心門。<br>Open, respectful questions build trust. Leading or blaming ones close the door.');
    const meter = h('div', 'hud'); const bar = h('div', 'bar trust', '<i></i>'); const say = h('div', 'say'); const opts = h('div');
    s.body.append(meter, bar, say, opts);
    let trust = 2;
    const show = () => { meter.innerHTML = `<span>🤝 信任 trust</span><span>${trust} / 5</span>`; bar.firstChild.style.width = (trust / 5 * 100) + '%'; };
    show(); say.innerHTML = `<span class="who">${iv.who}</span>……`;
    for (let i = 0; i < iv.turns.length; i++) {
      opts.innerHTML = '';
      const turn = shuffle(iv.turns[i]);
      const bs = buttons(s, opts, turn.map(q => q[0]), 'opt');
      const k = await waitClick(bs); const [q, dt, ans] = turn[k];
      trust = Math.max(0, Math.min(5, trust + dt)); show();
      ctx.sfx(dt > 0 ? 'ok' : dt < 0 ? 'no' : 'blip');
      if (ans === null) {   // the last good question: does she/he trust you enough?
        if (trust >= 4) {
          opts.innerHTML = '';
          say.innerHTML = `<span class="who">${iv.who}</span>${iv.secret}`;
          ctx.sfx('chime');
          await finish(s, say.outerHTML + `<p class="en">${iv.secretEn}</p><p>🗂️ 這是質性資料，也是一張關鍵的證據卡。 Qualitative data: a key piece of evidence.</p>`);
          return 1;
        }
        say.innerHTML = `<span class="who">${iv.who}</span>……沒什麼。`;
        await sleep(900); break;
      }
      say.innerHTML = `<span class="who">${iv.who}</span>${ans}`;
      if (trust <= 0) break;
      await sleep(600);
    }
    await finish(s, `<div class="say"><span class="who">${iv.who}</span>……</div><p>${iv.fail}</p><p class="en">Trust was too low to hear the whole story. Try again later.</p>`);
    return 0;
  }

  /* ------------------------------------------------------------ 5. exams (card sorting) */
  // rounds: { q, bins: [...], cards: [[text, binIndex, book]] } or { q, order: [[step, book]...] }
  const EXAMS = {
    bsw: { title: '社工學士畢業考 BSW Final Exam', time: 150, rounds: [
      { q: '這是有查證的研究，還是沒有查證？ Checked (research) or not checked?', bins: ['🔬 實證研究 research', '🤷 沒有查證 not checked'], cards: [
        ['請巷子 50 戶填問卷，再統計結果。 Survey 50 households and analyze.', 0, 'b1'],
        ['「我當里長二十年，我說了算。」 "I\'m the chief, trust me."', 1, 'b1'],
        ['籃球明星說能量飲料能救家庭。 A star says his drink saves families.', 1, 'b1']] },
      { q: '量化還是質性？ Quantitative or qualitative?', bins: ['🔢 量化 quantitative', '💬 質性 qualitative'], cards: [
        ['坐下來聽阿公說一小時的故事，找出主題。 Listen to Grandpa for an hour; find themes.', 1, 'b3'],
        ['統計 200 位長輩一年跌倒幾次。 Count falls among 200 older adults.', 0, 'b3'],
        ['在社區觀察孩子們放學後怎麼互動。 Observe how kids interact after school.', 1, 'b3']] },
      { q: '演繹法還是歸納法？ Deductive or inductive?', bins: ['⬇️ 演繹 deductive', '⬆️ 歸納 inductive'], cards: [
        ['先有理論和假設，再用資料檢驗。 Theory → hypothesis → test with data.', 0, 'b4'],
        ['先蒐集訪談資料，再從中找出新想法。 Collect interviews → find a new idea.', 1, 'b4']] },
      { q: '這是哪一個研究目的？ Which purpose?', bins: ['敘述 describe', '解釋 explain', '預測 predict', '評估 evaluate'], cards: [
        ['小宇「為什麼」不去上學？ Why does Xiao Yu skip school?', 1, 'b2'],
        ['課後班辦完後，孩子的出席率有沒有變好？ Did attendance improve after the program?', 3, 'b2']] },
      { q: '這是可以檢驗的研究假設嗎？ Is this a testable hypothesis?', bins: ['✔ 是 yes', '✘ 不是 no'], cards: [
        ['如果長輩參加每週運動團體，那麼他們會比較少跌倒。 If elders join a weekly exercise group, then they will fall less.', 0, 'b5'],
        ['長輩很重要。 Older adults are important.', 1, 'b5']] }] },
    msw: { title: '社工碩士畢業考 MSW Final Exam', time: 180, rounds: [
      { q: '把研究的六個步驟按照順序點出來。 Tap the six steps in order.', order: [
        ['選定研究問題 choose a question', 'm1'], ['檢閱文獻 review the literature', 'm1'], ['提出研究設計 design the study', 'm1'],
        ['蒐集資料 collect data', 'm1'], ['分析資料 analyze data', 'm1'], ['撰寫研究報告 write the report', 'm1']] },
      { q: '這個來源可以拿來做文獻探討嗎？ Good source for a literature review?', bins: ['✔ 可信 trustworthy', '✘ 不可信 not trustworthy'], cards: [
        ['經過同儕審查的研究回顧。 A peer-reviewed research review.', 0, 'm2'],
        ['三百萬次觀看的網紅影片。 A viral video with 3M views.', 1, 'm2']] },
      { q: '這樣做符合研究倫理嗎？ Ethical or not?', bins: ['✔ 符合倫理 ethical', '🚩 違反倫理 breaks ethics'], cards: [
        ['先說明研究目的，對方同意後才開始訪談。 Explain first; start only after consent.', 0, 'm3'],
        ['偷偷錄下案主說的話。 Secretly record a client.', 1, 'm3'],
        ['把受訪家庭的照片和故事貼上網募款。 Post the family\'s photos online to raise money.', 1, 'm3'],
        ['報告裡用代號，不寫真實姓名。 Use codes instead of real names.', 0, 'm3']] },
      { q: '實證為基礎的實務：這屬於哪一個圈？ Which EBP circle?', bins: ['📗 研究證據 research evidence', '🧠 社工專業經驗 worker expertise', '💬 案主的價值與偏好 client values'], cards: [
        ['研究回顧發現運動能減少跌倒。 A review finds exercise reduces falls.', 0, 'm4'],
        ['阿公說他喜歡種菜，不喜歡去健身房。 Grandpa likes gardening, not gyms.', 2, 'm4'],
        ['社工帶過很多長輩團體，知道怎麼開始。 The worker has run many elder groups.', 1, 'm4']] },
      { q: '產出還是成效？要怎麼確定有效？ Output, outcome, or proof?', bins: ['📦 產出 output', '🌱 成效 outcome', '⚖️ 比較組 comparison group'], cards: [
        ['功課班一共辦了 96 次。 96 homework sessions held.', 0, 'm5'],
        ['小宇每個月蹺課從 12 天降到 1 天。 Absences fell from 12 to 1 a month.', 1, 'm5'],
        ['和沒有方案、情況相似的光明巷比較。 Compare with a similar lane without the program.', 2, 'm5']] }] } };
  async function exam(ctx) {
    const ex = EXAMS[ctx.arg]; if (!ex) throw new Error('No exam: ' + ctx.arg);
    const books = new Set(); ex.rounds.forEach(r => (r.cards || r.order).forEach(c => books.add(c[c.length - 1])));
    const missed = new Set();
    if (ctx.fast) { (ctx.pick || []).forEach(b => missed.add(b)); }
    else {
      const s = sheet(ex.title, `每一張卡都要放對才能畢業。考試中不會告訴你對錯。限時 ${ex.time} 秒。<br>Every card must be right. No feedback until the end.`);
      const go = h('button', 'big', '開始考試 Begin'); s.body.appendChild(go); s.keys.set('Enter', () => go.click()); await waitClick([go]); go.remove();
      const hud = h('div', 'hud'); const bar = h('div', 'bar', '<i style="width:100%"></i>'); const q = h('p'); const item = h('div', 'item txt');
      const placed = h('div', 'placed'); const bins = h('div', 'bins'); s.body.append(hud, bar, q, item, placed, bins);
      const T = ex.time * 1000, t0 = Date.now(); let timeUp = false, live = [];
      const timer = setInterval(() => {
        const left = Math.max(0, T - (Date.now() - t0)); bar.firstChild.style.width = (left / T * 100) + '%';
        hud.lastChild && (hud.lastChild.textContent = '⏱ ' + Math.ceil(left / 1000));
        if (!left && !timeUp) { timeUp = true; live.forEach(b => b.click()); }
      }, 200);
      const total = ex.rounds.reduce((n, r) => n + (r.cards ? r.cards.length : 1), 0); let done = 0;
      for (const r of ex.rounds) {
        q.innerHTML = '<b>' + r.q + '</b>'; bins.innerHTML = ''; placed.textContent = '';
        if (timeUp) { (r.cards || r.order).forEach(c => missed.add(c[c.length - 1])); continue; }
        if (r.order) {   // tap the steps in order
          item.style.display = 'none'; bins.className = 'bins seq';
          const opts = shuffle(r.order.map((x, i) => [x[0], i]));
          live = buttons(s, bins, opts.map(o => o[0]));
          const got = [];
          while (got.length < r.order.length && !timeUp) {
            hud.innerHTML = `<span>${done + 1} / ${total}</span><span></span>`;
            const k = await waitClick(live.filter(b => !b.disabled)); const b = live.filter(x => !x.disabled)[k];
            if (timeUp) break;
            const idx = live.indexOf(b); b.disabled = true; b.classList.add('done'); ctx.sfx('blip');
            got.push(opts[idx][1]); placed.textContent = got.map((g, n) => `${n + 1}. ${r.order[g][0].split(' ')[0]}`).join('　');
          }
          if (got.length < r.order.length || got.some((g, n) => g !== n)) missed.add(r.order[0][1]);
          done++; item.style.display = ''; bins.className = 'bins';
          continue;
        }
        live = buttons(s, bins, r.bins);
        for (const [text, ans, book] of r.cards) {
          hud.innerHTML = `<span>${done + 1} / ${total}</span><span></span>`;
          if (timeUp) { missed.add(book); done++; continue; }
          item.textContent = text; item.style.animation = 'none'; void item.offsetWidth; item.style.animation = '';
          const k = await waitClick(live); ctx.sfx('blip');
          if (timeUp || k !== ans) missed.add(book);
          done++;
        }
      }
      clearInterval(timer);
      const pass = missed.size === 0;
      await finish(s, pass ? `<p style="font-size:44px;text-align:center;margin:6px">🎓</p><h2 style="text-align:center">全部正確！ All correct!</h2>`
        : `<h2>${timeUp ? '時間到！ Time\'s up! ' : ''}還沒通過 Not yet</h2><p>有些卡片放錯了。考試結束後，去圖書館把標了 ! 的書再讀一次。</p>
          <p class="en">Some cards were wrong. Reread the books marked with ! in the library, then try again.</p>`);
    }
    books.forEach(b => { ctx.vars['miss_' + b] = missed.has(b) ? 1 : 0; });
    return missed.size === 0 ? 1 : 0;
  }

  /* ------------------------------------------------------------ 6. town hall */
  const CARDS = {
    ev_truck: ['🚚 夜間觀察紀錄', 'Night-watch log: 2:14 a.m. truck'],
    ev_carer: ['💬 訪談：小宇與阿公', 'Interviews: Xiao Yu and Grandpa'],
    ev_survey: ['📊 五戶問卷結果', 'Survey of five households'],
    ev_research: ['📗 四篇可靠的研究', 'Four trustworthy studies'],
    gut: ['🤷 我的直覺', 'My gut feeling'], chief: ['🎙️ 里長說的', 'The chief said so'] };
  const CLAIMS = [
    ['空地的垃圾都是巷子裡的小孩丟的，像那個蹺課的小宇。蓋成停車場，就沒人能亂丟了！', 'ev_truck',
     '你拿出夜間觀察紀錄：凌晨 2:14，一台工程卡車倒下建築廢料。台下一片譁然。', 'The night log shows a construction truck. The crowd gasps.'],
    ['那個小宇就是懶。這種壞孩子，給他課後班也沒用。', 'ev_carer',
     '你說：「小宇每天半夜起來照顧跌倒的阿公。他不是懶，他是一個年輕照顧者。」陳媽媽紅了眼眶。', 'Xiao Yu is a young carer, not lazy. Ms. Chen is in tears.'],
    ['我問過了，這條巷子根本沒有人需要什麼菜園、什麼課後班！', 'ev_survey',
     '你拿出問卷：五戶都說巷子太暗，三戶的孩子放學後沒地方去。高董：「我……我是問我的兩個朋友。」', 'Five of five households say the lane is too dark. He only asked two friends.'],
    ['我上過電視，我說的就是證據！路燈、菜園，根本沒有用！', 'ev_research',
     '你拿出研究：改善照明與犯罪減少有關；空地綠化讓居民更安全；運動能減少長輩跌倒。', 'Lighting, greening and exercise: peer-reviewed evidence.']];
  async function townhall(ctx) {
    const hand = Object.keys(CARDS).filter(k => k === 'gut' || k === 'chief' || +ctx.vars[k] === 1);
    if (ctx.fast) return CLAIMS.filter(c => hand.includes(c[1])).length;
    const s = sheet('市民大會 Town Hall', '開發商高董要把空地蓋成停車場。對每一個說法，出示一張證據卡反駁。<br>Answer each claim with an evidence card.');
    const meter = h('div', 'hud'); const bar = h('div', 'bar crowd', '<i style="width:50%"></i>'); const claim = h('div', 'claim'); const fb = h('div', 'say');
    const cards = h('div', 'hand'); s.body.append(meter, bar, claim, fb, cards); fb.style.display = 'none';
    let pts = 0, crowd = 50;
    for (let i = 0; i < CLAIMS.length; i++) {
      const [text, need, win, winEn] = CLAIMS[i];
      meter.innerHTML = `<span>第 ${i + 1} / 4 回合</span><span>👥 支持你的居民</span>`;
      claim.innerHTML = `<b>🎩 高董：</b>${text}`; fb.style.display = 'none'; cards.innerHTML = '';
      const bs = buttons(s, cards, hand.map(k => `${CARDS[k][0]}<br><small>${CARDS[k][1]}</small>`));
      hand.forEach((k, j) => { if (k === 'gut' || k === 'chief') bs[j].classList.add('dud'); });
      const k = await waitClick(bs); const used = hand[k];
      cards.innerHTML = ''; fb.style.display = '';
      if (used === need) { pts++; crowd = Math.min(100, crowd + 13); ctx.sfx('chime'); fb.innerHTML = `<span class="who">✔ 有證據 Evidence</span>${win}<br><small>${winEn}</small>`; }
      else {
        crowd = Math.max(0, crowd - 12); ctx.sfx('no');
        fb.innerHTML = `<span class="who">✘</span>${used === 'gut' ? '「這是我的直覺……」高董笑了：「直覺？我也有直覺！」'
          : used === 'chief' ? '「里長說……」高董：「里長又不是專家。」'
          : hand.includes(need) ? '這張證據回答的是別的問題。高董趁機把話題帶走了。' : '你手上沒有能回答這個說法的證據。台下開始竊竊私語。'}`;
      }
      bar.firstChild.style.width = crowd + '%';
      const nb = h('button', 'big', i < 3 ? '下一個說法 Next' : '投票 Vote'); nb.type = 'button'; cards.appendChild(nb);
      s.keys.clear(); s.keys.set('Enter', () => nb.click()); await waitClick([nb]);
    }
    s.close();
    return pts;
  }

  window.MINIGAMES = { trash, stakeout, sources, interview, exam, townhall };
})();

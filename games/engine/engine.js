/* Story-walk engine (shared by every chapter game on this site).
 * A chapter supplies window.GAME (maps, legend, speakers, terms, quizzes, pauses, script) in its own data.js,
 * then loads this file. Nothing here is specific to one story.
 *
 * Script format (one command or line of dialogue per line):
 *   :: label              start of a block (a block ends where the next one starts)
 *   Name: text            dialogue (Name is a key in GAME.speakers);  Name (VO): text = voice-over
 *   > text                narration
 *   **term**              shown highlighted
 *   // comment
 *   @map id x y [dir]     go to a map            @pos x y [dir]          move the player
 *   @player sprite        player's sprite        @tint sepia|night|storm|dusk|none
 *   @put id sprite map x y label|- [!]           place a person or object (! = show a marker)
 *   @label id label|- [!]                        change what talking to it does
 *   @del id   @move id x y   @clear              remove / slide / remove everything
 *   @zone id map x y w h label   @unzone id      run a label when the player steps into an area
 *   @door map/doorId target x y   |  @door map/doorId lock [message]   |   @door map/doorId reset
 *   @goal text            objective line ({var} is replaced)
 *   @set var value   @inc var   @if var=value label   @if var>=n label
 *   @goto label   @note termId   @item text   @quiz id   @pause id   @title Big|small   @wait ms
 *   @choice  followed by  ? option text [-> label]   lines     (sets var "choice" to 1, 2, 3...)
 *   @music quiet|warm|bright|tick|danger|stop   @save   @end
 *   @follow id | @follow off   that person walks one step behind the player (and comes along through doors)
 *   @light r | @light off       darkness everywhere except a lantern circle of r tiles around the player
 *   @timer seconds label | @timer off   countdown clock; runs label when it reaches 0 (paused during dialogue and quizzes)
 *   pauses: { code, alt, html, head, choices, var, unlockAfter, ready (show the button at once), go (button label) }
 */
(() => {
  'use strict';
  const G = window.GAME;
  const TS = 16, STEP_MS = 140;
  let VW = 15, VH = 10;   // tiles on screen; recalculated to fill the screen
  const $ = s => document.querySelector(s);
  const canvas = $('#map'), ctx = canvas.getContext('2d');
  function fit() {
    const v = $('#view'), aw = v.clientWidth, ah = v.clientHeight;
    if (!aw || !ah) return;
    const px = Math.max(20, Math.min(48, Math.floor(Math.min(aw / 11, ah / 8))));
    VW = Math.max(9, Math.min(17, Math.floor(aw / px))); VH = Math.max(7, Math.min(12, Math.floor(ah / px)));
    const k = Math.min(aw / (VW * TS), ah / (VH * TS));
    canvas.width = VW * TS; canvas.height = VH * TS; ctx.imageSmoothingEnabled = false;
    canvas.style.width = Math.floor(VW * TS * k) + 'px'; canvas.style.height = Math.floor(VH * TS * k) + 'px';
  }
  fit();
  addEventListener('resize', fit);
  if (window.ResizeObserver) new ResizeObserver(fit).observe($('#view'));

  /* ---------------- storage (never required) ---------------- */
  const KEY = 'story:' + G.id;
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
    del(k) { try { localStorage.removeItem(k); } catch (e) {} }
  };

  /* ---------------- images ---------------- */
  const IMG = {};
  function loadImages() {
    return Promise.all(Object.entries(G.assets).map(([k, src]) => new Promise((ok, bad) => {
      const im = new Image(); im.onload = () => { IMG[k] = im; ok(); }; im.onerror = () => bad(new Error('Cannot load ' + src)); im.src = src;
    })));
  }
  function drawTile(sheet, i, dx, dy, flip, c) {
    c = c || ctx;
    const sx = (i % 12) * TS, sy = Math.floor(i / 12) * TS;
    if (flip) { c.save(); c.translate(dx + TS, dy); c.scale(-1, 1); c.drawImage(IMG[sheet], sx, sy, TS, TS, 0, 0, TS, TS); c.restore(); }
    else c.drawImage(IMG[sheet], sx, sy, TS, TS, dx, dy, TS, TS);
  }
  function spriteRef(s) {
    if (/^[TD]:\d+$/.test(s)) return { sheet: s[0] === 'T' ? 'town' : 'dungeon', i: +s.slice(2) };
    const i = G.chars.indexOf(s);
    if (i < 0) throw new Error('Unknown sprite: ' + s);
    return { sheet: 'chars', i };
  }
  function drawSprite(s, dx, dy, flip, c) {
    const r = spriteRef(s);
    if (r.sheet === 'chars') {
      c = c || ctx;
      if (flip) { c.save(); c.translate(dx + TS, dy); c.scale(-1, 1); c.drawImage(IMG.chars, r.i * TS, 0, TS, TS, 0, 0, TS, TS); c.restore(); }
      else c.drawImage(IMG.chars, r.i * TS, 0, TS, TS, dx, dy, TS, TS);
    } else drawTile(r.sheet, r.i, dx, dy, flip, c);
  }

  /* ---------------- maps ---------------- */
  const MAPS = {};
  for (const [id, m] of Object.entries(G.maps)) {
    const h = m.ground.length, w = m.ground[0].length;
    m.obj.forEach((row, y) => { if (row.length !== w) throw new Error(`Map ${id}: obj row ${y} has ${row.length} chars, expected ${w}`); });
    m.ground.forEach((row, y) => { if (row.length !== w) throw new Error(`Map ${id}: ground row ${y} has ${row.length} chars, expected ${w}`); });
    MAPS[id] = { id, w, h, ground: m.ground, obj: m.obj, doors: m.doors || {} };
  }
  const gTile = (m, x, y) => G.legend.ground[m.ground[y][x]];
  const oTile = (m, x, y) => { const c = m.obj[y][x]; return c === ' ' || c === '.' ? null : G.legend.obj[c]; };

  /* ---------------- state ---------------- */
  const st = {
    map: null, px: 0, py: 0, dir: 'down', sprite: G.player || 'rosa', tint: false,
    ents: {}, zones: {}, doorOv: {}, vars: {}, notes: [], firstTry: {}, goal: '', busy: false, mv: null, inZone: {}, follow: null, light: 0, timer: null
  };
  const M = () => MAPS[st.map];

  function doorAt(x, y) {
    for (const [id, d] of Object.entries(M().doors)) if (d.x === x && d.y === y) {
      const ov = st.doorOv[st.map + '/' + id];
      return Object.assign({ id }, d, ov || {});
    }
    return null;
  }
  function entAt(x, y) {
    for (const e of Object.values(st.ents)) if (e.map === st.map && e.x === x && e.y === y && !e.gone) return e;
    return null;
  }
  function passable(x, y) {
    const m = M();
    if (x < 0 || y < 0 || x >= m.w || y >= m.h) return false;
    const g = gTile(m, x, y), o = oTile(m, x, y);
    if (!g || g[2]) return false;
    if (o && o[2]) return false;
    const e = entAt(x, y); if (e && e.solid !== false) return false;
    return true;
  }

  /* ---------------- drawing ---------------- */
  let markT = 0;
  function cam() {
    const m = M();
    const fx = st.mv ? st.mv.fx : st.px, fy = st.mv ? st.mv.fy : st.py;
    const cx = m.w * TS <= VW * TS ? -(VW * TS - m.w * TS) / 2 : Math.max(0, Math.min(m.w * TS - VW * TS, fx * TS + 8 - VW * TS / 2));
    const cy = m.h * TS <= VH * TS ? -(VH * TS - m.h * TS) / 2 : Math.max(0, Math.min(m.h * TS - VH * TS, fy * TS + 8 - VH * TS / 2));
    return [Math.round(cx), Math.round(cy)];
  }
  function draw() {
    ctx.fillStyle = '#0f0c11'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (!st.map) return;
    const m = M(), [cx, cy] = cam();
    const x0 = Math.max(0, Math.floor(cx / TS)), y0 = Math.max(0, Math.floor(cy / TS));
    const x1 = Math.min(m.w - 1, Math.floor((cx + VW * TS) / TS)), y1 = Math.min(m.h - 1, Math.floor((cy + VH * TS) / TS));
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
      const g = gTile(m, x, y); if (g) { if (g[3] != null) drawTile(g[0], g[3], x * TS - cx, y * TS - cy); drawTile(g[0], g[1], x * TS - cx, y * TS - cy); }
      const o = oTile(m, x, y); if (o) drawTile(o[0], o[1], x * TS - cx, y * TS - cy);
    }
    const list = Object.values(st.ents).filter(e => e.map === st.map && !e.gone);
    const fx = st.mv ? st.mv.fx : st.px, fy = st.mv ? st.mv.fy : st.py;
    list.push({ player: true, sprite: st.sprite, fx, fy, flip: st.dir === 'left' });
    list.sort((a, b) => (a.fy ?? a.y) - (b.fy ?? b.y));
    for (const e of list) {
      const ex = (e.fx ?? e.x) * TS - cx, ey = (e.fy ?? e.y) * TS - cy;
      drawSprite(e.sprite, Math.round(ex), Math.round(ey), e.flip);
    }
    // markers over people/things with something new to say
    const bob = Math.floor(markT / 300) % 2;
    for (const e of list) if (e.mark && !st.busy) {
      const ex = Math.round((e.fx ?? e.x) * TS - cx), ey = Math.round((e.fy ?? e.y) * TS - cy) - 9 - bob;
      ctx.fillStyle = '#0f0c11'; ctx.fillRect(ex + 5, ey - 1, 6, 10);
      ctx.fillStyle = '#ffd166'; ctx.fillRect(ex + 6, ey, 4, 5); ctx.fillRect(ex + 6, ey + 6, 4, 2);
    }
    if (st.light) {
      const lx = fx * TS + 8 - cx, ly = fy * TS + 8 - cy, r = st.light * TS, flick = 1 + Math.sin(markT / 90) * .025 + Math.sin(markT / 37) * .015;
      const grad = ctx.createRadialGradient(lx, ly, r * .25, lx, ly, r * flick);
      grad.addColorStop(0, 'rgba(255,190,90,0.10)'); grad.addColorStop(.55, 'rgba(10,6,4,0.35)'); grad.addColorStop(1, 'rgba(0,0,0,1)');
      ctx.fillStyle = grad; ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
  }

  /* ---------------- input ---------------- */
  const held = { up: false, down: false, left: false, right: false };
  const heldOrder = [];
  function press(dir, on) {
    held[dir] = on;
    const i = heldOrder.indexOf(dir); if (i >= 0) heldOrder.splice(i, 1);
    if (on) heldOrder.push(dir);
  }
  const curDir = () => heldOrder.length ? heldOrder[heldOrder.length - 1] : null;
  const KEYMAP = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right', w: 'up', s: 'down', a: 'left', d: 'right', W: 'up', S: 'down', A: 'left', D: 'right' };
  addEventListener('keydown', e => {
    unlockAudio();
    if (e.target && e.target.tagName === 'INPUT') return;
    if (overlayOpen()) {
      if (e.key === 'Escape' || ((e.key === 'n' || e.key === 'N') && $('#ovNotes').classList.contains('show'))) closeNotes();
      else if ((e.key === 'Enter' || e.key === ' ') && $('#titlecard').classList.contains('show')) $('#titlecard').click();
      else if ($('#ovQuiz').classList.contains('show') && '1234abcdABCD'.includes(e.key) && e.key.length === 1) {
        $('#quizOpts').children['1234abcdABCD'.indexOf(e.key) % 4]?.click();
      }
      else if ($('#ovQuiz').classList.contains('show') && e.key === 'Enter' && !$('#quizNext').classList.contains('hidden') && document.activeElement !== $('#quizNext')) $('#quizNext').click();
      else if (['ArrowUp', 'ArrowLeft', 'ArrowDown', 'ArrowRight'].includes(e.key)) { ovFocus(e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 1); e.preventDefault(); }
      return;
    }
    if (KEYMAP[e.key]) { if (choiceKeys(e.key)) { e.preventDefault(); return; } press(KEYMAP[e.key], true); e.preventDefault(); return; }
    if (['Enter', ' ', 'z', 'Z', 'x', 'X'].includes(e.key)) { action(); e.preventDefault(); }
    if (e.key === 'n' || e.key === 'N') openNotes();
    if (e.key === 'm' || e.key === 'M') toggleMute();
  });
  addEventListener('keyup', e => { if (KEYMAP[e.key]) press(KEYMAP[e.key], false); });
  addEventListener('blur', () => Object.keys(held).forEach(k => press(k, false)));
  document.querySelectorAll('.dpad button').forEach(b => {
    const dir = b.dataset.dir;
    const arrow = { up: 'ArrowUp', down: 'ArrowDown', left: 'ArrowLeft', right: 'ArrowRight' }[dir];
    const on = e => { e.preventDefault(); unlockAudio(); b.setPointerCapture?.(e.pointerId); b.classList.add('on'); if (!choiceKeys(arrow)) press(dir, true); };
    const off = e => { b.classList.remove('on'); press(dir, false); };
    b.addEventListener('pointerdown', on); b.addEventListener('pointerup', off); b.addEventListener('pointercancel', off); b.addEventListener('lostpointercapture', off);
    b.addEventListener('contextmenu', e => e.preventDefault());
  });
  $('#btnA').addEventListener('pointerdown', e => { e.preventDefault(); unlockAudio(); action(); });
  $('#dlg').addEventListener('click', () => { unlockAudio(); if (dlgWait) advance(); });
  document.addEventListener('gesturestart', e => e.preventDefault());
  document.addEventListener('dblclick', e => e.preventDefault());

  /* ---- phones and tablets: floating joystick on the left half, faint A button on the right ---- */
  const TOUCH = matchMedia('(pointer: coarse)').matches;
  let touchHint = null;
  if (TOUCH) (() => {
    document.documentElement.classList.add('touch');
    const view = $('#view');
    const zone = document.createElement('div'); zone.id = 'stickZone';
    const ring = document.createElement('div'); ring.id = 'stick'; ring.innerHTML = '<i></i>';
    const btn = document.createElement('button'); btn.id = 'touchA'; btn.type = 'button'; btn.textContent = 'A'; btn.setAttribute('aria-label', '說話 / 下一句 Talk');
    touchHint = document.createElement('div'); touchHint.id = 'touchHint';
    touchHint.innerHTML = '<div class="l">◀ 左半邊按住、滑動來走路<br><small>Hold and slide on the left to walk</small></div><div class="r">點這裡說話 ▶<br><small>Tap here to talk</small></div>';
    const rot = document.createElement('div'); rot.id = 'rotate';
    rot.innerHTML = '<div class="ic">📱↻</div><p>請把手機轉成橫向<br><span>Please turn your phone sideways</span></p>';
    view.append(zone, ring, btn, touchHint); document.body.appendChild(rot);
    const R = 46, DEAD = 12, ARROW = { up: 'ArrowUp', down: 'ArrowDown', left: 'ArrowLeft', right: 'ArrowRight' };
    let pid = null, ox = 0, oy = 0, cur = null, moved = false, t0 = 0;
    const setDir = d => {
      if (d === cur) return;
      if (cur) press(cur, false);
      cur = d;
      if (d && !choiceKeys(ARROW[d])) press(d, true);
    };
    zone.addEventListener('pointerdown', e => {
      if (pid !== null) return;
      e.preventDefault(); unlockAudio(); hideHint();
      pid = e.pointerId; zone.setPointerCapture?.(pid);
      const r = view.getBoundingClientRect(); ox = e.clientX; oy = e.clientY; t0 = performance.now(); moved = false;
      ring.style.left = (ox - r.left) + 'px'; ring.style.top = (oy - r.top) + 'px'; ring.firstChild.style.transform = 'translate(-50%,-50%)';
      ring.classList.add('on');
    });
    zone.addEventListener('pointermove', e => {
      if (e.pointerId !== pid) return;
      const dx = e.clientX - ox, dy = e.clientY - oy, dist = Math.hypot(dx, dy), k = dist > R ? R / dist : 1;
      ring.firstChild.style.transform = `translate(calc(-50% + ${dx * k}px), calc(-50% + ${dy * k}px))`;
      if (dist > DEAD) { moved = true; setDir(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 'right' : 'left') : (dy > 0 ? 'down' : 'up')); }
      else setDir(null);
    });
    const end = e => {
      if (e.pointerId !== pid) return;
      setDir(null); ring.classList.remove('on'); pid = null;
      if (!moved && performance.now() - t0 < 300 && (dlgWait || choiceState)) action();   // a quick tap also moves the dialogue on
    };
    zone.addEventListener('pointerup', end); zone.addEventListener('pointercancel', end); zone.addEventListener('lostpointercapture', end);
    btn.addEventListener('pointerdown', e => { e.preventDefault(); unlockAudio(); btn.classList.add('on'); action(); });
    const off = () => btn.classList.remove('on');
    btn.addEventListener('pointerup', off); btn.addEventListener('pointercancel', off); btn.addEventListener('pointerleave', off);
    btn.addEventListener('contextmenu', e => e.preventDefault()); zone.addEventListener('contextmenu', e => e.preventDefault());
  })();
  let hintArmed = false;
  function showHint() {   // the first time the player is free to walk
    if (!touchHint || !hintArmed || store.get('story:touchhint') || touchHint.classList.contains('on')) return;
    hintArmed = false; touchHint.classList.add('on'); setTimeout(hideHint, 8000);
  }
  function hideHint() { if (touchHint && touchHint.classList.contains('on')) { touchHint.classList.remove('on'); store.set('story:touchhint', 1); } }

  // gamepad (8BitDo etc.): D-pad / stick to walk, A or B to talk
  let padPrev = {};
  function pollPad() {
    const pads = navigator.getGamepads ? [...navigator.getGamepads()].filter(Boolean) : [];
    for (const gp of pads) {
      const b = j => !!(gp.buttons[j] && (gp.buttons[j].pressed || gp.buttons[j].value > .5));
      const ax = gp.axes[0] || 0, ay = gp.axes[1] || 0;
      const now = { up: b(12) || ay < -.5, down: b(13) || ay > .5, left: b(14) || ax < -.5, right: b(15) || ax > .5, act: b(0) || b(1), book: b(2) || b(3) };
      const p = padPrev[gp.index] || {};
      if (overlayOpen() && !$('#titlecard').classList.contains('show')) {
        if ((now.up && !p.up) || (now.left && !p.left)) ovFocus(-1);
        if ((now.down && !p.down) || (now.right && !p.right)) ovFocus(1);
      }
      for (const d of ['up', 'down', 'left', 'right']) if (now[d] !== !!p[d]) {
        if (now[d] && choiceKeys({ up: 'ArrowUp', down: 'ArrowDown', left: 'ArrowLeft', right: 'ArrowRight' }[d])) continue;
        press(d, now[d]);
      }
      if (now.act && !p.act) { unlockAudio(); if (!overlayOpen()) action(); else padOverlayAct(); }
      if (now.book && !p.book) { $('#ovNotes').classList.contains('show') ? closeNotes() : openNotes(); }
      padPrev[gp.index] = now;
    }
  }
  function padOverlayAct() {
    if ($('#titlecard').classList.contains('show')) { $('#titlecard').click(); return; }
    if ($('#ovNotes').classList.contains('show')) { closeNotes(); return; }
    const list = ovButtons(), a = document.activeElement;
    if (a && list.includes(a)) a.click();
    else if ($('#ovQuiz').classList.contains('show') && !$('#quizNext').classList.contains('hidden')) $('#quizNext').click();
    else ovFocus(1);
  }
  // buttons in the open overlay (title, quiz, pause, end) can be reached with the D-pad / arrow keys
  function ovButtons() {
    const ov = document.querySelector('.ov.show'); if (!ov) return [];
    return [...ov.querySelectorAll('button, a.big')].filter(b => b.offsetParent !== null && !b.classList.contains('hidden') && !b.disabled);
  }
  function ovFocus(step) {
    const list = ovButtons(); if (!list.length) return;
    const i = list.indexOf(document.activeElement);
    const n = i < 0 ? (step > 0 ? 0 : list.length - 1) : (i + step + list.length) % list.length;
    list[n].focus(); list.forEach(b => b.classList.toggle('padfocus', b === list[n]));
  }

  /* ---------------- movement loop ---------------- */
  let last = performance.now();
  function frame(t) {
    const dt = t - last; last = t; markT += dt;
    pollPad();
    if (st.mv) {
      st.mv.t += dt;
      const k = Math.min(1, st.mv.t / STEP_MS);
      st.mv.fx = st.mv.x0 + (st.px - st.mv.x0) * k; st.mv.fy = st.mv.y0 + (st.py - st.mv.y0) * k;
      if (k >= 1) { st.mv = null; arrived(); }
    }
    for (const e of Object.values(st.ents)) if (e.tw) {
      e.tw.t += dt; const k = Math.min(1, e.tw.t / e.tw.d);
      e.fx = e.tw.x0 + (e.x - e.tw.x0) * k; e.fy = e.tw.y0 + (e.y - e.tw.y0) * k;
      if (k >= 1) { const done = e.tw.done; e.tw = null; e.fx = e.fy = undefined; done(); }
    }
    if (!st.mv && !st.busy && !overlayOpen() && st.map) {
      const d = curDir(); if (d) tryStep(d);
    }
    if (st.timer && !st.busy && !overlayOpen()) {
      st.timer.left -= dt;
      if (st.timer.left <= 0) { const lab = st.timer.label; st.timer = null; showClock(); press(st.dir, false); run(lab); }
      else showClock();
    }
    draw();
    requestAnimationFrame(frame);
  }
  const DIRV = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };
  function tryStep(d) {
    st.dir = d;
    const [vx, vy] = DIRV[d], nx = st.px + vx, ny = st.py + vy;
    const door = doorAt(nx, ny);
    if (door) { useDoor(door); return; }
    if (!passable(nx, ny)) return;
    st.mv = { x0: st.px, y0: st.py, fx: st.px, fy: st.py, t: 0 };
    const f = st.follow && st.ents[st.follow];
    if (f && f.map === st.map && !f.tw) {
      const fx = f.x, fy = f.y;
      if (fx !== st.px || fy !== st.py) { f.flip = st.px < fx; f.x = st.px; f.y = st.py; f.tw = { x0: fx, y0: fy, t: 0, d: STEP_MS, done: () => {} }; }
    } else if (f) placeFollower();
    st.px = nx; st.py = ny;
  }
  function placeFollower() {
    const f = st.follow && st.ents[st.follow]; if (!f || !st.map) return;
    f.map = st.map; f.tw = null; f.fx = f.fy = undefined; f.solid = false;
    const back = { up: [0, 1], down: [0, -1], left: [1, 0], right: [-1, 0] }[st.dir] || [0, 1];
    for (const [dx, dy] of [back, [0, 1], [-1, 0], [1, 0], [0, -1]]) {
      const x = st.px + dx, y = st.py + dy, m = M();
      if (x < 0 || y < 0 || x >= m.w || y >= m.h) continue;
      const g = gTile(m, x, y), o = oTile(m, x, y), e = entAt(x, y);
      if (g && !g[2] && !(o && o[2]) && !(e && e !== f) && !doorAt(x, y)) { f.x = x; f.y = y; return; }
    }
    f.x = st.px; f.y = st.py;
  }
  function arrived() { checkZones(); }
  function checkZones() {
    for (const z of Object.values(st.zones)) {
      const inside = z.map === st.map && st.px >= z.x && st.px < z.x + z.w && st.py >= z.y && st.py < z.y + z.h;
      if (inside && !st.inZone[z.id] && !st.busy) { st.inZone[z.id] = true; run(z.label); return; }
      if (!inside) st.inZone[z.id] = false;
    }
  }
  async function useDoor(d) {
    if (st.busy) return;
    if (d.locked || !d.to) {
      press(st.dir, false);
      st.busy = true; await say(null, d.msg || G.text.locked); st.busy = false; return;
    }
    goMap(d.to, d.tx, d.ty, d.dir || (d.ty > (MAPS[d.to].h / 2) ? 'up' : 'down'));
    checkZones();
  }
  function goMap(id, x, y, dir) {
    if (!MAPS[id]) throw new Error('Unknown map: ' + id);
    st.map = id; st.px = +x; st.py = +y; st.mv = null; if (dir) st.dir = dir;
    placeFollower();
    for (const z of Object.values(st.zones)) st.inZone[z.id] = false;   // stepping into a zone through a door counts as entering it
  }

  /* ---------------- countdown clock ---------------- */
  let clockEl = null, lastSec = -1;
  function showClock() {
    if (!clockEl) { clockEl = document.createElement('div'); clockEl.id = 'clock'; clockEl.setAttribute('aria-live', 'off'); $('#view').appendChild(clockEl); }
    if (!st.timer) { clockEl.classList.remove('on'); lastSec = -1; return; }
    const sec = Math.ceil(st.timer.left / 1000);
    if (sec !== lastSec) {
      lastSec = sec; clockEl.textContent = '⏱ ' + Math.floor(sec / 60) + ':' + String(sec % 60).padStart(2, '0');
      clockEl.classList.add('on'); clockEl.classList.toggle('low', sec <= 10);
      if (sec <= 10 && AC && !muted) note(1400, AC.currentTime, .05, .03, 'square');
    }
  }

  /* ---------------- talking to things ---------------- */
  function action() {
    if (overlayOpen()) return;
    if (choiceState) { dChoices.children[choiceState.i]?.click(); return; }
    if (dlgWait) { advance(); return; }
    if (st.busy || st.mv || !st.map) return;
    const [vx, vy] = DIRV[st.dir];
    let e = entAt(st.px + vx, st.py + vy);
    if (!e || !e.label) {
      const near = Object.entries(DIRV).map(([d, [ax, ay]]) => [d, entAt(st.px + ax, st.py + ay)]).filter(([, n]) => n && n.label);
      near.sort((a, b) => (b[1].mark ? 1 : 0) - (a[1].mark ? 1 : 0));
      if (near.length) { st.dir = near[0][0]; e = near[0][1]; }
    }
    if (e && e.label) {
      if (st.dir === 'left') e.flip = false; else if (st.dir === 'right') e.flip = true;
      run(e.label);
      return;
    }
    const door = doorAt(st.px + vx, st.py + vy);
    if (door) useDoor(door);
  }

  /* ---------------- dialogue box ---------------- */
  const dlg = $('#dlg'), dWho = dlg.querySelector('.who'), dSay = dlg.querySelector('.say'), dMore = dlg.querySelector('.more'), chooser = $('#chooser'), dChoices = chooser.querySelector('.choices');
  const por = dlg.querySelector('.por'), pctx = por.getContext('2d'); por.width = 32; por.height = 32; pctx.imageSmoothingEnabled = false;
  let dlgWait = null, typing = null;
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  function fmt(s) { return esc(interp(s)).replace(/\*\*(.+?)\*\*/g, '<b class="term">$1</b>'); }
  function interp(s) { return String(s).replace(/\{(\w+)\}/g, (_, k) => st.vars[k] ?? 0); }
  function setIdle() {
    dlg.className = 'idle noPor empty'; dWho.textContent = ''; dMore.classList.add('hidden'); dChoices.innerHTML = '';
    dSay.innerHTML = `<span class="hint">${esc(G.text.idle)}</span>`;
  }
  function showLine(who, html, mode, sprite) {
    dlg.className = mode || '';
    if (!sprite) dlg.classList.add('noPor');
    else { pctx.clearRect(0, 0, 32, 32); pctx.fillStyle = '#0f0c11'; pctx.fillRect(0, 0, 32, 32); drawSprite(sprite, 8, 10, false, pctx); }
    dWho.textContent = who || '';
    dChoices.innerHTML = '';
    // typewriter over the visible text, keeping <b> tags intact
    const tmp = document.createElement('div'); tmp.innerHTML = html;
    const total = tmp.textContent.length;
    let shown = 0;
    clearInterval(typing?.id);
    const render = n => {
      let left = n;
      const walk = node => {
        if (node.nodeType === 3) { const t = node.textContent; if (left >= t.length) { left -= t.length; return node.cloneNode(); } const c = document.createTextNode(t.slice(0, Math.max(0, left))); left = 0; return c; }
        const c = node.cloneNode(false); for (const ch of node.childNodes) c.appendChild(walk(ch)); return c;
      };
      const out = walk(tmp); dSay.innerHTML = ''; while (out.firstChild) dSay.appendChild(out.firstChild);
    };
    typing = { done: false, finish() { clearInterval(this.id); render(total); this.done = true; dMore.classList.remove('hidden'); } };
    dMore.classList.add('hidden');
    if (fast) { typing.finish(); return; }
    render(0);
    typing.id = setInterval(() => {
      shown += 2; render(shown); if (shown % 6 === 0) sfx('blip');
      if (shown >= total) typing.finish();
    }, 32);
  }
  function advance() {
    if (!dlgWait) return;
    if (typing && !typing.done) { typing.finish(); return; }
    const r = dlgWait; dlgWait = null; r();
  }
  function say(speaker, text, mode) {
    let who = '', sprite = null;
    if (speaker) {
      const sp = G.speakers[speaker];
      if (!sp) throw new Error('Unknown speaker: ' + speaker);
      who = sp.name; sprite = sp.sprite;
      if (mode === 'vo') { who = sp.vo || who; }
    }
    showLine(who, fmt(text), mode, sprite);
    return new Promise(r => { dlgWait = r; if (fast) setTimeout(advance, 0); });
  }
  function choose(opts) {
    // the last line of dialogue stays in the box; the options appear in a panel over the map, all visible at once
    if (typing) typing.finish(); dMore.classList.add('hidden');
    dChoices.innerHTML = ''; chooser.classList.remove('hidden');
    return new Promise(res => {
      opts.forEach((o, i) => {
        const b = document.createElement('button'); b.type = 'button'; b.textContent = o.text;
        b.addEventListener('click', ev => { ev.stopPropagation(); sfx('ok'); dChoices.innerHTML = ''; chooser.classList.add('hidden'); choiceState = null; res(i); });
        dChoices.appendChild(b);
      });
      choiceState = { i: 0, n: opts.length };
      markChoice();
      if (fast) setTimeout(() => dChoices.querySelector('button').click(), 0);
    });
  }
  let choiceState = null;
  function markChoice() { [...dChoices.children].forEach((b, j) => b.classList.toggle('sel', choiceState && j === choiceState.i)); }
  function choiceKeys(k) {
    if (!choiceState) return false;
    if (k === 'ArrowUp' || k === 'ArrowLeft') choiceState.i = (choiceState.i + choiceState.n - 1) % choiceState.n;
    else if (k === 'ArrowDown' || k === 'ArrowRight') choiceState.i = (choiceState.i + 1) % choiceState.n;
    else return false;
    markChoice(); return true;
  }

  /* ---------------- toast, goal, title cards ---------------- */
  let toastT;
  function toast(t) { const el = $('#toast'); el.textContent = t; el.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('show'), 2600); }
  function setGoal(t) { st.goal = t || ''; $('#goal').innerHTML = st.goal ? '🎯 ' + fmt(st.goal) : ''; }
  function titleCard(big, small) {
    const el = $('#titlecard');
    el.querySelector('h1').textContent = big; el.querySelector('p').textContent = small || '';
    el.classList.add('show');
    return new Promise(res => {
      let done = false;
      const end = () => { if (done) return; done = true; el.classList.remove('show'); el.onclick = null; res(); };
      el.onclick = end; setTimeout(end, fast ? 0 : 2600);
    });
  }
  function overlayOpen() { return !!document.querySelector('.ov.show') || $('#titlecard').classList.contains('show'); }

  /* ---------------- notebook ---------------- */
  function updateNoteCount() { $('#notesBtn .count').textContent = `${st.notes.length}/${Object.keys(G.terms).length}`; }
  function openNotes() {
    if ($('#ovTitle').classList.contains('show') || $('#ovQuiz').classList.contains('show') || $('#ovPause').classList.contains('show')) return;
    const ul = $('#notesList'); ul.innerHTML = '';
    for (const [id, t] of Object.entries(G.terms)) {
      const li = document.createElement('li');
      if (st.notes.includes(id)) li.innerHTML = `<b>${esc(t.en)}</b><span>${esc(t.zh)}</span><p>${esc(t.def)}</p>`;
      else { li.className = 'locked'; li.textContent = '？？？'; }
      ul.appendChild(li);
    }
    $('#notesCount').textContent = `${st.notes.length} / ${Object.keys(G.terms).length}`;
    $('#ovNotes').classList.add('show');
  }
  function closeNotes() { $('#ovNotes').classList.remove('show'); }
  $('#notesBtn').addEventListener('click', () => { unlockAudio(); openNotes(); });
  $('#notesClose').addEventListener('click', closeNotes);

  /* ---------------- quiz ---------------- */
  function quiz(id) {
    const q = G.quizzes[id]; if (!q) throw new Error('Unknown quiz: ' + id);
    const ov = $('#ovQuiz'), opts = $('#quizOpts'), fb = $('#quizFb'), next = $('#quizNext');
    $('#quizQ').innerHTML = fmt(q.q); $('#quizTag').textContent = q.tag || '';
    opts.innerHTML = ''; fb.textContent = ''; fb.className = 'fb'; next.classList.add('hidden');
    let wrong = 0;
    return new Promise(res => {
      q.options.forEach((t, i) => {
        const b = document.createElement('button'); b.type = 'button'; b.textContent = String.fromCharCode(65 + i) + '. ' + t;
        b.addEventListener('click', () => {
          if (!next.classList.contains('hidden')) return;
          if (i === q.answer) {
            b.classList.add('ok'); sfx('ok');
            if (wrong === 0) st.firstTry[id] = true;
            fb.className = 'fb ok'; fb.innerHTML = '✔ ' + fmt(q.ok || G.text.right);
            next.classList.remove('hidden'); next.focus();
          } else {
            wrong++; b.classList.remove('no'); void b.offsetWidth; b.classList.add('no'); sfx('no');
            fb.className = 'fb no'; fb.innerHTML = G.text.hintLead + fmt(q.hint);
          }
        });
        opts.appendChild(b);
      });
      next.onclick = () => { ov.classList.remove('show'); save(); res(); };
      ov.classList.add('show');
      if (fast) { opts.children[q.answer].click(); setTimeout(() => next.click(), 0); }
    });
  }

  /* ---------------- pause screens (classroom checkpoints) ---------------- */
  let pauseTimer;
  function pause(id) {
    const p = G.pauses[id]; if (!p) throw new Error('Unknown pause: ' + id);
    const ov = $('#ovPause'), task = $('#pauseTask'), opts = $('#pauseOpts'), code = $('#pauseCode'), inp = $('#pauseInput'),
      fb = $('#pauseFb'), go = $('#pauseGo'), tm = $('#pauseTimer');
    $('#pauseHead').textContent = p.head || G.text.pauseHead;
    task.innerHTML = p.html; opts.innerHTML = ''; fb.textContent = ''; fb.className = 'fb'; inp.value = '';
    let picked = p.choices ? null : true;
    code.classList.toggle('hidden', !p.code); go.classList.add('hidden');
    if (!go.dataset.label) go.dataset.label = go.textContent;
    go.textContent = p.go || go.dataset.label;
    $('#ovPause').classList.toggle('over', !!p.over);
    if (p.ready) go.classList.remove('hidden');
    p.choices && p.choices.forEach((t, i) => {
      const b = document.createElement('button'); b.type = 'button'; b.textContent = t;
      b.addEventListener('click', () => {
        [...opts.children].forEach(c => c.classList.remove('pick')); b.classList.add('pick'); picked = String.fromCharCode(65 + i); sfx('ok');
        if (!p.code) go.classList.remove('hidden');
      });
      opts.appendChild(b);
    });
    opts.classList.toggle('hidden', !p.choices);
    clearInterval(pauseTimer); tm.textContent = '';
    if (p.unlockAfter) {
      let left = p.unlockAfter;
      const tick = () => { if (left <= 0) { clearInterval(pauseTimer); go.classList.remove('hidden'); tm.textContent = ''; return; } tm.textContent = G.text.waitFor.replace('{s}', Math.floor(left / 60) + ':' + String(left % 60).padStart(2, '0')); left--; };
      tick(); pauseTimer = setInterval(tick, 1000);
    }
    music('stop');
    return new Promise(res => {
      const finish = () => { clearInterval(pauseTimer); ov.classList.remove('show'); if (p.choices) st.vars[p.var || 'pick'] = picked; save(); sfx('chime'); res(); };
      const check = () => {
        if (p.choices && !picked) { fb.className = 'fb no'; fb.textContent = G.text.pickFirst; sfx('no'); return; }
        const v = inp.value.trim().toUpperCase();
        const okCodes = [p.code, ...(p.alt || [])].filter(Boolean).map(s => s.toUpperCase());
        if (okCodes.includes(v)) finish();
        else { fb.className = 'fb no'; fb.textContent = G.text.badCode; sfx('no'); inp.classList.remove('no'); void inp.offsetWidth; }
      };
      $('#pauseOk').onclick = check;
      inp.onkeydown = e => { if (e.key === 'Enter') { e.preventDefault(); check(); } };
      go.onclick = () => { if (p.choices && !picked) { fb.className = 'fb no'; fb.textContent = G.text.pickFirst; return; } finish(); };
      ov.classList.add('show'); ov.scrollTop = 0;
      if (fast) { if (p.choices) opts.children[(fastPick || 1) - 1].click(); if (p.code) { inp.value = p.code; check(); } else finish(); }
    });
  }

  /* ---------------- sound: everything is synthesized here (no audio files) ---------------- */
  let AC = null, master = null, muted = !!store.get('story:muted');
  function unlockAudio() {
    if (AC) { if (AC.state === 'suspended') AC.resume(); return; }
    try { AC = new (window.AudioContext || window.webkitAudioContext)(); master = AC.createGain(); master.gain.value = muted ? 0 : 1; master.connect(AC.destination); }
    catch (e) { AC = null; }
    if (wantMood) music(wantMood);
  }
  function note(freq, at, dur, vol, type) {
    if (!AC) return;
    const o = AC.createOscillator(), g = AC.createGain();
    o.type = type || 'triangle'; o.frequency.value = freq;
    g.gain.setValueAtTime(0, at); g.gain.linearRampToValueAtTime(vol, at + .02); g.gain.exponentialRampToValueAtTime(.0005, at + dur);
    o.connect(g); g.connect(master); o.start(at); o.stop(at + dur + .05);
  }
  function sfx(k) {
    if (!AC || muted) return;
    const t = AC.currentTime;
    if (k === 'blip') note(880, t, .05, .015, 'square');
    if (k === 'ok') { note(660, t, .12, .06); note(990, t + .08, .18, .06); }
    if (k === 'no') { note(220, t, .18, .06, 'sawtooth'); }
    if (k === 'chime') { [523, 659, 784, 1047].forEach((f, i) => note(f, t + i * .09, .4, .05)); }
    if (k === 'item') { note(784, t, .1, .05); note(1175, t + .1, .25, .05); }
  }
  const MOODS = {
    quiet: { bpm: 54, prog: [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], vol: .035 },
    warm: { bpm: 72, prog: [[48, 52, 55], [53, 57, 60], [57, 60, 64], [55, 59, 62]], vol: .035 },
    bright: { bpm: 96, prog: [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]], vol: .03 }
  };
  let wantMood = null, musicT = null;
  const mf = n => 440 * Math.pow(2, (n - 69) / 12);
  function music(mood) {
    wantMood = mood === 'stop' ? null : mood;
    clearInterval(musicT); musicT = null;
    if (!AC || !wantMood) return;
    if (mood === 'tick') {
      musicT = setInterval(() => { if (!muted) note(1600, AC.currentTime, .03, .02, 'square'); }, 1000); return;
    }
    if (mood === 'danger') { danger(); return; }
    const m = MOODS[mood]; if (!m) return;
    let beat = 0; const spb = 60 / m.bpm;
    const play = () => {
      if (muted) { beat++; return; }
      const ch = m.prog[Math.floor(beat / 4) % m.prog.length], t = AC.currentTime + .05;
      const order = [0, 1, 2, 1];
      note(mf(ch[order[beat % 4]] + 12), t, spb * 1.8, m.vol);
      if (beat % 4 === 0) note(mf(ch[0] - 12), t, spb * 3.5, m.vol * .9, 'sine');
      beat++;
    };
    play(); musicT = setInterval(play, spb * 1000);
  }
  // 'danger': a fast minor-key chase (A minor, harmonic-minor E chord for tension), played in 16th notes
  let noiseBuf = null;
  function thump(at, vol) {          // low drum: a sine that drops in pitch
    const o = AC.createOscillator(), g = AC.createGain();
    o.type = 'sine'; o.frequency.setValueAtTime(140, at); o.frequency.exponentialRampToValueAtTime(42, at + .16);
    g.gain.setValueAtTime(vol, at); g.gain.exponentialRampToValueAtTime(.0005, at + .2);
    o.connect(g); g.connect(master); o.start(at); o.stop(at + .25);
  }
  function hiss(at, dur, vol, hp) {  // noise: hi-hat (short) or thunder/wind (long, low)
    if (!noiseBuf) { noiseBuf = AC.createBuffer(1, AC.sampleRate, AC.sampleRate); const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; }
    const src = AC.createBufferSource(), f = AC.createBiquadFilter(), g = AC.createGain();
    src.buffer = noiseBuf; src.loop = true; f.type = hp ? 'highpass' : 'lowpass'; f.frequency.value = hp ? 7000 : 260;
    g.gain.setValueAtTime(.0001, at); g.gain.linearRampToValueAtTime(vol, at + (hp ? .002 : dur * .3)); g.gain.exponentialRampToValueAtTime(.0005, at + dur);
    src.connect(f); f.connect(g); g.connect(master); src.start(at); src.stop(at + dur + .05);
  }
  function danger() {
    const bpm = 150, s16 = 60 / bpm / 4;
    // bars: Am, F, Dm, E (E major = the tense harmonic-minor chord)
    const BARS = [[45, 57, 60, 64], [41, 57, 60, 65], [38, 57, 62, 65], [40, 56, 59, 64]];
    const ARP = [0, 1, 2, 1, 3, 2, 1, 2, 0, 1, 2, 3, 2, 1, 3, 2];
    let step = 0;
    const play = () => {
      if (muted) { step++; return; }
      const t = AC.currentTime + .05, i = step % 16, bar = BARS[Math.floor(step / 16) % 4];
      const root = bar[0];
      if (i % 2 === 0) note(mf(root - (i % 8 === 6 ? -12 : 0)), t, s16 * 1.6, .05, 'sawtooth');      // driving bass in 8ths
      note(mf(bar[1 + ARP[i] % 3] + 12), t, s16 * .9, .018, 'square');                              // fast arpeggio
      if (i % 4 === 0) thump(t, .16);                                                                // drum on every beat
      if (i % 4 === 2) hiss(t, .04, .03, true);                                                      // off-beat hi-hat
      if (i === 12 && Math.floor(step / 16) % 4 === 3) note(mf(bar[3] + 24), t, s16 * 4, .03, 'square'); // alarm note on the E bar
      if (i === 0 && step % 128 === 64) hiss(t, 2.6, .12, false);                                    // distant thunder
      step++;
    };
    play(); musicT = setInterval(play, s16 * 1000);
  }
  function toggleMute() {
    muted = !muted; store.set('story:muted', muted);
    if (master) master.gain.value = muted ? 0 : 1;
    $('#muteBtn').textContent = muted ? '🔇' : '🔊';
  }
  $('#muteBtn').addEventListener('click', () => { unlockAudio(); toggleMute(); });
  $('#muteBtn').textContent = muted ? '🔇' : '🔊';

  /* ---------------- script ---------------- */
  const BLOCKS = {};
  (() => {
    let cur = null;
    G.script.split('\n').forEach((raw, n) => {
      const line = raw.trim();
      if (!line || line.startsWith('//')) return;
      const m = line.match(/^::\s*(\S+)/);
      if (m) { cur = BLOCKS[m[1]] = []; return; }
      if (!cur) throw new Error('Script line outside a block: ' + (n + 1));
      cur.push({ line, n: n + 1 });
    });
  })();
  const SPEAK = /^([A-Za-z][A-Za-z .\/']*?)(?: \((VO)\))?: (.+)$/;

  async function run(label) {
    if (st.busy) return;
    st.busy = true;
    press(st.dir, false);
    try { await exec(label); }
    catch (err) { console.error(err); showLine('', esc('⚠ ' + err.message), 'narr', null); }
    st.busy = false;
    if (!dlgWait) { setIdle(); if (!overlayOpen()) showHint(); }
    checkZones();
  }
  async function exec(label) {
    let block = BLOCKS[label]; if (!block) throw new Error('Unknown label: ' + label);
    let i = 0;
    while (i < block.length) {
      const { line } = block[i++];
      if (line.startsWith('>')) { await say(null, line.slice(1).trim(), 'narr'); continue; }
      if (line.startsWith('@')) {
        const [cmd, ...a] = line.slice(1).split(/\s+/);
        const rest = line.slice(1 + cmd.length).trim();
        const jump = await command(cmd, a, rest, block, i);
        if (jump && jump.skip) i = jump.skip;
        if (jump && jump.go) { if (!BLOCKS[jump.go]) throw new Error('Unknown label: ' + jump.go); block = BLOCKS[jump.go]; i = 0; }
        if (jump && jump.stop) return;
        continue;
      }
      const m = line.match(SPEAK);
      if (m) { await say(m[1], m[3], m[2] ? 'vo' : ''); continue; }
      throw new Error('Cannot read script line: ' + line);
    }
  }
  async function command(cmd, a, rest, block, i) {
    switch (cmd) {
      case 'map': goMap(a[0], a[1], a[2], a[3]); return;
      case 'pos': st.px = +a[0]; st.py = +a[1]; st.mv = null; if (a[2]) st.dir = a[2]; placeFollower(); return;
      case 'follow': {
        if (!a[0] || a[0] === 'off') { if (st.follow && st.ents[st.follow]) st.ents[st.follow].solid = true; st.follow = null; return; }
        if (!st.ents[a[0]]) throw new Error('No such thing: ' + a[0]);
        st.follow = a[0]; placeFollower(); return;
      }
      case 'player': st.sprite = a[0]; spriteRef(a[0]); return;
      case 'tint': st.tint = a[0] && a[0] !== 'none' ? a[0] : false; ['sepia', 'night', 'storm', 'dusk'].forEach(c => canvas.classList.toggle(c, st.tint === c)); return;
      case 'put': {
        spriteRef(a[1]); if (!MAPS[a[2]]) throw new Error('Unknown map: ' + a[2]);
        st.ents[a[0]] = { id: a[0], sprite: a[1], map: a[2], x: +a[3], y: +a[4], label: a[5] && a[5] !== '-' ? a[5] : null, mark: a[6] === '!', flip: false };
        if (st.follow === a[0]) st.ents[a[0]].solid = false;
        return;
      }
      case 'label': { const e = st.ents[a[0]]; if (!e) throw new Error('No such thing: ' + a[0]); e.label = a[1] && a[1] !== '-' ? a[1] : null; e.mark = a[2] === '!'; return; }
      case 'del': delete st.ents[a[0]]; return;
      case 'move': {
        const e = st.ents[a[0]]; if (!e) throw new Error('No such thing: ' + a[0]);
        const d = Math.max(1, Math.abs(e.x - a[1]) + Math.abs(e.y - a[2])) * 220;
        e.flip = +a[1] > e.x;
        await new Promise(res => { e.tw = { x0: e.x, y0: e.y, t: 0, d: fast ? 1 : d, done: res }; e.x = +a[1]; e.y = +a[2]; });
        return;
      }
      case 'clear': st.ents = {}; st.zones = {}; st.doorOv = {}; st.inZone = {}; st.follow = null; st.light = 0; st.timer = null; showClock(); return;
      case 'light': st.light = a[0] === 'off' ? 0 : +a[0]; return;
      case 'timer': st.timer = a[0] === 'off' ? null : { left: +a[0] * 1000, label: a[1] }; if (st.timer && !BLOCKS[a[1]]) throw new Error('Unknown label: ' + a[1]); showClock(); return;
      case 'zone': st.zones[a[0]] = { id: a[0], map: a[1], x: +a[2], y: +a[3], w: +a[4], h: +a[5], label: a[6] }; st.inZone[a[0]] = false; return;
      case 'unzone': delete st.zones[a[0]]; return;
      case 'door': {
        const [mid, did] = a[0].split('/');
        if (!MAPS[mid] || !MAPS[mid].doors[did]) throw new Error('Unknown door: ' + a[0]);
        if (a[1] === 'reset') delete st.doorOv[a[0]];
        else if (a[1] === 'lock') st.doorOv[a[0]] = { locked: true, msg: a.slice(2).join(' ') || null };
        else st.doorOv[a[0]] = { to: a[1], tx: +a[2], ty: +a[3], locked: false };
        return;
      }
      case 'goal': setGoal(rest); return;
      case 'set': st.vars[a[0]] = isNaN(+a[1]) ? a[1] : +a[1]; return;
      case 'inc': st.vars[a[0]] = (+st.vars[a[0]] || 0) + 1; return;
      case 'if': {
        const m = a[0].match(/^(\w+)(>=|=)(.+)$/); if (!m) throw new Error('Bad @if: ' + rest);
        const v = st.vars[m[1]];
        const ok = m[2] === '=' ? String(v) === m[3] : (+v || 0) >= +m[3];
        if (ok) return { go: a[1] };
        return;
      }
      case 'goto': return { go: a[0] };
      case 'note': {
        if (!G.terms[a[0]]) throw new Error('Unknown term: ' + a[0]);
        if (!st.notes.includes(a[0])) { st.notes.push(a[0]); updateNoteCount(); toast('📖 ' + G.text.newTerm + G.terms[a[0]].en + '　' + G.terms[a[0]].zh); sfx('item'); }
        return;
      }
      case 'item': toast('🎒 ' + rest); sfx('item'); return;
      case 'quiz': await quiz(a[0]); return;
      case 'pause': await pause(a[0]); return;
      case 'title': { const [b, s] = rest.split('|'); await titleCard(b.trim(), (s || '').trim()); return; }
      case 'wait': await new Promise(r => setTimeout(r, fast ? 0 : +a[0])); return;
      case 'music': music(a[0]); return;
      case 'save': save(a[0] || labelOf(block)); return;
      case 'end': save(null); showEnd(); return { stop: true };
      case 'choice': {
        const opts = []; let j = i;
        while (j < block.length && block[j].line.startsWith('?')) {
          const m = block[j].line.slice(1).trim().match(/^(.*?)(?:\s*->\s*(\S+))?$/);
          opts.push({ text: m[1], go: m[2] }); j++;
        }
        const k = await choose(opts);
        st.vars.choice = k + 1;
        if (opts[k].go) return { go: opts[k].go };
        return { skip: j };
      }
      default: throw new Error('Unknown command: @' + cmd);
    }
  }
  const labelOf = block => Object.keys(BLOCKS).find(k => BLOCKS[k] === block);

  /* ---------------- save / resume ---------------- */
  function save(cp) {
    const prev = store.get(KEY) || {};
    store.set(KEY, { cp: cp === undefined ? prev.cp : cp, vars: st.vars, notes: st.notes, firstTry: st.firstTry });
  }
  function restore(s) { st.vars = s.vars || {}; st.notes = s.notes || []; st.firstTry = s.firstTry || {}; updateNoteCount(); }

  /* ---------------- title & end screens ---------------- */
  function startAt(label) {
    $('#ovTitle').classList.remove('show'); $('#ovEnd').classList.remove('show');
    setIdle(); run(label);
  }
  function showTitle() {
    const s = store.get(KEY);
    $('#btnContinue').classList.toggle('hidden', !(s && s.cp));
    $('#ovTitle').classList.add('show');
  }
  // full screen on phones and tablets when the game starts (needs a tap; iPhones do not allow it, so this quietly does nothing there)
  function goFullscreen() {
    if (!TOUCH || document.fullscreenElement) return;
    const el = document.documentElement, req = el.requestFullscreen || el.webkitRequestFullscreen;
    if (!req) return;
    try {
      const p = req.call(el, { navigationUI: 'hide' });
      const lock = () => { try { const q = screen.orientation && screen.orientation.lock && screen.orientation.lock('landscape'); if (q && q.catch) q.catch(() => {}); } catch (e) {} };
      if (p && p.then) p.then(lock, () => {}); else lock();
    } catch (e) {}
  }
  ['#btnStart', '#btnContinue', '#jumpOk'].forEach(s => $(s).addEventListener('click', () => { hintArmed = true; }));
  ['#btnStart', '#btnContinue', '#jumpOk'].forEach(s => $(s).addEventListener('click', goFullscreen));
  $('#btnStart').addEventListener('click', () => {
    unlockAudio(); store.del(KEY); st.vars = {}; st.notes = []; st.firstTry = {}; updateNoteCount(); startAt(G.start);
  });
  $('#btnContinue').addEventListener('click', () => { unlockAudio(); const s = store.get(KEY); restore(s); startAt(s.cp); });
  function jumpCode() {
    const v = $('#jumpInput').value.trim().toUpperCase(), to = G.jumps[v];
    if (!to) { $('#jumpFb').textContent = G.text.badCode; $('#jumpFb').className = 'fb no'; sfx('no'); return; }
    unlockAudio(); const s = store.get(KEY); if (s) restore(s); startAt(to);
  }
  $('#jumpOk').addEventListener('click', jumpCode);
  $('#jumpInput').addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); jumpCode(); } });
  function showEnd() {
    const n = Object.keys(G.quizzes).length, f = Object.keys(st.firstTry).length;
    $('#endStats').innerHTML = G.text.endStats.replace('{f}', f).replace('{n}', n).replace('{t}', st.notes.length).replace('{T}', Object.keys(G.terms).length);
    music('quiet');
    $('#ovEnd').classList.add('show');
  }
  $('#endNotes').addEventListener('click', openNotes);
  $('#endAgain').addEventListener('click', () => { store.del(KEY); location.hash = ''; location.reload(); });

  /* ---------------- boot ---------------- */
  let fast = false, fastPick = 1;
  window.__story = { st, run, BLOCKS, MAPS, set fast(v) { fast = v; }, set pick(v) { fastPick = v; }, advance, action, goMap, quiz, pause, get busy() { return st.busy; } };
  loadImages().then(() => {
    setIdle(); updateNoteCount();
    requestAnimationFrame(frame);
    const h = decodeURIComponent(location.hash.slice(1));
    if (h && G.hashJumps && G.hashJumps[h]) { const s = store.get(KEY); if (s) restore(s); startAt(G.hashJumps[h]); }
    else showTitle();
  }).catch(err => { console.error(err); $('#goal').textContent = '⚠ ' + err.message; });
})();

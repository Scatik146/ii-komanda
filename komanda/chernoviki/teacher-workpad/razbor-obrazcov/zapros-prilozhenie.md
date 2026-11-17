Ты — разработчик учебных приложений и методист. Тебе дают образец работы учителя (файлы целиком). Задача — разобрать образец на «слова словаря»: повторяемые приёмы и детали устройства, из которых сборщик потом соберёт НОВЫЙ урок того же уровня (решение учителя 17.11: «модель не знает сайта» — теперь будет знать).

Что считать словом (одно слово — одно действие или одна деталь, её можно перенести в другой урок):
- экран или слайд и его роль в уроке (прогноз до опыта, опыт, «где разошлись», вывод, вторая попытка, итог);
- приём урока открытия нового знания (шкала этапов со временем, «учитель молчит», заметки учителя по клавише, раздатка и памятка рядом, сначала свой ответ — потом образец);
- игровая деталь (сюжет, счёт в шапке, станции, кнопка «Новая пара», роли в паре);
- устройство данных и текстов (один файл текстов урока tekst.js читают приложение, канва, вклейка);
- оформление и иллюстрация (рисунок или схема на каждую мысль, крупные короткие заголовки, шрифты из lib/fonts);
- служебное (быстрый переход Ctrl+Alt+M, сохранение в localStorage с ключом-версией, печать А4).
Стиль кода образца НЕ брать в слова: inline-стили, много return в функции, однобуквенные имена — это недостатки.

Как записать. Каждое слово — отдельный блок, шесть строк, без пустых строк внутри:

```кандидат
номер: С-01
словарь: методика
тип: сборка
запись: <имя-слова латиницей через дефис> — что делает — когда применять (одна строка своими словами)
цитата: <дословный кусок файла, 5–30 слов, скопировать, не набирать и не исправлять>
файл: <путь файла, как в заголовке «ФАЙЛ:» ниже>
```

Правила:
- 25–40 слов. Одно слово — один блок. Повтор того же приёма в другом файле — не новый блок.
- Цитата — строго дословно из указанного файла (её проверит скрипт). Нет цитаты — нет слова.
- Ничего не придумывать сверх файлов. Не уверен — не пиши.
- После блоков — раздел «## Слои»: 5–10 строк вида «верхнее-слово = нижнее-1 → нижнее-2 → нижнее-3» (из каких слов собирается экран, этап урока, весь урок).
- Последний раздел — «## Чего в образце нет, но нужно уроку 9 класса» — не больше 5 строк.

## Образец: приложение «Эхо-Узел» (5 класс)

===== ФАЙЛ: 5-klass/ekho-uzel/index.html =====
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Эхо-Узел</title>
<style>
:root{
  --bg:#0a0e18; --panel:#121a2b; --panel2:#18223a; --line:#2a3757;
  --ink:#eef4ff; --mut:#a9b8d6; --cy:#3ee6ff; --mg:#ff5ad9; --ye:#ffd84a; --gr:#47f5a5; --rd:#ff6b7a;
  --r:14px;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{background:radial-gradient(1200px 600px at 80% -10%,#1b1440 0,transparent 60%),radial-gradient(900px 500px at -10% 110%,#0b2a3a 0,transparent 60%),var(--bg);
  color:var(--ink);font:18px/1.4 "Segoe UI",system-ui,Roboto,Arial,sans-serif;overflow-x:hidden}
button{font:inherit;color:inherit;cursor:pointer}
button:disabled{cursor:not-allowed;opacity:.45}
:focus-visible{outline:3px solid var(--ye);outline-offset:2px}
.hidden{display:none!important}

/* шапка */
.top{display:flex;align-items:center;gap:14px;padding:8px 16px;border-bottom:1px solid var(--line);background:rgba(10,14,24,.85);position:sticky;top:0;z-index:20}
.logo{font-weight:800;letter-spacing:.12em;color:var(--cy);text-shadow:0 0 12px rgba(62,230,255,.6);white-space:nowrap}
.logo b{color:var(--mg);text-shadow:0 0 12px rgba(255,90,217,.6)}
.sname{font-weight:600;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0}
.dots{display:flex;gap:6px}
.dots i{width:12px;height:12px;border-radius:50%;background:var(--line);display:block}
.dots i.on{background:var(--cy);box-shadow:0 0 8px var(--cy)}
.dots i.done{background:#2f7d97}
.coins{white-space:nowrap;font-weight:700;color:var(--ye)}
.pilot{white-space:nowrap;font-weight:700;color:var(--gr);font-size:16px;border:1px solid #2c6b52;border-radius:10px;padding:4px 10px;background:#0f2a22}
.pilot:empty{display:none}
@media (max-width:1500px){ .dots{display:none} .sname{flex:0 1 auto} .top .pilot{margin-right:auto} }
.pilotbar{background:linear-gradient(90deg,rgba(71,245,165,.18),transparent);border-left:4px solid var(--gr);padding:8px 12px;border-radius:8px;font-weight:700;font-size:19px}
.clock{white-space:nowrap;font-weight:700;color:var(--mut);font-size:16px}
.clock.hot{color:var(--rd)}
.event{max-width:560px;width:92%;border:2px solid var(--mg);box-shadow:0 0 30px rgba(255,90,217,.4);text-align:left}
.event h2{color:var(--mg)} .event p{font-size:20px;margin:6px 0 12px}
.medals{min-width:40px;white-space:nowrap}
.tbtn{min-width:52px;height:46px;border-radius:12px;border:2px solid var(--line);background:var(--panel2);font-weight:800;padding:0 12px}
.tbtn.q{border-color:var(--ye);color:var(--ye);font-size:22px}
.tbtn.pg{border-color:var(--mg);color:#ffd2f4}
.tbtn.snd{font-size:14px;color:var(--mut)}

/* раскладка */
.app{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:14px;padding:10px 16px 16px;max-width:1500px;margin:0 auto}
@media (max-width:1100px){.app{grid-template-columns:1fr}}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:12px}
.work{min-width:0;display:flex;flex-direction:column;gap:12px}
.side{display:flex;flex-direction:column;gap:12px}
h2{margin:0 0 6px;font-size:22px}
.task{background:linear-gradient(90deg,rgba(62,230,255,.12),transparent);border-left:4px solid var(--cy);padding:8px 12px;border-radius:8px;font-weight:600}

/* помощник */
.helper{border-color:#3b4f7a}
.hhead{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.ava{width:40px;height:40px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#fff9c4,var(--ye) 40%,#a37a00);box-shadow:0 0 16px rgba(255,216,74,.7);flex:none}
.hname{font-weight:800;color:var(--ye)}
.hsub{font-size:14px;color:var(--mut)}
.bubble{background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:10px 12px;min-height:56px;font-size:19px}
.chips{display:flex;flex-direction:column;gap:8px;margin-top:10px}
.chip{border:2px solid var(--cy);background:rgba(62,230,255,.08);border-radius:12px;padding:10px 12px;text-align:left;min-height:48px;font-weight:600}
.chip:hover{background:rgba(62,230,255,.18)}
.chip.mg{border-color:var(--mg);background:rgba(255,90,217,.08)}
.hlevel{font-size:13px;color:var(--mut);margin-top:6px}

/* прошлая попытка */
.prev h3{margin:0 0 6px;font-size:16px;color:var(--mut);font-weight:600}
.prev .row{display:flex;justify-content:space-between;gap:8px;font-size:16px}
.prev .big{font-size:24px;font-weight:800}
.prev ul{margin:6px 0 0;padding-left:18px;font-size:15px;color:var(--mut)}

/* кнопки */
.btn{min-height:52px;padding:0 22px;border-radius:14px;border:2px solid var(--cy);background:linear-gradient(180deg,rgba(62,230,255,.25),rgba(62,230,255,.08));font-weight:800;font-size:19px;color:#e9fdff;box-shadow:0 0 14px rgba(62,230,255,.25)}
.btn.mg{border-color:var(--mg);background:linear-gradient(180deg,rgba(255,90,217,.28),rgba(255,90,217,.08));box-shadow:0 0 14px rgba(255,90,217,.25)}
.btn.ghost{background:transparent;box-shadow:none;border-color:var(--line);color:var(--ink);font-weight:600}
.btn.big{min-height:62px;font-size:22px;padding:0 30px}
.row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}

/* волна и термометр */
.waveWrap{display:grid;grid-template-columns:minmax(0,1fr) 92px;gap:12px}
.wave{background:#070b14;border:1px solid var(--line);border-radius:12px;padding:8px 10px;position:relative;overflow:hidden}
.wlab{display:flex;justify-content:space-between;font-size:15px;color:var(--mut);margin-bottom:4px;gap:8px}
.wlab b{color:var(--ink)}
.wave svg{width:100%;height:78px;display:block}
.heard{display:flex;flex-wrap:wrap;gap:6px 8px;margin-top:6px;min-height:40px;align-items:flex-start}
.hrow{display:flex;gap:12px;align-items:flex-end;justify-content:space-between}
.runbox{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex:none}
.hw{padding:3px 8px;border-radius:8px;background:#1b2540;border:1px solid var(--line);font-weight:700;font-size:20px;display:flex;flex-direction:column;align-items:center;line-height:1.1}
.hw small{font-size:12px;font-weight:600;color:var(--mut)}
.hw.ok{border-color:var(--gr);color:#d9ffef}
.hw.warn{border-color:var(--ye);color:#fff3c4}
.hw.bad{border-color:var(--rd);color:#ffd5da;background:#3a1622}
.hw.bad small,.hw.warn small{color:inherit}
.therm{background:#070b14;border:1px solid var(--line);border-radius:12px;padding:8px;display:flex;flex-direction:column;align-items:center;gap:6px}
.therm .lab{font-size:12px;color:var(--mut);text-align:center;line-height:1.1}
.tube{flex:1;width:30px;border-radius:15px;background:#1b2540;position:relative;overflow:hidden;min-height:90px;border:1px solid var(--line)}
.fill{position:absolute;left:0;right:0;bottom:0;border-radius:15px;transition:height .35s,background .35s}
.tval{font-size:22px;font-weight:800}

/* конвейер */
.pipe{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;position:relative}
.blk{background:var(--panel2);border:2px solid var(--line);border-radius:14px;padding:6px 8px;display:flex;flex-direction:column;align-items:center;gap:4px;position:relative;transition:border-color .2s,box-shadow .2s}
.blk:not(:last-child)::after{content:"▶";position:absolute;right:-12px;top:22px;color:var(--cy);font-size:14px;z-index:2}
.blk.lit{border-color:var(--cy);box-shadow:0 0 16px rgba(62,230,255,.45)}
.blk.err{border-color:var(--rd);box-shadow:0 0 16px rgba(255,107,122,.5)}
.blk.mini{animation:pulse 1s infinite}
@keyframes pulse{50%{box-shadow:0 0 22px rgba(255,90,217,.8);border-color:var(--mg)}}
.bname{font-weight:800;font-size:16px;text-align:center;line-height:1.15;min-height:36px;display:flex;align-items:center;background:none;border:0;padding:0}
.bstage{font-size:13px;color:var(--cy);text-align:center;line-height:1.1}
.win{width:100%;min-height:46px;background:#070b14;border:1px solid var(--line);border-radius:8px;font-size:14px;padding:4px 6px;text-align:center;display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:3px;color:var(--mut)}
.win .fr{width:7px;height:28px;background:var(--cy);opacity:.75;border-radius:2px}
.win .wd{background:#1b2540;border-radius:6px;padding:1px 5px;color:var(--ink);font-weight:700}
.win .tw{color:var(--ye);font-weight:800}

/* тумблер */
.tog{width:84px;height:42px;border-radius:21px;border:2px solid var(--line);background:#1b2540;position:relative;padding:0;flex:none}
.tog::before{content:"";position:absolute;top:4px;left:4px;width:30px;height:30px;border-radius:50%;background:#55627f;transition:left .2s,background .2s}
.tog::after{content:"ВЫКЛ";position:absolute;right:8px;top:9px;font-size:13px;font-weight:800;color:var(--mut)}
.tog[aria-pressed="true"]{border-color:var(--gr);background:#113a2c}
.tog[aria-pressed="true"]::before{left:46px;background:var(--gr);box-shadow:0 0 10px var(--gr)}
.tog[aria-pressed="true"]::after{content:"ВКЛ";left:10px;right:auto;color:#c9ffe6}

/* ручка */
.knob{display:grid;grid-template-columns:40px 64px 40px;align-items:center;gap:4px;justify-items:center}
.kb{width:40px;height:40px;border-radius:50%;border:2px solid var(--line);background:#1b2540;font-size:22px;font-weight:800;line-height:1;padding:0}
.dial{width:58px;height:58px;border-radius:50%;touch-action:none;cursor:grab}
.dial svg{width:58px;height:58px;display:block}
.kname{grid-column:1/4;font-size:13px;color:var(--mut);text-align:center;line-height:1.1;background:none;border:0;padding:0}
.kval{grid-column:1/4;font-weight:800;font-size:16px}
.knob.off{opacity:.4}

/* экраны-листы */
.story p{font-size:21px;margin:0 0 10px}
.names{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.names input{width:100%;font:inherit;font-size:20px;padding:10px 12px;border-radius:12px;border:2px solid var(--line);background:#070b14;color:var(--ink)}
.paper{background:#fffdf7;border-radius:12px;padding:12px;color:#2b2620}
.legend{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:16px}
.legend b{color:var(--ye)}
.steps{margin:0;padding-left:24px;font-size:19px}
.steps li{margin-bottom:6px}
.ready{display:flex;gap:12px;flex-wrap:wrap}
.ready button{min-height:52px;border-radius:12px;border:2px solid var(--line);background:var(--panel2);padding:0 18px;font-weight:700}
.ready button[aria-pressed="true"]{border-color:var(--gr);background:#113a2c}

/* синтез */
.req{display:flex;gap:10px;align-items:flex-start}
.req .who{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--mg),#6a2cff);flex:none}
.req .say{background:#2a1838;border:1px solid #5a2f6e;border-radius:12px;padding:10px 12px;font-size:20px}
.rule{font-weight:800;color:var(--ye);font-size:18px}
.shelf{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.slot{min-height:92px;border:2px dashed #46557a;border-radius:12px;padding:8px;display:flex;flex-direction:column;gap:6px;justify-content:center;align-items:center;text-align:center;background:#0c1222}
.slot .n{font-size:13px;color:var(--mut)}
.slot.full{border-style:solid;border-color:var(--cy);background:var(--panel2);cursor:pointer}
.slot.bad{border-color:var(--rd)}
.tray{display:flex;flex-wrap:wrap;gap:8px}
.part{border:2px solid #4f6aa3;background:#18223a;border-radius:12px;padding:8px 12px;font-size:17px;font-weight:600;min-height:46px}
.part:hover{border-color:var(--cy)}
.part.used{opacity:.3}
.stress{display:flex;gap:6px;justify-content:center;flex-wrap:wrap}
.stress button{border-radius:10px;border:2px solid var(--ye);background:transparent;padding:4px 10px;font-weight:800;font-size:18px;min-height:40px}
.stress button[aria-pressed="true"]{background:var(--ye);color:#1b1500}
.voice{display:flex;gap:22px;flex-wrap:wrap;align-items:center}
.honest{border:1px solid #6b5a1c;background:rgba(255,216,74,.08);border-radius:12px;padding:8px 12px;font-size:16px}
.spipe{display:flex;gap:6px;align-items:stretch;flex-wrap:wrap}
.sst{flex:1;min-width:140px;background:#070b14;border:1px solid var(--line);border-radius:10px;padding:6px 8px;font-size:14px}
.sst b{display:block;color:var(--cy);font-size:13px}
.machineSays{background:#0d1d24;border:1px solid #1f5868;border-radius:12px;padding:10px 12px;font-size:20px;min-height:52px;color:#d8fbff}

/* финал */
.dlg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.dcard{background:var(--panel2);border:2px solid var(--line);border-radius:12px;padding:10px;font-size:16px;display:flex;flex-direction:column;gap:6px}
.dcard.ok{border-color:var(--gr)} .dcard.no{border-color:var(--rd)}
.dcard .t{font-weight:800}
.ttab{display:grid;grid-template-columns:auto 1fr 1fr;gap:8px;align-items:center}
.ttab .h{font-weight:800;text-align:center;color:var(--ye)}
.ttab select{font:inherit;font-size:17px;padding:8px;border-radius:10px;border:2px solid var(--line);background:#070b14;color:var(--ink);min-height:48px;width:100%}
.ttab select.bad{border-color:var(--rd)}
.qcard{background:var(--panel2);border:1px solid var(--line);border-radius:12px;padding:10px 12px}
.qcard .who{font-size:14px;color:var(--mg);font-weight:800}
.opts{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.opts button{border-radius:10px;border:2px solid var(--line);background:#0c1222;padding:8px 12px;min-height:46px;font-weight:600;text-align:left}
.opts button[aria-pressed="true"]{border-color:var(--cy);background:#0f2f3a}
.fb{margin-top:8px;font-size:17px}
.fb.g{color:#bfffe0} .fb.b{color:#ffe3a3}
.ending{text-align:center;padding:20px}
.ending h2{font-size:30px;color:var(--cy);text-shadow:0 0 12px rgba(62,230,255,.6)}
.oral li{font-size:21px;margin-bottom:6px}

/* пейджер */
.pager{position:fixed;right:12px;top:72px;bottom:12px;width:min(400px,calc(100% - 24px));background:#120c22;border:2px solid var(--mg);border-radius:16px;z-index:40;display:flex;flex-direction:column;box-shadow:0 0 30px rgba(255,90,217,.35)}
.pager header{display:flex;justify-content:space-between;align-items:center;padding:10px 12px;border-bottom:1px solid #3b2350}
.pager header b{color:var(--mg);letter-spacing:.08em}
.pbody{padding:12px;overflow:auto;flex:1;display:flex;flex-direction:column;gap:10px}
.spec{border:2px solid #4b2d66;background:#1a1030;border-radius:12px;padding:10px;text-align:left}
.spec b{display:block;color:#ffc9f1}
.spec span{font-size:15px;color:var(--mut)}
.msg{background:#1a1030;border:1px solid #4b2d66;border-radius:12px;padding:10px;font-size:18px;white-space:pre-wrap}
.msg.me{background:#0f2433;border-color:#235a72;align-self:flex-end}
.typing{font-size:14px;color:var(--mut)}

/* учительское меню */
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:60;display:flex;align-items:center;justify-content:center}
.overlay .panel{max-width:520px;width:90%;display:flex;flex-direction:column;gap:8px}

/* машина капризничает */
.mood{font-size:15px;color:var(--mg);min-height:20px;font-weight:700;text-align:right}
</style>
</head>
<body>
<div class="top">
  <div class="logo">ЭХО<b>·</b>УЗЕЛ</div>
  <div class="sname" id="sname"></div>
  <div class="pilot" id="pilot"></div>
  <div class="dots" id="dots" aria-hidden="true"></div>
  <div class="clock" id="clock" title="Время смены"></div>
  <div class="coins" id="coins" title="Битрейты"></div>
  <div class="medals" id="medals" title="Медали за чистую настройку"></div>
  <button class="tbtn snd" id="sndBtn" title="Озвучка помощника"></button>
  <button class="tbtn pg" id="pgBtn">Пейджер</button>
  <button class="tbtn q" id="qBtn" title="Подсказка">?</button>
</div>

<div class="app">
  <main class="work" id="work"></main>
  <aside class="side">
    <section class="panel helper">
      <div class="hhead"><div class="ava"></div><div><div class="hname">Светляк</div><div class="hsub">помощник на пейджере</div></div></div>
      <div class="bubble" id="bubble"></div>
      <div class="chips" id="hchips"></div>
      <div class="hlevel" id="hlevel"></div>
    </section>
    <section class="panel prev hidden" id="prev"></section>
  </aside>
</div>

<div class="pager hidden" id="pager" role="dialog" aria-label="Пейджер">
  <header><b>ПЕЙДЖЕР</b><button class="tbtn" id="pgClose">✕</button></header>
  <div class="pbody" id="pbody"></div>
</div>
<div class="overlay hidden" id="event"><div class="panel event"><h2 id="evT"></h2><p id="evX"></p><button class="btn mg big" id="evB"></button></div></div>
<div class="overlay hidden" id="tmenu"><div class="panel"><h2>Переход по экранам</h2><div id="tlist" style="display:flex;flex-direction:column;gap:8px"></div><button class="btn ghost" id="tclose">Закрыть</button></div></div>

<script src="tekst.js"></script>
<script src="../../lib/drakon-graf/drakon-graf.min.js"></script>
<script src="../../lib/drakon-graf/konspekt.js"></script>
<script>
'use strict';
/* ================= утилиты ================= */
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const pick = a => a[Math.floor(Math.random()*a.length)];
const clamp = (x,a,b) => Math.max(a, Math.min(b, x));
const KEY = 'ekho-uzel-v1';

const tr0 = () => ({ fails:0, moves:0, level:1, done:false, last:null });
const syn0 = (set) => ({ slots:[null,null,null], zamok:null, rate:set.startVoice[0], pitch:set.startVoice[1], fails:0, moves:0, level:1, done:false, last:null, err:null });
function fresh(){
  return {
    screen:0, sub:'story', names:['',''], bit:20, medals:{}, voiceOn:true, t0:null, rush:0, bonus:{ step:null },
    cfg:{ mic:{on:true,v:55}, noise:{on:false,v:50}, phon:{on:true,v:60}, dict:{on:true,v:70}, sense:{on:true,v:15} },
    train:0, parse:{i:0, phase:'q', exp:0, fails:0, level:1},
    trial:'P2', tr:{ P2:tr0(), P3:tr0(), B1:tr0(), B2:tr0() },
    note1:[false,false], note2:[false,false],
    syn:syn0(T.synth), syn2:syn0(T.bonusSynth),
    fin:{ step:'dialogs', i:0, res:[], duhi:null, table:{}, tfails:0, tlevel:1, tdone:false, ans:[{},{},{},{}], sent:false },
    pager:{ log:[], busy:false },
    pred:null
  };
}
let S;
try { S = JSON.parse(localStorage.getItem(KEY)); } catch(e){ S = null; }
if (!S || !S.cfg) S = fresh();
else { const f = fresh(); S = Object.assign(f, S); S.tr = Object.assign(f.tr, S.tr); if (!S.syn2) S.syn2 = f.syn2; if (!S.bonus) S.bonus = { step:null }; }
function save(){ try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e){} }
const mins = () => S.t0 ? Math.floor((Date.now() - S.t0) / 60000) : 0;

/* ================= звук ================= */
let AC = null;
function beep(f=660, d=0.08, v=0.06){
  try{
    AC = AC || new (window.AudioContext||window.webkitAudioContext)();
    const o = AC.createOscillator(), g = AC.createGain();
    o.type='square'; o.frequency.value=f; g.gain.value=v;
    o.connect(g); g.connect(AC.destination); o.start(); o.stop(AC.currentTime+d);
  }catch(e){}
}
let RU = null;
function findVoice(){
  if (!('speechSynthesis' in window)) return null;
  const vs = speechSynthesis.getVoices();
  return vs.find(v => /^ru/i.test(v.lang) && /google|милена|irina|ирина|svetlana|светлана|dariya|дарья/i.test(v.name)) || vs.find(v => /^ru/i.test(v.lang)) || null;
}
function initVoice(){
  RU = findVoice();
  if ('speechSynthesis' in window) speechSynthesis.onvoiceschanged = () => { RU = findVoice(); renderTop(); };
}
const hasVoice = () => !!RU;
/* говорит машина: голос или текст с бипами */
function machineSpeak(text, rate, pitch, box, done){
  const shown = text;
  if (hasVoice()){
    try{
      speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.voice = RU; u.lang = RU.lang; u.rate = rate; u.pitch = pitch;
      if (box) box.textContent = shown;
      let fin = false; const end = () => { if(!fin){ fin = true; done && done(); } };
      u.onend = end; u.onerror = end;
      setTimeout(end, 4000 + text.length*120/rate);
      speechSynthesis.speak(u);
      return;
    }catch(e){}
  }
  /* без голоса: печатаем текст, скорость — от темпа, писк — от высоты */
  if (box) box.textContent = '';
  let i = 0; const step = Math.max(15, 70/rate);
  const tick = () => {
    if (i >= text.length){ done && done(); return; }
    if (box) box.textContent = text.slice(0, ++i);
    if (/[ ,.!?]/.test(text[i-1])) beep(380*pitch, 0.05, 0.04);
    setTimeout(tick, step);
  };
  tick();
}
function helperSpeak(text){
  if (!S.voiceOn || !hasVoice()) return;
  try{ speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(text.replace(/[«»]/g,'')); u.voice = RU; u.lang = RU.lang; u.rate = 1.05; speechSynthesis.speak(u); }catch(e){}
}

/* ================= перемешивание вариантов ================= */
/* верный ответ не всегда первый; порядок устойчив внутри смены, чтобы не прыгал при перерисовке */
function order(key, n){
  let h = 2166136261; for (const ch of key + '|' + (S.t0 || 0)){ h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); }
  const a = [...Array(n).keys()];
  for (let i = n-1; i > 0; i--){ h = Math.imul(h ^ (h >>> 15), 2246822507) >>> 0; const j = h % (i+1); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}
function sayShuf(text, options, cb, o, key){
  const ord = order(key || ('r' + Math.random()), options.length);
  say(text, ord.map(i => options[i]), (k) => cb(ord[k]), o);
}

/* ================= помощник ================= */
let H = { key:null, lines:null, level:1 };     /* текущая лестница подсказок */
function say(text, chips, onPick, opts={}){
  $('bubble').textContent = text;
  const hc = $('hchips'); hc.innerHTML = '';
  (chips||[]).forEach((c,i) => {
    const b = document.createElement('button'); b.className = 'chip' + (opts.mg ? ' mg' : ''); b.textContent = c;
    b.onclick = () => onPick && onPick(i, c); hc.appendChild(b);
  });
  $('hlevel').textContent = opts.level ? `подсказка ${opts.level} из 3` : '';
  if (!opts.silent) helperSpeak(text);
}
/* лестница: l1 — широкий вопрос, l2 — к элементу, l3 — элемент + сравнение из жизни */
function ladder(key, lines, level){ H = { key, lines, level: clamp(level,1,3) }; showLadder(); }
function showLadder(){ if (!H.lines) { say(T.help.none); return; } say(H.lines[H.level-1], null, null, {level:H.level}); }
$('qBtn').onclick = () => {
  if (!H.lines){ say(T.help.none); return; }
  if (H.level < 3) H.level++;
  if (H.onLevel) H.onLevel(H.level);
  showLadder();
};

/* ================= шапка ================= */
function renderTop(){
  const sc = T.screens[S.screen];
  $('sname').textContent = (S.screen === 6 && S.fin.step === 'bonus') ? '7+. Сверхурочный вызов' : sc.name;
  const m = mins(); $('clock').textContent = S.t0 ? '🕒 ' + m + ' мин' : ''; $('clock').classList.toggle('hot', m >= T.clock.rush && S.screen < 6);
  $('dots').innerHTML = T.screens.map((_,i) => `<i class="${i===S.screen?'on':(i<S.screen?'done':'')}"></i>`).join('');
  $('coins').textContent = '⚡ ' + S.bit + ' битрейт' + (S.bit%10===1&&S.bit%100!==11?'':(S.bit%10>=2&&S.bit%10<=4&&(S.bit%100<10||S.bit%100>=20)?'а':'ов'));
  const M = { gold:'🥇', silver:'🥈', bronze:'🥉' };
  $('medals').textContent = Object.values(S.medals).map(m => M[m]).join('');
  $('sndBtn').textContent = !hasVoice() ? 'Голос: текстом' : (S.voiceOn ? '🔊 Светляк' : '🔈 Светляк');
  $('pgBtn').disabled = !pagerOn();
}
$('sndBtn').onclick = () => { S.voiceOn = !S.voiceOn; if (!S.voiceOn && 'speechSynthesis' in window) speechSynthesis.cancel(); save(); renderTop(); };

/* ================= ручка и тумблер ================= */
let moveBurst = { id:null, t:0 };
function countMove(id){
  const now = Date.now();
  if (moveBurst.id === id && now - moveBurst.t < 1500){ moveBurst.t = now; return false; }
  moveBurst = { id, t:now }; return true;
}
function knobHTML(id, name, mini){ return `<div class="knob" data-knob="${id}">
  <button class="kb" data-d="-1" aria-label="меньше">−</button>
  <div class="dial" tabindex="0" role="slider" aria-label="${esc(name)}"></div>
  <button class="kb" data-d="1" aria-label="больше">+</button>
  <button class="kname" ${mini?`data-mini="${mini}"`:''}>${esc(name)}</button><div class="kval"></div></div>`; }
function mountKnob(el, o){
  /* o: {get, set, min, max, step, fmt, onMove} */
  const dial = el.querySelector('.dial'), kv = el.querySelector('.kval');
  const draw = () => {
    const v = o.get(), p = (v-o.min)/(o.max-o.min), a = -135 + 270*p, r = a*Math.PI/180;
    const x = 32 + 20*Math.sin(r), y = 32 - 20*Math.cos(r);
    const arc = (deg) => { const t=deg*Math.PI/180; return [32+26*Math.sin(t), 32-26*Math.cos(t)]; };
    const [sx,sy] = arc(-135), [ex,ey] = arc(a);
    dial.innerHTML = `<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="26" fill="none" stroke="#2a3757" stroke-width="6"/>
      ${p>0.005?`<path d="M${sx} ${sy} A26 26 0 ${a+135>180?1:0} 1 ${ex} ${ey}" fill="none" stroke="#3ee6ff" stroke-width="6" stroke-linecap="round"/>`:''}
      <circle cx="32" cy="32" r="19" fill="#1b2540" stroke="#46557a" stroke-width="2"/>
      <line x1="32" y1="32" x2="${x}" y2="${y}" stroke="#ff5ad9" stroke-width="4" stroke-linecap="round"/></svg>`;
    kv.textContent = o.fmt ? o.fmt(v) : v;
    dial.setAttribute('aria-valuenow', v);
  };
  const setv = (v, commit) => {
    v = clamp(Math.round(v/o.step)*o.step, o.min, o.max); v = +v.toFixed(2);
    if (v === o.get()) return;
    o.set(v); draw(); o.onMove && o.onMove(commit);
  };
  el.querySelectorAll('.kb').forEach(b => b.onclick = () => setv(o.get() + o.step*(+b.dataset.d), true));
  let start = null;
  dial.onpointerdown = e => { start = { x:e.clientX, y:e.clientY, v:o.get() }; dial.setPointerCapture(e.pointerId); };
  dial.onpointermove = e => { if(!start) return; const d = (e.clientX-start.x) - (e.clientY-start.y); setv(start.v + d/160*(o.max-o.min), false); };
  dial.onpointerup = dial.onpointercancel = () => { if(start){ start=null; o.onMove && o.onMove(true); } };
  dial.onkeydown = e => { const d = {ArrowUp:1,ArrowRight:1,ArrowDown:-1,ArrowLeft:-1}[e.key]; if(d){ e.preventDefault(); setv(o.get()+d*o.step, true); } };
  dial.onwheel = e => { e.preventDefault(); setv(o.get() + (e.deltaY<0?1:-1)*o.step, true); };
  draw();
  return { draw };
}

/* ================= модель распознавания ================= */
function hear(P, c){
  const ph = T.phrases[P], W = ph.words;
  const out = W.map(w => ({ t:w.w.replace(/[,.:!?]/g,''), st:'ok', tag:'' }));
  const blame = new Set();
  const all = (st, tag, b) => { out.forEach(o => { o.st = st; o.tag = tag; }); blame.add(b); };
  if (!c.mic.on){ all('bad', T.hear.nomic, 'mic'); return { conf:0, out, blame, stop:'mic' }; }
  if (!c.phon.on){ all('bad', T.hear.nophon, 'phon'); return { conf:4, out, blame, stop:'phon' }; }
  if (!c.dict.on){
    out.forEach((o,i) => { o.t = o.t.toLowerCase().replace(/в/g,'ф').replace(/[ео]/g,'а'); o.st='bad'; o.tag=T.hear.nodict; });
    blame.add('dict'); return { conf:15, out, blame, stop:'dict' };
  }
  let conf = ph.noise ? 96 : 97;
  const m = c.mic.v, quiet = m < 35, loud = m > 75;
  const den = c.noise.on ? c.noise.v : 0;
  const mark = (i, st, tag, b) => { if (out[i].st === 'bad') return; out[i].st = st; out[i].tag = tag; blame.add(b); };
  if (ph.noise){
    if (den < 40){
      const weak = c.noise.on && den >= 20;
      W.forEach((w,i) => { if (w.n && (!weak || i === W.findIndex(x=>x.n))) mark(i,'bad',T.hear.noise,'noise'); });
      conf = weak ? 82 : (loud ? 62 : quiet ? 66 : 72);
    } else if (den > 80){
      W.forEach((w,i) => { if (w.q) mark(i,'bad',T.hear.eaten,'noise'); }); conf -= 12;
    }
  } else if (c.noise.on && den > 80){
    W.forEach((w,i) => { if (w.q) mark(i,'bad',T.hear.eaten,'noise'); }); conf -= 10;
  }
  if (quiet){
    W.forEach((w,i) => { if (w.q || (m < 20 && i%2)) mark(i,'bad',T.hear.quiet,'mic'); });
    conf -= m < 20 ? 30 : 9;
  }
  if (loud){
    mark(1, m > 85 ? 'bad' : 'warn', T.hear.loud, 'mic'); conf -= m > 85 ? 14 : 6;
    if (ph.noise && den < 40) conf = Math.min(conf, 62);
  }
  if (c.phon.v < 30){ W.forEach((w,i) => { if (w.q) mark(i,'bad',T.hear.quiet,'phon'); }); conf -= 8; }
  if (c.dict.v < 30){ mark(W.length-1,'bad',T.hear.nodict,'dict'); conf -= 10; }
  W.forEach((w,i) => {
    if (w.twin && (!c.sense.on || c.sense.v < 40)){ out[i].t = w.twin.join('? ') + '?'; mark(i,'warn',T.hear.twin,'sense'); conf -= 10; }
  });
  if (c.sense.on && c.sense.v > 85 && ph.over){ const [i, word] = ph.over; out[i].t = word.replace(/[,.:!?]/g,''); mark(i,'bad',T.hear.over,'sense'); conf -= 8; }
  conf = clamp(Math.round(conf), 0, 97);
  if (ph.noise && den < 40 && !(c.noise.on && den>=20)) conf = clamp(conf, 60, 80);
  const ok = out.every(o => o.st === 'ok') && conf >= 90;
  return { conf, out, blame, ok };
}

/* ================= разметка экрана с пультом ================= */
function seeded(n){ let s = n*9301+49297; return () => (s = (s*9301+49297)%233280)/233280; }
function waveSVG(P, res, sweep){
  const ph = T.phrases[P], n = ph.words.length, W = 1000, Hh = 96;
  const den = S.cfg.noise.on ? S.cfg.noise.v : 0;
  const noisy = ph.noise && den < 40;
  let x = 10, out = '';
  const total = ph.words.reduce((a,w) => a + w.w.length + 2, 0), k = (W-20)/total;
  ph.words.forEach((w, i) => {
    const len = (w.w.length + 2)*k, rnd = seeded(i+P.length*7+w.w.length);
    const st = res ? res.out[i].st : 'idle';
    const col = { idle:'#3ee6ff', ok:'#47f5a5', warn:'#ffd84a', bad:'#ff6b7a' }[st];
    if (res && st !== 'ok') out += `<rect x="${x}" y="2" width="${len-8}" height="${Hh-4}" rx="8" fill="${col}" opacity=".12"/>`;
    for (let b = x+3; b < x+len-10; b += 7){
      const h = (w.q ? 14 : 30) + rnd()*(w.q ? 14 : 34) * (S.cfg.mic.on ? S.cfg.mic.v/55 : 0.1);
      out += `<rect x="${b}" y="${Hh/2-h/2}" width="4" height="${Math.max(2,Math.min(h,Hh-6))}" rx="2" fill="${col}"/>`;
    }
    x += len;
  });
  if (noisy){ const r = seeded(3); for (let b = 10; b < W-10; b += 5){ const h = 8 + r()*16; out += `<rect x="${b}" y="${Hh/2-h/2}" width="2" height="${h}" fill="#a9b8d6" opacity=".35"/>`; } }
  if (sweep !== undefined) out += `<rect x="${10+sweep*(W-20)}" y="0" width="4" height="${Hh}" fill="#ff5ad9"/>`;
  return `<svg viewBox="0 0 ${W} ${Hh}" preserveAspectRatio="none" aria-hidden="true">${out}</svg>`;
}
function heardHTML(res){
  if (!res) return `<span style="color:var(--mut)">Нажми «Запуск» — здесь появится то, что услышала машина.</span>`;
  return res.out.map(o => `<span class="hw ${o.st}">${esc(o.t)}${o.tag?`<small>${esc(o.tag)}</small>`:''}</span>`).join('');
}
function thermColor(c){ return c >= 90 ? 'var(--gr)' : c >= 75 ? 'var(--ye)' : 'var(--rd)'; }

function pultHTML(opt){
  return `
  <div class="panel">
    <div class="waveWrap">
      <div class="wave">
        <div class="wlab"><span id="plabel"></span><span>Что услышала машина</span></div>
        <div id="wsvg"></div>
        <div class="hrow"><div class="heard" id="heard"></div><div class="runbox"><div class="mood" id="mood"></div><button class="btn big" id="runBtn">▶ Запуск</button></div></div>
      </div>
      <div class="therm"><div class="lab">уверенность<br>машины</div><div class="tube"><div class="fill" id="tfill"></div></div><div class="tval" id="tval"></div></div>
    </div>
  </div>
  <div class="pipe" id="pipe">${T.blocks.map(b => `
    <div class="blk" id="b-${b.id}">
      <button class="bname" data-mini="${b.id}">${esc(b.name)}</button>
      <div class="bstage">→ ${esc(b.stage)}</div>
      <button class="tog" id="t-${b.id}" aria-label="${esc(b.name)}: включить или выключить"></button>
      ${knobHTML(b.id, b.knob)}
      <div class="win" id="w-${b.id}"></div>
    </div>`).join('')}
  </div>`;
}
let PULT = { P:'P0', res:null, onRun:null, onChange:null, lastConf:null };
function mountPult(P, onRun, onChange){
  PULT = { P, res:null, onRun, onChange, lastConf:null };
  $('plabel').innerHTML = `<b>${esc(T.phrases[P].label)}</b>`;
  T.blocks.forEach(b => {
    const t = $('t-'+b.id);
    const sync = () => { t.setAttribute('aria-pressed', S.cfg[b.id].on); $('b-'+b.id).querySelector('.knob').classList.toggle('off', !S.cfg[b.id].on); };
    sync();
    t.onclick = () => { S.cfg[b.id].on = !S.cfg[b.id].on; sync(); beep(S.cfg[b.id].on?880:330,.05); changed(b.id+'-t', true); };
    mountKnob($('b-'+b.id).querySelector('.knob'), { get:()=>S.cfg[b.id].v, set:v=>S.cfg[b.id].v=v, min:0, max:100, step:5,
      onMove:(commit)=>changed(b.id+'-k', commit) });
  });
  $('runBtn').onclick = () => onRun && onRun();
  live(); drawWave();
}
let moodT = 0;
function changed(id, commit){
  const before = PULT.lastConf;
  live();
  if (commit){
    const isNew = countMove(id);
    PULT.onChange && PULT.onChange(id, isNew);
    const now = hear(PULT.P, S.cfg).conf;
    if (Date.now() - moodT > 2200 && before !== null && now !== before){
      moodT = Date.now(); $('mood').textContent = pick(now > before ? T.reactions.up : T.reactions.down);
    }
  }
  PULT.lastConf = hear(PULT.P, S.cfg).conf;
  save();
}
function live(){
  const r = hear(PULT.P, S.cfg);
  $('tfill').style.height = r.conf + '%'; $('tfill').style.background = thermColor(r.conf);
  $('tval').textContent = r.conf + '%';
  if (PULT.lastConf === null) PULT.lastConf = r.conf;
  drawWave();
}
function drawWave(sweep){ $('wsvg').innerHTML = waveSVG(PULT.P, PULT.res, sweep); $('heard').innerHTML = heardHTML(PULT.res); }
function clearWins(){ T.blocks.forEach(b => { $('w-'+b.id).innerHTML = ''; $('b-'+b.id).classList.remove('lit','err'); }); }
/* окошки блоков: что каждый блок сделал */
function fillWin(id, P, res){
  const ph = T.phrases[P], w = $('w-'+id);
  if (id === 'mic')   w.innerHTML = S.cfg.mic.on ? '〰 звук записан' : 'тишина';
  if (id === 'noise') w.innerHTML = Array.from({length:12}, () => '<span class="fr"></span>').join('');
  if (id === 'phon'){
    const tw = ph.words.find(x => x.twin);
    if (tw && res && res.out.some(o => o.st==='warn' && o.tag===T.hear.twin))
    { const snd = x => { const t = x.toLowerCase().replace(/д$/,'т').replace(/г$/,'к'); return '[' + t.slice(0,-1) + '<u>' + t.slice(-1) + '</u>]'; };
      w.innerHTML = `похожие звуки: <span class="tw">${snd(tw.twin[0])}</span> = <span class="tw">${snd(tw.twin[1])}</span>`; }
    else w.innerHTML = ph.sounds ? esc(ph.sounds) : (tw ? 'похожие звуки: —' : '[ … звуки … ]');
  }
  if (id === 'dict')  w.innerHTML = res.out.map(o => `<span class="wd">${esc(o.t)}</span>`).join(' ');
  if (id === 'sense') w.innerHTML = res.ok ? '«' + esc(res.out.map(o=>o.t).join(' ')) + '»' : '…';
}
/* запуск: волна пробегает, блоки загораются по очереди */
function animateRun(P, done, perBlock){
  const res = hear(P, S.cfg); PULT.res = null; clearWins();
  let t = 0; const steps = 30;
  $('runBtn').disabled = true;
  const iv = setInterval(() => {
    t++; drawWave(t/steps);
    if (t % 6 === 0){ const b = T.blocks[t/6-1]; if (b){ $('b-'+b.id).classList.add('lit'); if (perBlock !== false) fillWin(b.id, P, res); beep(500+t*15,.03,.03); } }
    if (t >= steps){
      clearInterval(iv); PULT.res = res; drawWave();
      T.blocks.forEach(b => { $('b-'+b.id).classList.remove('lit'); if (res.blame.has(b.id)) $('b-'+b.id).classList.add('err'); });
      $('runBtn').disabled = false;
      beep(res.ok ? 990 : 220, .15, .05);
      done(res);
    }
  }, 45);
}

/* ================= прошлая попытка ================= */
const BLK = Object.fromEntries(T.blocks.map(b => [b.id, b]));
function snapCfg(){ return JSON.parse(JSON.stringify(S.cfg)); }
function showPrev(last, nowCfg){
  const p = $('prev');
  if (!last){ p.classList.add('hidden'); return; }
  const diff = [];
  T.blocks.forEach(b => {
    const a = last.cfg[b.id], c = nowCfg[b.id];
    if (a.on !== c.on) diff.push(`${b.name}: ${a.on?'вкл':'выкл'} → ${c.on?'вкл':'выкл'}`);
    if (a.v !== c.v) diff.push(`${b.name}, ${b.knob}: ${a.v} → ${c.v}`);
  });
  p.classList.remove('hidden');
  p.innerHTML = `<h3>Прошлая попытка</h3>
    <div class="row"><span>уверенность</span><span class="big" style="color:${thermColor(last.conf)}">${last.conf}%</span></div>
    <div style="font-size:16px;margin-top:4px">«${esc(last.text)}»</div>
    ${diff.length ? `<ul>${diff.map(d=>`<li>${esc(d)}</li>`).join('')}</ul>` : '<ul><li>после неё ты ещё ничего не менял</li></ul>'}`;
}

/* ================= прогноз перед запуском ================= */
function askPredict(q, opts, go){
  sayShuf(q, opts, (i) => { S.pred = i; go(i); });
}
function predictReact(i, ok, worse){
  const actual = ok ? 0 : (worse ? 2 : 1);
  return i === actual ? T.predictRight : T.predictWrong;
}

/* ================= кто за пультом ================= */
const NM = i => S.names[i] || ('Стажёр ' + (i+1));
function pilotIdx(){
  const sc = S.screen;
  if (sc === 3 || sc === 5) return -1;
  if (sc === 0) return S.sub === 'train' ? 0 : -9;
  if (sc === 1) return 1;
  if (sc === 2) return S.trial === 'P3' ? 1 : 0;
  if (sc === 4) return 0;
  const F = S.fin;
  if (F.step === 'bonus') return S.bonus.step === 'B2' ? 1 : 0;
  if (F.step === 'dialogs') return 1;
  if (F.step === 'table') return 0;
  if (F.step === 'check') return -9;
  return -1;
}
function updatePilot(){
  const i = pilotIdx(), el = $('pilot');
  if (i === -9){ el.textContent = ''; return; }
  if (i === -1){ el.textContent = '✍ ' + T.pilot.both; return; }
  el.textContent = '🎮 ' + T.pilot.head.replace('{a}', NM(i)).replace('{b}', NM(1-i));
  if (S.lastPilot !== i){
    if (S.lastPilot !== undefined && S.lastPilot !== null){
      const bar = document.createElement('div'); bar.className = 'pilotbar';
      bar.textContent = '🔄 ' + T.pilot.say.replace('{a}', NM(i)).replace('{b}', NM(1-i));
      W.prepend(bar); beep(700,.06); setTimeout(() => beep(900,.06), 90);
      setTimeout(() => bar.remove(), 9000);
    }
    S.lastPilot = i; save();
  }
}

/* ================= экраны ================= */
const W = $('work');
function go(i){ S.screen = i; save(); render(); window.scrollTo(0,0); }
function render(){
  renderTop(); $('prev').classList.add('hidden'); H = { key:null, lines:null, level:1 };
  [scStart, scParse, scTrials, scNote1, scSynth, scNote2, scFinal][S.screen]();
  updatePilot();
}

/* ---------- 1. Смена началась ---------- */
function scStart(){
  if (S.sub === 'story'){
    W.innerHTML = `<section class="panel story"><h2>Ночная смена</h2>${T.story.map(p=>`<p>${esc(p)}</p>`).join('')}
      <div class="row" style="margin-top:14px"><button class="btn big" id="goNames">Принять смену</button>
      ${S.train||S.names[0] ? '<button class="btn ghost" id="restart">Новая смена (для другой пары)</button>' : ''}</div></section>`;
    $('goNames').onclick = () => { if (!S.t0) S.t0 = Date.now(); S.sub = 'names'; save(); scStart(); renderTop(); updatePilot(); };
    if ($('restart')) $('restart').onclick = () => { if (confirm('Начать смену заново? Прогресс этой пары сотрётся.')){ S = fresh(); save(); render(); } };
    say('Привет, стажёр! Я Светляк. Буду рядом всю смену. Нажми «Принять смену».');
    return;
  }
  if (S.sub === 'names'){
    W.innerHTML = `<section class="panel"><h2>Кто на смене?</h2><p>${esc(T.namesAsk)}</p>
      <div class="names"><input id="n1" placeholder="Стажёр 1" value="${esc(S.names[0])}" maxlength="20"><input id="n2" placeholder="Стажёр 2" value="${esc(S.names[1])}" maxlength="20"></div>
      <div class="row" style="margin-top:14px"><button class="btn big" id="goTrain">К пульту</button></div></section>`;
    $('goTrain').onclick = () => { S.names = [$('n1').value.trim(), $('n2').value.trim()]; S.sub = 'train'; save(); scStart(); updatePilot(); };
    say('Впишите имена. Можно и без них — тогда будете «Стажёр 1» и «Стажёр 2».');
    return;
  }
  /* обучение управлению на пробной фразе */
  W.innerHTML = `<div class="task" id="ttask"></div>` + pultHTML();
  mountPult('P0', () => {
    if (S.train < 3){ say('Сначала выполни задание сверху — потом запустим.'); return; }
    animateRun('P0', res => {
      if (res.ok){ S.train = 4; save(); say(T.trainingDone, ['Идём!'], () => { S.sub = 'done'; go(1); }); $('ttask').textContent = 'Пульт освоен!'; }
      else say('Термометр не зелёный. Смотри на красные блоки и поправь их, потом снова «Запуск».');
    });
  }, (id) => {
    if (S.train === 0 && id === 'mic-t' && !S.cfg.mic.on) S.train = 1;
    else if (S.train === 1 && id === 'mic-t' && S.cfg.mic.on) S.train = 2;
    else if (S.train === 2 && id === 'mic-k') S.train = 3;
    trainStep();
  });
  trainStep();
}
let lastTrain = -1;
function trainStep(){
  const st = T.training[Math.min(S.train, 3)];
  $('ttask').textContent = 'Задание: ' + st.say;
  ['mic','noise','phon','dict','sense'].forEach(id => $('b-'+id).classList.toggle('mini', id === 'mic' && S.train < 3));
  if (S.train < 4 && S.train !== lastTrain){ lastTrain = S.train; say(st.say); }
  save();
}

/* ---------- 2. Разбор машины ---------- */
function scParse(){
  W.innerHTML = `<div class="task" id="ptask">Фраза № 1 пришла на станцию. Нажми «Запуск» и смотри, как блоки загораются по очереди.</div>` + pultHTML();
  /* для разбора пульт ставим как было на станции */
  mountPult('P1', parseRun, () => {});
  if (S.parse.phase === 'q' && S.parse.i === 0 && !S.parse.started){ say('Слушай, к нам пришла первая фраза. Как думаешь, что машина сделает с ней сначала?', ['Запишет звук','Сразу напишет текст','Не знаю — проверим'], () => say('Проверим! Жми «Запуск».')); return; }
  resumeParse();
}
function parseRun(){
  if (S.parse.phase === 'exp' && S.parse.exp === 1){
    if (S.cfg.dict.on){ say('Сначала выключи тумблер «Словарь» — это наш опыт.'); return; }
    askPredict(T.experiment.ask, T.experiment.opts, () => {
      animateRun('P1', res => { S.parse.exp = 2; save(); expAfter(); });
    });
    return;
  }
  if (S.parse.phase === 'exp' && S.parse.exp >= 3){
    if (!S.cfg.dict.on){ say('Включи «Словарь» обратно, потом «Запуск».'); return; }
    animateRun('P1', res => { if (res.ok){ say(T.experiment.done, ['К испытаниям!'], () => go(2)); } else say('Что-то ещё мешает. Смотри на красный блок.'); });
    return;
  }
  /* разбор: блоки по одному */
  S.parse.started = true; save();
  animateRun('P1', res => { stageShow(S.parse.i); resumeParse(); }, false);
}
function stageShow(upto){
  const res = hear('P1', S.cfg);
  ['mic','noise','phon','dict','sense'].forEach((id, k) => { if (k <= upto+1) fillWin(id, 'P1', res); $('b-'+id).classList.toggle('lit', k === upto+1); });
}
function resumeParse(){
  if (!S.parse.started) return;
  if (S.parse.phase === 'q'){
    const st = T.parse[S.parse.i];
    stageShow(S.parse.i);
    $('ptask').textContent = 'Смотри на загоревшийся блок и его окошко. Ответь Светляку.';
    const ask = () => sayShuf(st.q, st.opts, (i) => {
      if (i === st.ok){
        S.parse.i++; S.parse.fails = 0; S.parse.level = 1; save();
        if (S.parse.i >= T.parse.length){ S.parse.phase = 'exp'; S.parse.exp = 1; save(); clearWins(); startExp(); }
        else resumeParse();
      } else {
        S.parse.fails++; S.parse.level = S.rush ? 3 : Math.min(3, S.parse.level+1); save();
        say(S.parse.level === 2 ? st.l2 : st.l3, ['Попробую ещё'], ask, {level:S.parse.level});
      }
    }, {}, 'parse' + S.parse.i);
    H = { key:'parse'+S.parse.i, lines:[st.q, st.l2, st.l3], level:S.parse.level };
    ask();
    return;
  }
  if (S.parse.phase === 'exp'){ if (S.parse.exp === 2) expAfter(); else if (S.parse.exp >= 3) { $('ptask').textContent = 'Включи «Словарь» обратно и нажми «Запуск».'; say('Включи «Словарь» обратно и нажми «Запуск».'); } else startExp(); }
}
function startExp(){
  $('ptask').textContent = 'Опыт: выключи тумблер «Словарь», потом «Запуск».';
  say(T.experiment.ask.split('.')[0] + '. Выключи тумблер «Словарь» и нажми «Запуск».');
}
function expAfter(){
  PULT.res = hear('P1', S.cfg); drawWave();
  T.blocks.forEach(b => $('b-'+b.id).classList.toggle('err', PULT.res.blame.has(b.id)));
  $('ptask').textContent = 'Смотри на волну и на красный блок. Ответь Светляку.';
  const E = T.experiment; let lvl = 1;
  const ask = () => sayShuf(E.after, E.afterOpts, (i) => {
    if (i === E.ok){ S.parse.exp = 3; save(); $('ptask').textContent = 'Включи «Словарь» обратно и нажми «Запуск».'; say('Верно! Включи «Словарь» обратно и нажми «Запуск».'); }
    else { lvl = Math.min(3, lvl+1); say(lvl === 2 ? E.l2 : E.l3, ['Попробую ещё'], ask, {level:lvl}); }
  }, {}, 'exp');
  H = { key:'exp', lines:[E.after, E.l2, E.l3], level:1 };
  ask();
}

/* ---------- 3. Испытания слуха ---------- */
function scTrials(){
  const P = S.trial, tr = S.tr[P], TT = T.trials[P];
  W.innerHTML = `<div class="task">${esc(TT.intro)} Настрой пульт, чтобы машина услышала всё верно. Термометр — зелёный.</div>` + pultHTML() +
    `<div class="row"><span style="color:var(--mut);font-size:16px">Застрял? Нажми «?» — Светляк подскажет. Или позвони специалисту на пейджер.</span></div>`;
  mountPult(P, trialRun, (id, isNew) => { if (isNew){ tr.moves++; save(); } });
  if (P[0] === 'B') $('plabel').innerHTML = `<b>${esc(T.bonus.names[P === 'B1' ? 0 : 1])}</b> · ${esc(T.phrases[P].label)}`;
  if (S.rush && tr.level < 3) tr.level = 3;
  ladder('tr'+P, [TT.l1, TT.l2, TT.l3], tr.level);
  showPrev(tr.last, S.cfg);
  if (tr.last){ PULT.res = null; drawWave(); }
  if (tr.fails >= 3) offerRollback();
}
const GOOD = { mic:{on:true,v:55}, noise:{on:true,v:60}, phon:{on:true,v:60}, dict:{on:true,v:70}, sense:{on:true,v:60} };
function preset(P){
  const c = fresh().cfg;
  if (P === 'P3') c.noise = { on:true, v:60 };
  if (P === 'B1'){ c.mic = { on:true, v:90 }; c.sense = { on:true, v:60 }; }
  if (P === 'B2'){ c.noise = { on:true, v:60 }; c.sense = { on:true, v:95 }; }
  return c;
}
function offerRollback(){
  const tr = S.tr[S.trial];
  say(T.rollback, ['Да, вернуть пульт','Нет, разберусь сам'], (i) => {
    if (i === 0){ S.cfg = preset(S.trial); tr.fails = 0; save(); scTrials(); say('Пульт как в начале испытания. Попробуй снова — спокойно, по одной ручке.'); }
    else { tr.fails = 0; save(); showLadder(); }
  });
}
function trialRun(){
  const P = S.trial, tr = S.tr[P], TT = T.trials[P];
  askPredict(T.predict.q, T.predict.opts, (pi) => {
    const before = tr.last ? tr.last.conf : null;
    animateRun(P, res => {
      tr.last = { conf:res.conf, text:res.out.map(o=>o.t).join(' '), cfg:snapCfg() };
      showPrev(tr.last, S.cfg);
      const worse = before !== null && res.conf < before;
      const react = predictReact(pi, res.ok, worse);
      if (res.ok){
        tr.done = true;
        const medal = tr.moves <= 2 ? 'gold' : tr.moves <= 4 ? 'silver' : 'bronze';
        S.medals[P] = medal; S.bit += 15 + (medal==='gold'?10:medal==='silver'?5:0);
        save(); renderTop();
        const name = { gold:'золотая', silver:'серебряная', bronze:'бронзовая' }[medal];
        const next = { P2:'К фразе № 3', P3:'К отчёту в тетради', B1:'К вызову 2', B2:'К вызову 3' }[P];
        H = { key:null, lines:null, level:1 };
        say(`${TT.win} Медаль ${name} за чистую настройку.`, [next], () => {
          if (P === 'P2'){ S.trial = 'P3'; save(); scTrials(); updatePilot(); say(T.trials.P3.l1, null, null, {level:1}); }
          else if (P === 'B1'){ S.trial = 'B2'; S.bonus.step = 'B2'; S.cfg = preset('B2'); save(); scTrials(); updatePilot(); say(T.trials.B2.l1, null, null, {level:1}); }
          else if (P === 'B2'){ S.bonus.step = 'synth'; save(); scFinal(); updatePilot(); }
          else go(3);
        });
        return;
      }
      tr.fails++; tr.level = clamp(tr.fails + 1, S.rush ? 3 : 1, 3); save();
      H.level = tr.level;
      say(react, null, null, {silent:true});
      if (S.rush){
        /* мастер по рации чинит первый сломанный блок */
        const b = T.blocks.find(x => res.blame.has(x.id));
        if (b){ S.cfg[b.id] = Object.assign({}, GOOD[b.id]); save();
          setTimeout(() => { const P2 = PULT.P; mountPult(P2, PULT.onRun, PULT.onChange); say(T.rush.trialHelp.replace('{block}', b.name)); }, 1600); return; }
      }
      setTimeout(() => { if (tr.fails >= 3) offerRollback(); else showLadder(); }, 1600);
    });
  });
}

/* ---------- 4 и 6. Тетради ---------- */
function noteScreen(N, key, next){
  const D = T[N];
  W.innerHTML = `<section class="panel"><h2>${esc(D.title)}</h2>
    <div class="task">Образец, как записать в тетрадь. Так работают специалисты: схема вместо длинного текста.</div></section>
    <section class="paper" id="kon"></section>
    <section class="panel"><div style="display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:16px">
      <div><h2 style="font-size:19px">Что сделать${S.rush?' — быстро':''}</h2><ol class="steps">${(S.rush ? T.rush[N] : D.steps).map(s=>`<li>${esc(s)}</li>`).join('')}</ol></div>
      <div><h2 style="font-size:19px">Как читать схему</h2><div class="legend">${T.legend.map(([a,b])=>`<b>${esc(a)}</b><span>${esc(b)}</span>`).join('')}</div></div>
    </div></section>
    <section class="panel"><div class="ready">${[0,1].map(i=>`<button data-i="${i}" aria-pressed="${S[key][i]}">✔ ${esc(S.names[i]||('Стажёр '+(i+1)))}: записал(а)</button>`).join('')}
      <button class="btn" id="nextBtn" ${S[key][0]&&S[key][1]?'':'disabled'}>Дальше</button></div></section>`;
  try { Konspekt.draw($('kon'), D.konspekt, { class:5, width:760 }); }
  catch(e){ $('kon').innerHTML = '<pre style="white-space:pre-wrap;font-size:18px">' + esc(D.konspekt) + '</pre>'; }
  W.querySelectorAll('.ready button[data-i]').forEach(b => b.onclick = () => {
    const i = +b.dataset.i; S[key][i] = !S[key][i]; save(); b.setAttribute('aria-pressed', S[key][i]);
    $('nextBtn').disabled = !(S[key][0] && S[key][1]);
  });
  $('nextBtn').onclick = next;
  say(N === 'note1' ? 'Перерисуйте схему в тетрадь. Подписи можно своими словами. И не забудьте про красный флаг!'
                    : 'Вторая схема — под первой. Сравните стрелки. И допишите одно главное отличие.');
}
function scNote1(){ noteScreen('note1', 'note1', () => go(4)); }
function scNote2(){ noteScreen('note2', 'note2', () => go(6)); }

/* ---------- 5. Голос машины ---------- */
const BON = () => S.screen === 6 && S.fin.step === 'bonus';
const TS  = () => BON() ? T.bonusSynth : T.synth;
const SYN = () => BON() ? S.syn2 : S.syn;
const CHS = () => Object.fromEntries(TS().chips.map(c => [c.id, c]));
function chipText(c, forSpeech){
  let t = c.text;
  if (c.homograph){
    const z = TS().zamok, pickd = SYN().zamok;
    t = t.replace('{ZAMOK}', forSpeech ? (pickd ? z.say[pickd] : 'замок') : (pickd ? z[pickd] : 'замок'));
  }
  return t.charAt(0).toUpperCase() + t.slice(1);
}
function normalize(t){ TS().normal.forEach(([a,b]) => { t = t.split(a).join(b); }); return t; }
function synthText(forSpeech){ return SYN().slots.filter(Boolean).map(id => chipText(CHS()[id], forSpeech)).join(' '); }
function scSynth(){
  const sy = SYN();
  if (S.rush && !BON() && !sy.rushFixed){ sy.rate = 1; sy.pitch = 1; sy.rushFixed = true; save(); setTimeout(() => say(T.rush.synthHelp), 50); }
  W.innerHTML = `
  <section class="panel"><div class="req"><div class="who"></div><div class="say">${esc(TS().request)}</div></div></section>
  <section class="panel">
    <div class="row" style="justify-content:space-between"><div class="rule">${esc(TS().rule)}</div></div>
    <div class="shelf" id="shelf" style="margin:10px 0"></div>
    <div style="font-size:15px;color:var(--mut);margin-bottom:6px">Готовые части ответа (нажми, чтобы положить на полку; на полке — нажми, чтобы убрать):</div>
    <div class="tray" id="tray"></div>
  </section>
  <section class="panel">
    <div class="spipe" id="spipe"></div>
    <div class="voice" style="margin-top:12px">
      <div id="kRate">${knobHTML('rate','Темп','rate')}</div>
      <div id="kPitch">${knobHTML('pitch','Высота','pitch')}</div>
      <div style="flex:1;min-width:240px;display:flex;flex-direction:column;gap:8px">
        <div class="machineSays" id="msays">Здесь появится ответ машины.</div>
        <div class="row"><button class="btn" id="listen">🔊 Послушать</button><button class="btn mg big" id="send">Отправить жителю</button></div>
      </div>
    </div>
  </section>
  <section class="honest">${esc(TS().honest)}</section>`;
  const fmtR = v => v < 0.8 ? v.toFixed(1)+' · медленно' : v > 1.25 ? v.toFixed(1)+' · быстро' : v.toFixed(1)+' · спокойно';
  const fmtP = v => v < 0.8 ? v.toFixed(1)+' · низко' : v > 1.3 ? v.toFixed(1)+' · пискляво' : v.toFixed(1)+' · обычно';
  const mv = (id) => (commit) => { if (commit && countMove(id)){ sy.moves++; } save(); drawSpipe(); };
  mountKnob($('kRate').firstElementChild,  { get:()=>sy.rate,  set:v=>sy.rate=v,  min:0.5, max:2, step:0.1, fmt:fmtR, onMove:mv('rate') });
  mountKnob($('kPitch').firstElementChild, { get:()=>sy.pitch, set:v=>sy.pitch=v, min:0.5, max:2, step:0.1, fmt:fmtP, onMove:mv('pitch') });
  drawShelf();
  $('listen').onclick = () => { if (!sy.slots.some(Boolean)){ say('Сначала положи на полку хотя бы одну часть ответа.'); return; } speakAnswer(); };
  $('send').onclick = synthSend;
  ladder('synth', [TS().l1, TS().l2[sy.err||'empty'], TS().l3[sy.err||'empty']], sy.level);
  if (!sy.slots.some(Boolean)) say(TS().intro); else showLadder();
  showSynthPrev();
}
function drawShelf(){
  const sy = SYN();
  $('shelf').innerHTML = sy.slots.map((id,k) => {
    if (!id) return `<div class="slot"><span class="n">место ${k+1}</span><span style="color:var(--mut)">пусто</span></div>`;
    const c = CHS()[id];
    const stress = c.homograph ? `<div class="stress">${['a','b'].map(x=>`<button data-z="${x}" aria-pressed="${sy.zamok===x}">${TS().zamok[x]}</button>`).join('')}</div>` : '';
    return `<div class="slot full" data-k="${k}"><span class="n">место ${k+1} · нажми, чтобы убрать</span><span>${esc(chipText(c))}</span>${stress}</div>`;
  }).join('');
  $('shelf').querySelectorAll('.slot.full').forEach(el => el.onclick = (e) => {
    if (e.target.dataset.z) return;
    sy.slots[+el.dataset.k] = null; sy.moves++; save(); drawShelf();
  });
  $('shelf').querySelectorAll('[data-z]').forEach(b => b.onclick = (e) => { e.stopPropagation(); sy.zamok = b.dataset.z; sy.moves++; save(); drawShelf(); });
  const used = new Set(sy.slots.filter(Boolean));
  $('tray').innerHTML = TS().chips.map(c => { const t = c.text.replace('{ZAMOK}','замок'); return `<button class="part ${used.has(c.id)?'used':''}" data-id="${c.id}" ${used.has(c.id)?'disabled':''}>${esc(t.charAt(0).toUpperCase()+t.slice(1))}</button>`; }).join('');
  $('tray').querySelectorAll('.part').forEach(b => b.onclick = () => {
    const k = sy.slots.indexOf(null);
    if (k < 0){ say('Полка полная. Убери часть, чтобы положить другую.'); return; }
    sy.slots[k] = b.dataset.id; sy.moves++; save(); drawShelf();
  });
  drawSpipe();
}
function drawSpipe(){
  const raw = synthText(false), nrm = normalize(raw);
  const z = SYN().zamok;
  const sounds = !SYN().slots.some(Boolean) ? '' : !SYN().slots.includes('c1') ? '…звуки готовы' : (z ? (z === 'a' ? '…[за́мак]…' : '…[замо́к]…') : '…[зам?к] — где ударение?');
  const st = TS().stages;
  $('spipe').innerHTML = `<div class="sst"><b>${st[0]}</b>${esc(raw)||'—'}</div><div class="sst"><b>${st[1]}</b>${esc(nrm)||'—'}</div>
    <div class="sst"><b>${st[2]}</b>${esc(sounds)||'—'}</div><div class="sst"><b>${st[3]}</b>темп ${SYN().rate.toFixed(1)}, высота ${SYN().pitch.toFixed(1)}</div>`;
}
function speakAnswer(done){
  const t = normalize(synthText(true));
  $('listen').disabled = true;
  machineSpeak(t, SYN().rate, SYN().pitch, $('msays'), () => { $('listen').disabled = false; $('msays').textContent = normalize(synthText(false)); done && done(); });
}
function synthCheck(){
  const sy = SYN(), sl = sy.slots;
  if (sl.some(x => !x)) return 'empty';
  const order = ['приветствие','суть','уточнение'];
  if (sl.some((id,k) => CHS()[id].type !== order[k])) return 'order';
  if (sl.some(id => !CHS()[id].fit)) return 'fit';
  if (sy.zamok !== TS().zamok.ok) return 'stress';
  if (sy.rate < 0.8 || sy.rate > 1.25 || sy.pitch < 0.8 || sy.pitch > 1.3) return 'voice';
  return null;
}
function showSynthPrev(){
  const l = SYN().last, p = $('prev');
  if (!l){ p.classList.add('hidden'); return; }
  p.classList.remove('hidden');
  p.innerHTML = `<h3>Прошлая попытка</h3><div style="font-size:16px">«${esc(l.text)}»</div><ul><li>темп ${l.rate.toFixed(1)}, высота ${l.pitch.toFixed(1)}</li><li>${esc(l.verdict)}</li></ul>`;
}
function synthSend(){
  const sy = SYN();
  askPredict(T.predict.synthQ, T.predict.synthOpts, (pi) => {
    const err = synthCheck();
    const verdict = { empty:'на полке не хватает частей', order:'части не по правилу', fit:'часть не про просьбу жителя', stress:'ударение не там', voice:'голос неспокойный' }[err] || 'житель всё понял';
    sy.last = { text: normalize(synthText(false)), rate:sy.rate, pitch:sy.pitch, verdict }; save(); showSynthPrev();
    const actual = !err ? 0 : (err === 'voice' ? 1 : 2);
    const react = pi === actual ? T.predictRight : T.predictWrong;
    speakAnswer(() => {
      if (!err){
        sy.done = true;
        const medal = sy.moves <= 7 ? 'gold' : sy.moves <= 10 ? 'silver' : 'bronze';
        S.medals[BON() ? 'b3' : 'syn'] = medal; S.bit += 15 + (medal==='gold'?10:medal==='silver'?5:0); save(); renderTop();
        H = { key:null, lines:null, level:1 };
        const bon = BON();
        say(TS().win + ' Медаль ' + { gold:'золотая', silver:'серебряная', bronze:'бронзовая' }[medal] + '.', [bon ? 'Сдать вызов' : 'К отчёту в тетради'], () => {
          if (bon){ S.bonus.step = 'end'; save(); scFinal(); updatePilot(); } else go(5);
        });
        return;
      }
      sy.fails++; sy.err = err; sy.level = clamp(sy.fails + 1, 1, 3); save();
      H = { key:'synth', lines:[TS().l1, TS().l2[err], TS().l3[err]], level:sy.level };
      say(react, null, null, {silent:true});
      setTimeout(() => {
        if (sy.fails >= 3){
          say('Три попытки. Вернуть голос как был в начале? Части на полке останутся, битрейты и медали — тоже.', ['Да, вернуть ручки','Нет, разберусь'], (i) => {
            if (i === 0){ sy.rate = TS().startVoice[0]; sy.pitch = TS().startVoice[1]; } sy.fails = 0; save(); scSynth();
          });
        } else showLadder();
      }, 1600);
    });
  });
}

/* ---------- 7. Финал ---------- */
function scFinal(){
  const F = S.fin;
  if (F.step === 'dialogs') return finDialogs();
  if (F.step === 'table') return finTable();
  if (F.step === 'check') return finCheck();
  if (F.step === 'bonus') return scBonus();
  return finEnd();
}
function finDialogs(){
  const F = S.fin, keys = ['F1','F2','F3'];
  W.innerHTML = `<section class="panel"><h2>Живой разговор</h2><div class="task">${esc(T.final.intro)}</div></section>
    <section class="panel"><div class="wave"><div class="wlab"><span id="flab"></span><span>Что услышала машина</span></div><div id="fwave"></div><div class="heard" id="fheard"></div></div>
      <div class="machineSays" id="fsays" style="margin-top:10px">…</div>
      <div class="row" style="margin-top:10px"><button class="btn big" id="fnext"></button></div></section>
    <section class="dlg" id="dlg"></section>`;
  const cards = () => { $('dlg').innerHTML = keys.map((k,i) => { const r = F.res[i];
      return `<div class="dcard ${r?(r.ok?'ok':'no'):''}"><span class="t">${esc(T.phrases[k].label)}</span><span>«${esc(T.phrases[k].words.map(w=>w.w).join(' '))}»</span><span>${r?(r.ok?'✔ понял и ответил':'✖ '+esc(r.why)):'ждёт'}</span></div>`; }).join(''); };
  const btn = () => {
    const b = $('fnext');
    if (F.i < 3){ b.textContent = `Позвать жителя ${F.i+1}`; b.onclick = () => runDialog(F.i); }
    else { b.textContent = 'Дальше: свой конспект'; b.onclick = () => { F.step = 'table'; save(); scFinal(); updatePilot(); }; }
  };
  const P = keys[Math.min(F.i,2)];
  $('flab').innerHTML = `<b>${esc(T.phrases[P].label)}</b>`;
  $('fwave').innerHTML = waveSVG(P, null);
  $('fheard').innerHTML = heardHTML(null);
  cards(); btn();
  say(F.i < 3 ? 'Зовите жителей по одному. Слушайте, что услышала машина и что она ответила.' : 'Разговоры закончены. Теперь соберите свой конспект.');
  function runDialog(i){
    const P = keys[i]; $('fnext').disabled = true;
    $('flab').innerHTML = `<b>${esc(T.phrases[P].label)}</b>`;
    const res = hear(P, S.cfg); let t = 0;
    const iv = setInterval(() => {
      t++; $('fwave').innerHTML = waveSVG(P, t>=30?res:null, t<30?t/30:undefined);
      if (t >= 30){ clearInterval(iv); $('fheard').innerHTML = heardHTML(res); answer(); }
    }, 45);
    function answer(){
      if (!res.ok){ finish(false, 'машина не расслышала', T.final.answers.fail); return; }
      if (P === 'F3'){
        say(T.final.duhiAsk, [T.final.duhi.a, T.final.duhi.b], (k) => {
          const ch = k === 1 ? 'b' : 'a'; F.duhi = ch; save();
          const word = T.final.duhi[ch];
          const txt = T.final.answers.F3.replace('{DUHI}', word[0].toUpperCase() + word.slice(1));
          finish(ch === T.final.duhi.ok, 'ударение не там', txt, ch !== T.final.duhi.ok ? T.final.duhiWrong : null);
        });
        return;
      }
      finish(true, '', T.final.answers[P]);
    }
    function finish(ok, why, txt, note){
      const voiceOk = S.syn.rate >= 0.8 && S.syn.rate <= 1.25 && S.syn.pitch >= 0.8 && S.syn.pitch <= 1.3;
      if (ok && !voiceOk){ ok = false; why = 'голос неспокойный'; }
      machineSpeak(normalize(txt).replace(/\b10\b/,'десять'), S.syn.rate, S.syn.pitch, $('fsays'), () => {
        $('fsays').textContent = txt;
        F.res[i] = { ok, why }; F.i = i+1; save(); cards(); btn(); $('fnext').disabled = false;
        say(note || (ok ? 'Житель доволен!' : 'Житель ушёл в сомнениях: ' + why + '.'));
      });
    }
  }
}
function tableText(){
  const t = S.fin.table, v = (k) => t[k] || '…';
  return `тема: Слушает или говорит?
связка: Распознавание | Синтез
${T.final.rows.map((r,i) => `${r.q} -> ${v(i+'a')} | ${v(i+'b')}`).join('\n')}`;
}
function finTable(){
  const F = S.fin, R = T.final.rows;
  if (S.rush){ [0,1].forEach(i => ['a','b'].forEach(x => { F.table[i+x] = R[i][x]; })); save(); }
  W.innerHTML = `<section class="panel"><h2>Свой конспект</h2><div class="task">${esc(S.rush ? T.rush.table : T.final.tableIntro)}</div>
    <div class="ttab" style="margin-top:10px"><span></span><span class="h">Распознавание<br><small style="color:var(--mut)">машина слушает</small></span><span class="h">Синтез<br><small style="color:var(--mut)">машина говорит</small></span>
    ${R.map((r,i) => `<b>${esc(r.q)}</b>${['a','b'].map(s => `<select data-c="${i}${s}" aria-label="${esc(r.q)}" ${S.rush && i < 2 ? 'disabled' : ''}><option value="">— выбери —</option>${T.final.chips.map(c=>`<option ${F.table[i+s]===c?'selected':''}>${esc(c)}</option>`).join('')}</select>`).join('')}`).join('')}
    </div>
    <div class="row" style="margin-top:12px"><button class="btn mg big" id="tcheck">Проверить конспект</button></div></section>
    <section class="paper" id="tkon"></section>`;
  const draw = () => { try { Konspekt.draw($('tkon'), tableText(), { class:5, width:760 }); } catch(e){ $('tkon').textContent = tableText(); } };
  W.querySelectorAll('select').forEach(s => s.onchange = () => { F.table[s.dataset.c] = s.value; s.classList.remove('bad'); save(); draw(); });
  draw();
  ladder('table', [T.final.l1, T.final.l2.replace('{row}', R[0].q), T.final.l3], F.tlevel);
  $('tcheck').onclick = () => {
    const wrong = [];
    R.forEach((r,i) => ['a','b'].forEach(s => { if (F.table[i+s] !== r[s]) wrong.push(i+s); }));
    if (!wrong.length){
      F.tdone = true; save(); H = { key:null, lines:null, level:1 };
      say(T.final.tableWin, ['Записали — дальше'], () => { F.step = 'check'; save(); scFinal(); updatePilot(); });
      return;
    }
    F.tfails++; F.tlevel = clamp(F.tfails + 1, 1, 3); save();
    const row = R[+wrong[0][0]].q;
    H = { key:'table', lines:[T.final.l1, T.final.l2.replace('{row}', row), T.final.l3], level:F.tlevel };
    if (F.tlevel >= 3) wrong.forEach(c => W.querySelector(`select[data-c="${c}"]`).classList.add('bad'));
    showLadder();
  };
  say(S.rush ? T.rush.table : T.final.tableIntro);
}
function finCheck(){
  const F = S.fin, Q = S.rush ? T.check.qs.slice(0,2) : T.check.qs, names = [S.names[0]||'Стажёр 1', S.names[1]||'Стажёр 2'];
  const SP = Object.fromEntries(T.specialists.map(s => [s.id, s]));
  const done = Q.every((q,i) => F.ans[i].to && F.ans[i].why !== undefined);
  W.innerHTML = `<section class="panel"><h2>Отчёт специалистам</h2><div class="task">${esc(T.check.intro)}${S.rush ? ' ' + esc(T.rush.check) : ''}</div></section>` +
    Q.map((q,i) => {
      const a = F.ans[i];
      let fb = '';
      if (F.sent){
        const roleOk = a.to === q.to, whyOk = a.why === q.ok;
        fb = roleOk && whyOk ? `<div class="fb g">${esc(q.good)}</div>`
           : `<div class="fb b">${roleOk ? '' : esc(T.check.roleWrong.replace('{who}', SP[a.to].name)) + ' '}${esc(q.bad)}</div>`;
      }
      return `<section class="qcard"><div class="who">Отвечает: ${esc(names[i%2])}</div><div style="font-weight:700">${esc(q.q)}</div>
        <div class="opts">${T.specialists.map(s => `<button data-q="${i}" data-to="${s.id}" aria-pressed="${a.to===s.id}">${esc(s.name)}</button>`).join('')}</div>
        ${a.to ? `<div style="margin-top:8px;font-size:16px;color:var(--mut)">Зачем он нужен?</div><div class="opts">${order('why'+i, q.why.length).map(k => `<button data-q="${i}" data-why="${k}" aria-pressed="${a.why===k}">${esc(q.why[k])}</button>`).join('')}</div>` : ''}
        ${fb}</section>`;
    }).join('') +
    `<section class="panel"><div class="row">${F.sent ? `<span>${esc(T.check.again)}</span><button class="btn mg big" id="endBtn">Завершить смену</button>` : `<button class="btn mg big" id="sendRep" ${done?'':'disabled'}>Отправить отчёт</button>`}</div></section>`;
  W.querySelectorAll('[data-to]').forEach(b => b.onclick = () => { const a = F.ans[+b.dataset.q]; a.to = b.dataset.to; delete a.why; save(); finCheck(); });
  W.querySelectorAll('[data-why]').forEach(b => b.onclick = () => { F.ans[+b.dataset.q].why = +b.dataset.why; save(); finCheck(); });
  if ($('sendRep')) $('sendRep').onclick = () => { F.sent = true; save(); finCheck(); say('Специалисты ответили. Прочитайте. Если хотите — поменяйте ответ.'); };
  if ($('endBtn')) $('endBtn').onclick = () => { F.step = 'end'; save(); scFinal(); updatePilot(); };
  if (!F.sent) say('Отвечайте по очереди: имя над вопросом — тот и выбирает. Сначала кого позвать, потом — зачем.', null, null, {silent:true});
}
function finEnd(){
  const n = S.fin.res.filter(r => r && r.ok).length, m = mins();
  const E = T.endings.find(e => n >= e.min);
  const M = { gold:'🥇', silver:'🥈', bronze:'🥉' };
  const bonusDone = S.bonus.step === 'end';
  const early = m < T.clock.bonusUntil;
  const miss = [['note1', T.note1], ['note2', T.note2]].filter(([k]) => !S[k].every(Boolean));
  W.innerHTML = `<section class="panel ending"><h2>${esc(E.title)}</h2><p style="font-size:21px">${esc(E.text)}</p>
    ${bonusDone ? `<p style="font-size:21px;color:var(--gr)"><b>${esc(T.bonus.done.title)}</b> ${esc(T.bonus.done.text)}</p>` : ''}
    <p>Жителей поняли: <b>${n} из 3</b> · ${esc(String(S.bit))} битрейтов · медали: ${Object.values(S.medals).map(x=>M[x]).join(' ') || '—'}</p></section>
    <!--CONCL-->
    ${miss.map(([k,D],i) => `<section class="panel"><div class="task">${esc(T.late.note)}</div></section><section class="paper" id="miss${i}"></section>`).join('')}
    `;
  const frames = S.rush ? T.oral.frames.slice(0, T.oral.rushN) : T.oral.frames;
  const concl = `<section class="panel"><h2>${esc(T.oral.title)}</h2>
    <div class="task" style="margin-bottom:8px">${esc(T.oral.intro)}${S.rush ? ' ' + esc(T.rush.oral) : ''}</div>
    <ol class="oral">${frames.map(f=>`<li>${esc(f)}</li>`).join('')}</ol>
    <p style="color:var(--mut)">${esc(T.oral.hint)}</p></section>`;
  const bonusCard = !S.bonus.step && early ? `<section class="panel event" style="max-width:none;width:auto"><h2>${esc(T.bonus.call.title)}</h2><p>${esc(T.bonus.call.text)}</p><button class="btn mg big" id="bonusGo">${esc(T.bonus.call.btn)}</button></section>` : '';
  const extra = bonusDone ? `<section class="panel"><div class="task">${esc(T.ending.wait)} ${esc(T.ending.wait2)}</div></section>` : '';
  W.innerHTML = W.innerHTML.replace('<!--CONCL-->', concl + bonusCard + extra);
  miss.forEach(([k,D],i) => { try { Konspekt.draw($('miss'+i), D.konspekt, { class:5, width:760 }); } catch(e){} });
  if ($('bonusGo')) $('bonusGo').onclick = () => {
    S.fin.step = 'bonus'; S.bonus.step = 'B1'; S.trial = 'B1'; S.cfg = preset('B1'); save(); render(); window.scrollTo(0,0);
  };
  if (!S.bonus.step && early) say('Сначала — свой вывод в тетрадь. Записали? Тогда вас ждёт тревожный вызов!');
  else say(bonusDone ? T.ending.wait2 : 'Смена окончена! Теперь каждый пишет свой вывод в тетрадь — фразы на экране.');
}
function scBonus(){
  const b = S.bonus.step;
  if (b === 'B1' || b === 'B2'){ S.trial = b; return scTrials(); }
  if (b === 'synth') return scSynth();
  S.fin.step = 'end'; save(); renderTop(); return finEnd();
}

/* ================= часы смены ================= */
function showEvent(t, x, btn, cb){
  $('evT').textContent = t; $('evX').textContent = x; $('evB').textContent = btn;
  $('evB').onclick = () => { $('event').classList.add('hidden'); cb && cb(); };
  $('event').classList.remove('hidden'); beep(440,.12); setTimeout(() => beep(660,.12), 160);
  helperSpeak(x);
}
function checkTime(){
  if (!S.t0) return;
  renderTop();
  if (!$('event').classList.contains('hidden') || !$('tmenu').classList.contains('hidden')) return;
  const m = mins();
  if (S.screen < 6 && S.rush < 2 && m >= T.clock.late){
    S.rush = 2;
    S.cfg = JSON.parse(JSON.stringify(GOOD));
    if (!S.syn.done) Object.assign(S.syn, { slots:['g1','c1','u1'], zamok:'b', rate:1, pitch:1, done:true });
    S.fin = fresh().fin; save();
    showEvent(T.late.title, T.late.text, T.late.btn, () => go(6));
    return;
  }
  if (S.screen <= 4 && !S.rush && m >= T.clock.rush){
    S.rush = 1; save();
    showEvent(T.rush.title, T.rush.text, T.rush.btn, () => render());
  }
}
setInterval(checkTime, 10000);

/* ================= пейджер ================= */
let typingTimer = null;
function openPager(){
  if (!pagerOn()){ say('Специалисты на связи во время испытаний.'); return; }
  $('pager').classList.remove('hidden'); pagerHome();
}
$('pgBtn').onclick = openPager;
$('pgClose').onclick = () => $('pager').classList.add('hidden');
const pagerOn = () => S.screen === 2 || S.screen === 4 || (S.screen === 6 && S.fin.step === 'bonus' && ['B1','B2','synth'].includes(S.bonus.step));
const synthCtx = () => S.screen === 4 || (S.screen === 6 && S.fin.step === 'bonus' && S.bonus.step === 'synth');
function ctxHyps(){ return synthCtx() ? T.hyps.synth : T.hyps.recog; }
function pagerHome(){
  if (S.pager.busy) return pagerChat();
  $('pbody').innerHTML = `<div style="font-size:16px;color:var(--mut)">${esc(T.help.pager)} Ответ стоит ${T.cost} битрейтов. Не тот специалист — переадресует бесплатно.</div>` +
    T.specialists.map(s => `<button class="spec" data-s="${s.id}"><b>${esc(s.name)}</b><span>${esc(s.who)}</span></button>`).join('');
  $('pbody').querySelectorAll('[data-s]').forEach(b => b.onclick = () => pagerAsk(b.dataset.s));
}
function pagerAsk(sid){
  const sp = T.specialists.find(s => s.id === sid);
  $('pbody').innerHTML = `<div class="msg"><b>${esc(sp.name)}</b> на связи. Что ты заметил?</div>` +
    ctxHyps().map(h => `<button class="chip mg" data-h="${h.id}">${esc(h.text)}</button>`).join('') +
    `<button class="btn ghost" id="pback">← К списку</button>`;
  $('pback').onclick = pagerHome;
  $('pbody').querySelectorAll('[data-h]').forEach(b => b.onclick = () => {
    const h = ctxHyps().find(x => x.id === b.dataset.h);
    if (h.to !== sid){
      const who = T.specialists.find(s => s.id === h.to).name;
      $('pbody').innerHTML = `<div class="msg me">${esc(h.text)}</div><div class="msg"><b>${esc(sp.name)}:</b>\n${esc(T.redirect.replace('{who}', who))}</div>
        <button class="btn mg" id="pto">Написать: ${esc(who)}</button><button class="btn ghost" id="pback">← К списку</button>`;
      $('pto').onclick = () => pagerAsk(h.to); $('pback').onclick = pagerHome; return;
    }
    if (S.bit < T.cost){ $('pbody').insertAdjacentHTML('afterbegin', `<div class="msg">Не хватает битрейтов. Пройди испытание — и звони.</div>`); return; }
    S.bit -= T.cost; renderTop();
    const mini = pick(synthCtx() ? T.mini.synth : T.mini.recog);
    S.pager = { busy:true, sid, hid:h.id, shown:'', full:h.a, more:false, mini:mini.block, miniSay:mini.say, miniDone:false, log:[] };
    save(); pagerChat(); typeReply();
  });
}
function pagerChat(){
  const P = S.pager, sp = T.specialists.find(s => s.id === P.sid), h = [...T.hyps.recog, ...T.hyps.synth].find(x => x.id === P.hid);
  const typingDone = P.shown.length >= P.full.length;
  $('pbody').innerHTML = `<div class="msg me">${esc(h.text)}</div>
    <div class="msg"><b>${esc(sp.name)}:</b>\n${esc(P.shown)}${typingDone?'':'▌'}</div>
    ${typingDone ? '' : `<div class="typing">${esc(sp.name)} печатает…</div>`}
    ${P.miniDone ? `<div class="msg" style="border-color:#235a72">${esc(T.mini.done)}</div>` : `<div class="msg" style="border-color:var(--ye)"><b style="color:var(--ye)">${esc(T.mini.intro)}</b> ${esc(P.miniSay)}</div>`}
    ${typingDone && P.miniDone && !P.more ? `<button class="chip mg" id="pmore">Уточнить (бесплатно)</button>` : ''}
    ${typingDone ? `<button class="btn ghost" id="pend">Закончить разговор</button>` : ''}`;
  if ($('pmore')) $('pmore').onclick = () => { P.more = true; P.full = P.full + '\n\n' + h.more; save(); pagerChat(); typeReply(); };
  if ($('pend')) $('pend').onclick = () => { S.pager = { busy:false, log:[] }; markMini(null); save(); pagerHome(); };
  markMini(P.miniDone ? null : P.mini);
}
function typeReply(){
  clearTimeout(typingTimer);
  const step = () => {
    const P = S.pager; if (!P.busy) return;
    if (P.shown.length >= P.full.length){ save(); pagerChat(); return; }
    P.shown = P.full.slice(0, P.shown.length + 1);
    const box = $('pbody').querySelector('.msg:nth-child(2)');
    if (box && !$('pager').classList.contains('hidden')) box.innerHTML = `<b>${esc(T.specialists.find(s=>s.id===P.sid).name)}:</b>\n${esc(P.shown)}▌`;
    typingTimer = setTimeout(step, 1000 / T.typingSpeed);
  };
  step();
}
function markMini(id){
  document.querySelectorAll('.blk.mini').forEach(e => e.classList.remove('mini'));
  if (id && $('b-'+id)) $('b-'+id).classList.add('mini');
}
document.addEventListener('click', e => {
  const t = e.target.closest('[data-mini]'); const P = S.pager;
  if (!t || !P || !P.busy || P.miniDone) return;
  if (t.dataset.mini === P.mini){ P.miniDone = true; beep(1200,.06); save(); if (!$('pager').classList.contains('hidden')) pagerChat(); else markMini(null); }
});

/* ================= учитель: Ctrl+Alt+M ================= */
function fillDefaults(i){
  if (!S.t0) S.t0 = Date.now();
  S.bonus = { step:null };
  if (i >= 1){ S.sub = 'done'; S.train = 4; }
  if (i >= 2){ S.parse = { i:4, phase:'exp', exp:4, fails:0, level:1, started:true }; S.cfg.dict.on = true; }
  if (i === 2){ const f = fresh(); S.trial = 'P2'; S.tr = f.tr; S.cfg = f.cfg; }
  if (i >= 3){ S.cfg.noise = { on:true, v:60 }; S.cfg.sense = { on:true, v:60 }; S.tr.P2.done = S.tr.P3.done = true; S.trial = 'P3'; }
  if (i >= 4){ S.note1 = [true,true]; }
  if (i >= 5){ S.syn.slots = ['g1','c1','u1']; S.syn.zamok = 'b'; S.syn.rate = 1; S.syn.pitch = 1; S.syn.done = true; }
  if (i >= 6){ S.note2 = [true,true]; }
  if (i < 6){ S.fin = fresh().fin; }
  S.pager = { busy:false, log:[] };
}
function teacherMenu(){
  $('tlist').innerHTML = T.screens.map((s,i) => `<button class="btn ghost" data-i="${i}">${esc(s.name)} · ${s.min} мин</button>`).join('') +
    `<button class="btn ghost" data-i="b">7+. Сверхурочный вызов</button>` +
    `<div style="color:var(--mut);font-size:15px;margin-top:6px">Часы смены: ${S.t0 ? mins() + ' мин' : 'не запущены'}${S.rush ? ' · режим «мастер на связи»' : ''}</div>` +
    `<button class="btn ghost" data-i="c0">Часы смены: начать с нуля</button>` +
    `<button class="btn ghost" data-i="c5">Часы смены: +5 минут</button>` +
    `<button class="btn ghost" data-i="p">Лист для вклейки (печать)</button>` +
    `<button class="btn ghost" data-i="r">Новая смена (стереть прогресс)</button>`;
  $('tlist').querySelectorAll('button').forEach(b => b.onclick = () => {
    $('tmenu').classList.add('hidden');
    const d = b.dataset.i;
    if (d === 'r'){ S = fresh(); save(); render(); return; }
    if (d === 'p'){ window.open('vkleyka.html', '_blank'); return; }
    if (d === 'c0'){ S.t0 = Date.now(); S.rush = 0; save(); renderTop(); return; }
    if (d === 'c5'){ S.t0 = (S.t0 || Date.now()) - 5*60000; save(); checkTime(); return; }
    if (d === 'b'){ fillDefaults(6); S.fin.res = [{ok:true},{ok:true},{ok:true}]; S.fin.i = 3; S.fin.step = 'bonus'; S.bonus.step = 'B1'; S.trial = 'B1'; S.cfg = preset('B1'); go(6); return; }
    const i = +d; fillDefaults(i); go(i);
  });
  $('tmenu').classList.remove('hidden');
}
$('tclose').onclick = () => $('tmenu').classList.add('hidden');
document.addEventListener('keydown', e => { if (e.ctrlKey && e.altKey && e.code === 'KeyM'){ e.preventDefault(); teacherMenu(); } });

/* ================= старт ================= */
initVoice();
setTimeout(() => { RU = findVoice(); renderTop(); }, 1200);
render();
if (S.pager && S.pager.busy){ typeReply(); }
</script>
</body>
</html>

===== КОНЕЦ ФАЙЛА: 5-klass/ekho-uzel/index.html =====

===== ФАЙЛ: 5-klass/ekho-uzel/tekst.js =====
/* «Эхо-Узел» — все тексты урока.
   Этот файл читают и игра (index.html), и страница учителя (kanva.html):
   правка здесь меняет обе. Помощник ≤ 2 строк, специалист ≤ 3 строк. */
const T = {

  station: 'Эхо-Узел',
  helper: 'Светляк',

  screens: [
    { id:'start',  name:'1. Смена началась',          min:'0–4'   },
    { id:'parse',  name:'2. Разбор машины',           min:'4–8'   },
    { id:'trials', name:'3. Испытания слуха',         min:'8–16'  },
    { id:'note1',  name:'4. Тетрадь: как машина слушает', min:'16–19' },
    { id:'synth',  name:'5. Голос машины',            min:'19–28' },
    { id:'note2',  name:'6. Тетрадь: как машина говорит', min:'28–30' },
    { id:'final',  name:'7. Живой разговор',          min:'30–40' }
  ],

  /* ===== 1. Заставка и сюжет ===== */
  story: [
    'Неоновый квартал. Ночь. В квартале сломалась речевая станция «Эхо-Узел».',
    'Эхо слушает жителей и отвечает им голосом. А сейчас она путает слова и говорит странно.',
    'Мастер смены уехал на другой вызов. На смене — вы, стажёры. Раньше вы такого не чинили.',
    'С вами пейджер. В нём помощник Светляк и номера специалистов. Удачной смены!'
  ],
  namesAsk: 'Как зовут стажёров? Впишите имена — по очереди вы будете отвечать в конце смены.',

  training: [
    { do:'mic-toggle',  say:'Это тумблер. Щёлкни его — выключи микрофон станции.' },
    { do:'mic-toggle2', say:'Видишь, термометр упал? Включи микрофон обратно.' },
    { do:'mic-knob',    say:'Это ручка громкости. Покрути её: тяни мышкой или жми «+» и «−». Смотри на термометр.' },
    { do:'run',         say:'Почти середина — то что надо. Нажми «Запуск»: пусть машина послушает пробную фразу.' }
  ],
  trainingDone: 'Отлично, пульт ты освоил. Идём разбирать машину!',

  /* ===== фразы жителей ===== */
  /* n — слово тонет в шуме; q — тихое слово; twin — слова-близнецы; over — что машина «додумает», если угадывать слишком сильно */
  phrases: {
    P0: { label:'Пробная фраза', noise:0, words:[{w:'Проверка'},{w:'связи:'},{w:'раз,'},{w:'два,'},{w:'три.'}], over:[1,'свиньи:'] },
    P1: { label:'Фраза № 1 · чистая запись', noise:0,
          words:[{w:'Эхо,'},{w:'включи'},{w:'свет'},{w:'в',q:1},{w:'подъезде.'}], over:[4,'подвале.'],
          sounds:'[э́ха]  [фкл’уч’и́]  [св’э́т]  [фпад’jэ́з’д’и]' },
    P2: { label:'Фраза № 2 · рядом гудит вентиляция', noise:1,
          words:[{w:'Эхо,'},{w:'позвони',n:1},{w:'маме',n:1},{w:'на',q:1},{w:'работу.',n:1}], over:[2,'Маше'] },
    P3: { label:'Фраза № 3 · слова-близнецы', noise:0,
          words:[{w:'Эхо,'},{w:'запиши'},{w:'код',twin:['КОТ','КОД']},{w:'от'},{w:'двери.'}], over:[1,'закажи'] },
    F1: { label:'Житель 1 · на улице шумно', noise:1,
          words:[{w:'Эхо,'},{w:'закажи'},{w:'такси',n:1},{w:'к',q:1},{w:'школе.',n:1}], over:[2,'тесто'] },
    F2: { label:'Житель 2', noise:0,
          words:[{w:'Эхо,'},{w:'для'},{w:'супа'},{w:'купи'},{w:'лук.',twin:['ЛУГ','ЛУК']}], over:[2,'сока'] },
    F3: { label:'Житель 3', noise:0,
          words:[{w:'Эхо,'},{w:'где'},{w:'купить'},{w:'духи'},{w:'маме?'}], over:[4,'Маше?'] },
    B1: { label:'Эхо-2 · вызов 1', noise:1,
          words:[{w:'Эхо,'},{w:'вызови',n:1},{w:'лифт',n:1},{w:'на',q:1},{w:'пятый'},{w:'этаж.',n:1}], over:[5,'пляж.'] },
    B2: { label:'Эхо-2 · вызов 2', noise:0,
          words:[{w:'Эхо,'},{w:'на'},{w:'реке'},{w:'строим'},{w:'плот.',twin:['ПЛОД','ПЛОТ']}], over:[2,'руке'] }
  },

  blocks: [
    { id:'mic',   name:'Микрофон',            stage:'звук',                    knob:'громкость' },
    { id:'noise', name:'Шумодав',             stage:'кадры',                   knob:'сила' },
    { id:'phon',  name:'Цех звуков (фонем)',  stage:'звуки речи (фонемы)',     knob:'внимание' },
    { id:'dict',  name:'Словарь',             stage:'слова',                   knob:'запас слов' },
    { id:'sense', name:'Угадывание по смыслу', stage:'предложение',            knob:'смелость' }
  ],

  /* ===== 2. Разбор машины (фраза № 1) ===== */
  parse: [
    { stage:1, q:'Смотри: машина порезала запись на полоски. Как думаешь, зачем?',
      opts:['Чтобы разглядеть каждый кусочек','Чтобы запись стала короче','Просто так'], ok:0,
      l2:'Смотри на окошко «кадры»: кусочки одинаковые или разные?',
      l3:'Книгу читают по строчке, а не всю сразу. Машина так же — по кусочку. Зачем ей это?' },
    { stage:2, q:'В цехе звуков «включи» стало [фкл’уч’и́]. Почему не так, как пишем в тетради?',
      opts:['Машина слышит звуки, а не буквы','Машина ошиблась','Так короче'], ok:0,
      l2:'Скажи «включи» вслух. Ты слышишь [в] или [ф] в начале?',
      l3:'Мы пишем «в», а говорим [ф] — как в «вкусно». Машина записывает то, что слышно.' },
    { stage:3, q:'Из звуков вышли слова. Как машина узнала, что [св’э́т] — это «свет»?',
      opts:['Нашла в словаре','Придумала сама','Спросила человека'], ok:0,
      l2:'Смотри, какой блок загорелся, когда появились слова.',
      l3:'Ты ищешь незнакомое слово в словаре. Машина тоже. Какой блок ей помог?' },
    { stage:4, q:'Последний блок поставил запятую и точку. Что получилось в конце?',
      opts:['Целое предложение','Набор букв','Одно слово'], ok:0,
      l2:'Смотри на нижнее окошко «предложение». Что там написано?',
      l3:'Отдельные слова — как бусины. Последний блок нанизал их на нитку. Что вышло?' }
  ],
  experiment: {
    ask:'А теперь опыт. Выключи тумблер «Словарь». Как думаешь, что будет после запуска?',
    opts:['Слова сломаются','Ничего не изменится','Машина замолчит'],
    after:'Смотри на волну. На каком блоке машина остановилась?',
    afterOpts:['На словаре','На микрофоне','На шумодаве'], ok:0,
    l2:'Звуки в цехе есть, а слов нет. Какой блок между ними?',
    l3:'Буквы есть, а слова не сложились — как пазл без картинки на коробке. Кто подсказывает слова?',
    done:'Верно. Каждый блок — своё звено цепочки. Включи словарь обратно — и вперёд к испытаниям!'
  },

  /* ===== 3. Испытания ===== */
  trials: {
    P2: { intro:'Фраза № 2. Рядом гудит вентиляция — слышишь шорох на волне?',
          l1:'Посмотри на волну: где красные кусочки? Что ещё звучит на записи?',
          l2:'Смотри на блок «Шумодав» — он сейчас работает?',
          l3:'Шум — как песок в воде, шумодав — как фильтр. Включи его и поставь ручку на середину.',
          win:'Шум не мешает! Термометр зелёный.' },
    P3: { intro:'Фраза № 3. Житель просит записать то, что открывает дверь.',
          l1:'Слушай, машина выдала два варианта: КОТ и КОД. Как думаешь, почему она не смогла выбрать один?',
          l2:'Смотри на окошко «похожие звуки» — что там подсвечивается?',
          l3:'КОТ и КОД на конце звучат одинаково — как близнецы. Какая ручка угадывает по соседним словам? Подкрути её.',
          win:'КОД! Машина догадалась по соседним словам.' },
    B1: { intro:'Эхо-2: житель просит лифт, а рядом гудит вентиляция. Мастер говорит: поломок тут две.',
          l1:'Посмотри на волну и на подписи под словами. Сколько разных бед ты видишь?',
          l2:'Смотри на два блока: «Микрофон» и «Шумодав». Что с каждым не так?',
          l3:'Громче — не чище: как кричать в трубку, когда шумно. Убавь микрофон и включи шумодав.',
          win:'Обе поломки найдены! Эхо-2 слышит лифт.' },
    B2: { intro:'Эхо-2: житель рассказывает про реку. А машина слышит то, чего не было.',
          l1:'Смотри на красное слово. Житель правда это сказал?',
          l2:'Смотри на ручку «смелость» в блоке «Угадывание по смыслу». Где она стоит?',
          l3:'Как болтун, который договаривает за тебя и ошибается. Сделай угадывание поскромнее — к середине.',
          win:'Машина больше не додумывает! И плот не перепутала с плодом.' }
  },
  rollback: 'Три попытки — а машина капризничает. Вернуть пульт как было? Битрейты и медали останутся.',

  predict: {
    q:'Как думаешь, что покажет термометр после запуска?',
    opts:['Станет зелёным','Останется как был','Станет хуже'],
    synthQ:'Как думаешь, как прозвучит ответ?',
    synthOpts:['Понятно и спокойно','Слишком быстро или пискляво','Ответ будет странный']
  },
  predictRight:'Ты угадал! Значит, понимаешь, как работает эта ручка.',
  predictWrong:'Интересно: ты ждал одно, а вышло другое. Почему так?',

  reactions: {
    up:   ['Ну наконец-то!','Так-так, уже лучше.','Вот это настройка!','Ой, как чисто стало!'],
    down: ['Ой, опять шум…','Я запутался…','Ух, как громко!','Тише-тише, я слушаю.']
  },

  /* окошко «что услышала машина» */
  hear: {
    noise:'шум съел слово',
    quiet:'слишком тихо',
    loud:'перегруз — хрипит',
    eaten:'шумодав съел звук',
    twin:'два варианта',
    over:'машина додумала',
    nodict:'слово не найдено',
    nophon:'звуки не разобраны',
    nomic:'тишина'
  },

  /* ===== пейджер: специалисты ===== */
  specialists: [
    { id:'eng',  name:'Инженер Вольт',        who:'настраивает, как машина слышит',
      look:'коротко, по-деловому, сравнивает с техникой', markers:['«Коротко:»','сравнения с техникой','«Проверь.»'] },
    { id:'ling', name:'Лингвист Буквоед',      who:'знает всё про звуки речи и ударения',
      look:'дотошный, ворчит, но добрый', markers:['«Ну слушай…»','«Опять двадцать пять!»','«голубчик»'] },
    { id:'snd',  name:'Звукорежиссёр Тембр',  who:'записывает голоса и слушает, как звучит',
      look:'артист, говорит образами', markers:['«Ах!»','звук — тесто, голос — ткань','«Чувствуешь?»'] },
    { id:'dlg',  name:'Дизайнер диалогов Реплика', who:'придумывает, что машина ответит человеку',
      look:'объясняет через житейские случаи', markers:['«Представь…»','«по-житейски»','«Договорились?»'] }
  ],
  redirect: 'Хороший вопрос, но это не ко мне — спроси у {who}, он как раз про это.',
  cost: 10,
  typingSpeed: 4.5,   /* знаков в секунду — как печатает взрослый */

  hyps: {
    recog: [
      { id:'h1', text:'Кажется, машине мешает шум вентиляции.', to:'eng',
        a:'Коротко: шум — как песок в воде. Шумодав — фильтр, как для воды. Он у тебя включён? Проверь.',
        more:'Коротко: слишком сильный фильтр задерживает и воду. Не крути шумодав до упора. Проверь.' },
      { id:'h2', text:'Кажется, машина путает слова, которые звучат одинаково.', to:'ling',
        a:'Ну слушай… КОД и КОТ на конце звучат одинаково, голубчик. Ухо тут бессильно. А ты сам как бы догадался?',
        more:'Опять двадцать пять! Кота на двери не записывают. Какая ручка смотрит на соседние слова, голубчик?' },
      { id:'h3', text:'Кажется, запись слишком тихая или слишком громкая.', to:'snd',
        a:'Ах! Звук — это тесто: мало — не слепишь, много — лезет через край. Ручку микрофона — к середине. Чувствуешь?',
        more:'Ах, громче — не значит чище! Шум растёт вместе с голосом. Чувствуешь разницу?' },
      { id:'h4', text:'Кажется, машина не понимает, чего хочет человек.', to:'dlg',
        a:'Представь: звонишь бабушке, а в трубке шипит. Ты переспросишь, а машина — нет. Сначала пусть услышит. Договорились?',
        more:'По-житейски: понять смысл можно, только когда слова уже разобраны. Посмотри, где сейчас красное.' }
    ],
    synth: [
      { id:'s1', text:'Кажется, машина ставит ударение не туда.', to:'ling',
        a:'Ну слушай… За́мок — у короля, замо́к — на двери. Буквы те же, голубчик! Найди, где машине подсказать ударение.',
        more:'Опять двадцать пять! Ду́хи и духи́ — та же история. Смотри, о чём просит человек.' },
      { id:'s2', text:'Кажется, голос звучит неживым: слишком быстро или пискляво.', to:'snd',
        a:'Ах! Голос — это ткань. Тянешь быстро — рвётся, слишком высоко — визжит. Найди середину на слух. Чувствуешь?',
        more:'Ах, послушай два раза: до и после. Ухо не обманет.' },
      { id:'s3', text:'Кажется, машина не знает, как читать цифры.', to:'eng',
        a:'Коротко: машина видит «6», а сказать должна «шести». Как перевод с цифр на слова. Текст готовят до звука. Проверь.',
        more:'Коротко: «ул.» — «улица», «2 кг» — «два килограмма». Всё это — до голоса. Проверь окошко «текст».' },
      { id:'s4', text:'Кажется, машина сама придумывает слова для ответа.', to:'dlg',
        a:'Представь открытку из готовых наклеек. Эта машина так же: части ответа написали люди заранее. Договорились?',
        more:'По-житейски: машина выбирает, какую часть взять и в каком порядке, — по правилам. Вот и вся хитрость.' }
    ]
  },
  mini: {
    intro:'Пока специалист печатает — разминка:',
    recog:[ { block:'noise', say:'нажми на название блока «Шумодав».' },
            { block:'dict',  say:'нажми на название блока «Словарь».' },
            { block:'mic',   say:'нажми на название блока «Микрофон».' },
            { block:'sense', say:'нажми на название блока «Угадывание по смыслу».' } ],
    synth:[ { block:'rate',  say:'нажми на название ручки «Темп».' },
            { block:'pitch', say:'нажми на название ручки «Высота».' } ],
    done:'Готово! Можно уточнить у специалиста — бесплатно.'
  },

  /* ===== 5. Голос машины ===== */
  synth: {
    request:'Эхо, у меня сломался замок на двери. Что делать?',
    rule:'Правило машины: приветствие → суть → уточнение',
    honest:'Эта машина не придумывает слова сама. Части ответа написали люди заранее. Машина выбирает части и собирает их по правилам.',
    chips: [
      { id:'g1', type:'приветствие', text:'Здравствуйте!', fit:1 },
      { id:'g2', type:'приветствие', text:'Добрый вечер!', fit:1 },
      { id:'g3', type:'приветствие', text:'Пока-пока!', fit:0 },
      { id:'c1', type:'суть', text:'Мастер починит {ZAMOK} сегодня до 6.', fit:1, homograph:true },
      { id:'c2', type:'суть', text:'Завтра в квартале будет дождь.', fit:0 },
      { id:'c3', type:'суть', text:'Музей открыт с 10 до 18.', fit:0 },
      { id:'u1', type:'уточнение', text:'Позвать мастера прямо сейчас?', fit:1 },
      { id:'u2', type:'уточнение', text:'Хотите послушать песню?', fit:0 },
      { id:'u3', type:'уточнение', text:'Купить вам зонт?', fit:0 }
    ],
    zamok: { a:'за́мок', b:'замо́к', ok:'b', say:{ a:'за́мок', b:'замо́к' } },
    normal: [['до 6','до шести'],['с 10 до 18','с десяти до восемнадцати']],
    stages: ['текст','подготовка текста: цифры → слова','звуки речи (фонемы)','звук'],
    intro:'Житель спрашивает про замок на двери. Собери ответ из готовых частей и настрой голос.',
    l1:'Послушай ответ целиком. Что бы ты сам сказал жителю иначе?',
    l2: { order:'Смотри на правило машины над полкой: в каком порядке идут части?',
          fit:'Перечитай просьбу жителя. Каждая часть ответа — про это?',
          stress:'Смотри на слово с ударением в ответе. На какой слог оно сейчас?',
          voice:'Смотри на ручки «Темп» и «Высота». Где они сейчас стоят?',
          empty:'Смотри на полку ответа: все три места заняты?' },
    l3: { order:'Как в письме: сначала «здравствуйте», потом дело, потом вопрос. Переставь части.',
          fit:'Просишь в магазине хлеб — тебе не дают зонт. Убери лишнюю часть.',
          stress:'За́мок — у короля, замо́к — на двери. Какой нужен жителю?',
          voice:'Как диктор по радио: не тараторит и не пищит. Поставь ручки ближе к середине.',
          empty:'Ответ — как бутерброд из трёх слоёв. Положи все три.' },
    win:'Житель всё понял! Ответ собран по правилам, голос спокойный.'
  },

  /* ===== тетради (образцы ДРАКОН-ГРАФ) ===== */
  note1: {
    title:'Отчёт для специалистов № 1',
    konspekt: /*конспект*/`тема: Как машина слушает?
пример: [звук]{микрофон} → [кадры]{шумодав} → [звуки речи (фонемы)]{цех звуков} → [слова]{словарь} → [предложение]{угадывание по смыслу}
Что мешает? -> Шум и слова-близнецы.`,
    steps:[
      'Перерисуй схему в тетрадь. Овал, рамку и кружки — как на образце.',
      'Подписи под кружками можно писать своими словами.',
      'Под схемой допиши: «Красный флаг ставлю на … , потому что …» Каждый стажёр — свой ответ.'
    ]
  },
  note2: {
    title:'Отчёт для специалистов № 2',
    konspekt: /*конспект*/`тема: Как машина говорит?
пример: [текст]{«6» → «шести»} → [звуки речи (фонемы)]{где ударение?} → [звук]{темп и высота}
Что мешает? -> Ударения, омографы (за́мок — замо́к), интонация.`,
    steps:[
      'Перерисуй схему под первой. Сравни: куда идут стрелки там и здесь?',
      'Допиши одно главное отличие: «Синтез отличается от распознавания тем, что …»'
    ]
  },
  legend: [
    ['овал','тема — о чём схема'],
    ['белая рамка','разберись: пример по частям'],
    ['кружок','часть примера'],
    ['жёлтая выноска','подпись к части — запомни'],
    ['флажок →','вопрос, справа — ответ']
  ],

  /* ===== 7. Финал ===== */
  final: {
    intro:'Станция готова? Проверим на настоящих жителях. Эхо слушает вашим пультом и говорит вашим голосом.',
    answers: {
      F1:'Здравствуйте! Такси приедет к школе через 10 минут. Прислать номер машины?',
      F2:'Добрый день! Лук добавила в список покупок. Купить ещё морковь?',
      F3:'Здравствуйте! {DUHI} продают на первом этаже. Подсказать дорогу?',
      fail:'Простите, я не расслышала. Повторите, пожалуйста.'
    },
    duhi: { a:'ду́хи', b:'духи́', ok:'b' },
    duhiAsk:'Эхо собирает ответ. В нём слово «духи». Как его прочитать?',
    duhiWrong:'Житель удивился: ду́хи — это привидения! А мама ждёт духи́ — то, чем пахнут.',
    tableIntro:'Теперь соберите свой конспект. Выберите, что вписать в каждую клетку. Программа нарисует схему.',
    rows: [
      { q:'Что на входе?',  a:'звук',  b:'текст' },
      { q:'Что на выходе?', a:'текст', b:'звук' },
      { q:'Что мешает?',    a:'шум, слова-близнецы', b:'ударения, омографы' }
    ],
    chips: ['звук','текст','шум, слова-близнецы','ударения, омографы'],
    l1:'Сравни свою таблицу с двумя схемами в тетради. Где не совпало?',
    l2:'Посмотри на строку «{row}». Что машина получает, когда слушает? А когда говорит?',
    l3:'Слушает — как ухо: в него входит звук. Говорит — как рот: в него входит готовый текст.',
    tableWin:'Схема собрана! Перепишите её в тетрадь — это ваш итог урока.'
  },

  check: {
    intro:'Отчёт специалистам. Отвечайте по очереди: имя на экране — тот и выбирает.',
    qs: [
      { q:'В шумном цеху машина плохо понимает рабочих. Кого позовёшь?', to:'eng',
        why:['Включит и настроит шумодав','Перепишет ответы машины','Сделает голос машины выше'], ok:0,
        good:'Инженер благодарит: про шум ты понял хорошо.',
        bad:'Про шум загляни ещё раз на пульт: блок «Шумодав» и разговор с инженером.' },
      { q:'Машина говорит «за́мок» там, где нужен «замо́к». Кого позовёшь?', to:'ling',
        why:['Подскажет машине, где ударение','Уберёт шум','Поставит новый микрофон'], ok:0,
        good:'Лингвист ворчит, но доволен: про ударения ты понял.',
        bad:'Про ударения загляни ещё раз в «Голос машины»: слово «замок».' },
      { q:'Голос машины тараторит и пищит. Кого позовёшь?', to:'snd',
        why:['Подберёт темп и высоту на слух','Добавит слов в словарь','Напишет новые ответы'], ok:0,
        good:'Звукорежиссёр в восторге: ты слышишь голос, как мастер.',
        bad:'Про голос загляни ещё раз на ручки «Темп» и «Высота».' },
      { q:'На вежливую просьбу машина отвечает «Ошибка. Повторите». Люди обижаются. Кого позовёшь?', to:'dlg',
        why:['Заранее напишет понятные части ответа','Включит шумодав посильнее','Сделает голос ниже'], ok:0,
        good:'Дизайнер диалогов улыбается: ты понял, откуда берутся ответы.',
        bad:'Откуда берутся ответы — загляни ещё раз в правило машины: части ответа пишут люди.' }
    ],
    roles: { eng:'инженер', ling:'лингвист', snd:'звукорежиссёр', dlg:'дизайнер диалогов' },
    roleWrong:'{who} благодарит за звонок, но это не к нему.',
    again:'Можно пересмотреть ответы до отправки отчёта.'
  },

  endings: [
    { min:3, title:'Эхо снова в строю!',
      text:'Все три жителя поняли станцию. Утром мастер смены читает ваш отчёт и вручает пропуск: «Мастер речевых машин».' },
    { min:2, title:'Эхо работает, но иногда переспрашивает',
      text:'Двое жителей довольны, один ушёл в сомнениях. Мастер оставит записку: что подкрутить завтра. Смена засчитана!' },
    { min:0, title:'Эхо кашляет, но держится',
      text:'Жители пока путаются. Но вы нашли, где ломается цепочка, — а это половина ремонта. Мастер доделает утром по вашему отчёту.' }
  ],
  /* личный вывод: каждый пишет в тетради сам; в спешке — первые 3 фразы */
  oral: {
    title:'Твой вывод — в тетрадь',
    intro:'Каждый дописывает фразы в тетради сам, своими словами. Напарнику не подсказывать! Потом сверьтесь.',
    hint:'Подсказка — в ваших схемах в тетради.',
    rushN:3,
    frames:[
      'Машина слушает, когда превращает … в … .',
      'Машина говорит, когда превращает … в … .',
      'Слуху машины больше всего мешает … .',
      'Голосу машины больше всего мешает … .',
      'Чат-бот соединяет … и … .'
    ]
  },

  /* ===== развилки по часам смены ===== */
  clock: { rush:29, late:36, bonusUntil:35 },   /* минуты от «Принять смену» */
  rush: {
    title:'Мастер на связи',
    text:'Стажёры, это мастер смены. Я возвращаюсь, жители уже собираются у станции! Работаем быстрее — я помогу по рации.',
    btn:'Понял, ускоряемся',
    trialHelp:'Мастер подкрутил по рации блок «{block}». Посмотри, что он поменял, и запускай.',
    synthHelp:'Звукорежиссёр подстроил голос по рации. Ваше дело — части ответа и ударение.',
    note1:['Нарисуй только цепочку: 5 кружков со стрелками и подписи.','Красный флаг — скажи соседу вслух, писать не нужно.'],
    note2:['Под первой схемой допиши одну строку: текст → звуки речи → звук.','И одно главное отличие: «Синтез отличается от распознавания тем, что …»'],
    table:'Верхние строки мастер вписал сам. Выберите, что мешает слуху и голосу машины. В тетрадь — только эту строку.',
    check:'Отчёт короткий: по одному вопросу каждому.',
    oral:'Вывод короткий: первые три фразы.'
  },
  late: {
    title:'Мастер вернулся',
    text:'Я на месте! Жители ждут. Остальное я докрутил сам — покажите станцию людям.',
    btn:'Звать жителей',
    note:'Схема не успела попасть в тетрадь? Вот она — перепишите после урока.'
  },
  ending: {
    wait:'Вы закончили раньше времени — отличная смена!',
    wait2:'Осталось время: нарисуйте в тетради свою схему чат-бота. Тема в овале, шаги в кружках: что машина делает сначала, что потом.'
  },
  bonus: {
    call:{ title:'Тревога в соседнем квартале!',
      text:'Станция-близнец «Эхо-2» сломалась хуже нашей. Её мастер видел ваш отчёт и просит помощи. Возьмёте сверхурочный вызов?',
      btn:'Взять вызов' },
    names:['Вызов 1: две поломки сразу','Вызов 2: слишком смелая машина','Вызов 3: старый замок'],
    done:{ title:'Эхо-2 заговорила!',
      text:'Соседний квартал снова слышит свою станцию. Мастер выписывает вам пропуск: «Старший мастер речевых машин».' }
  },

  /* кто за пультом: второй стажёр — штурман, читает задание вслух и советует */
  pilot: {
    head:'За пультом: {a} · штурман: {b}',
    both:'Пишут оба',
    say:'Меняемся! За пультом — {a}. {b} — штурман: читает задание вслух и советует.'
  },

  help: {
    none:'Сейчас всё идёт как надо. Читай задание на экране сверху.',
    pager:'Пейджер: позвони специалисту, если застрял. Ответ стоит битрейты.'
  }
};
/* сверхурочный вызов 3: тот же конструктор голоса, другой житель */
T.bonusSynth = Object.assign({}, T.synth, {
  request:'Эхо, во сколько открывается старый замок на холме?',
  intro:'Эхо-2: житель спрашивает про старый замок на холме — там музей. Голос у этой станции тоже сбит.',
  chips: [
    { id:'g1', type:'приветствие', text:'Здравствуйте!', fit:1 },
    { id:'g2', type:'приветствие', text:'Добрый вечер!', fit:1 },
    { id:'g3', type:'приветствие', text:'Пока-пока!', fit:0 },
    { id:'c1', type:'суть', text:'{ZAMOK} на холме открыт с 10 до 18.', fit:1, homograph:true },
    { id:'c2', type:'суть', text:'Мастер починит дверь до 6.', fit:0 },
    { id:'c3', type:'суть', text:'Завтра в квартале будет дождь.', fit:0 },
    { id:'u1', type:'уточнение', text:'Рассказать, как туда доехать?', fit:1 },
    { id:'u2', type:'уточнение', text:'Купить вам зонт?', fit:0 },
    { id:'u3', type:'уточнение', text:'Хотите послушать песню?', fit:0 }
  ],
  zamok: { a:'за́мок', b:'замо́к', ok:'a', say:{ a:'за́мок', b:'замо́к' } },
  startVoice: [0.6, 0.6],
  win:'Житель Эхо-2 всё понял: за́мок на холме, а не замо́к на двери!'
});
T.synth.startVoice = [1.8, 1.7];
if (typeof module !== 'undefined') module.exports = T;

===== КОНЕЦ ФАЙЛА: 5-klass/ekho-uzel/tekst.js =====

===== ФАЙЛ: 5-klass/ekho-uzel/kanva.html =====
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Канва урока «Эхо-Узел»</title>
<style>
:root{--ink:#1d2126;--ink2:#5b5346;--line:#d9cfb9;--paper:#f6f1e6;--accent:#f2a93b}
*{box-sizing:border-box}
html,body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 "Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
.bar{position:sticky;top:0;z-index:5;display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 16px;background:#1f2329;color:#eef1f4;border-bottom:3px solid var(--accent)}
.bar a,.bar button{font:inherit;font-size:14px;color:#eef1f4;background:#272c33;border:1px solid #3a414a;border-radius:18px;padding:5px 12px;text-decoration:none;cursor:pointer}
.bar button{background:var(--accent);color:#2a1d05;border-color:var(--accent);font-weight:700}
.bar .t{flex:1;min-width:0;color:#a9b2bc;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.doc{max-width:900px;margin:20px auto 48px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:28px 34px}
h1{font-size:28px;line-height:1.25;margin:0 0 12px}
h2{font-size:21px;margin:28px 0 10px;padding-bottom:4px;border-bottom:1px solid var(--line)}
h3{font-size:17px;margin:20px 0 8px}
p{margin:8px 0}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:14.5px}
th,td{border:1px solid #cfc5ae;padding:6px 8px;vertical-align:top;text-align:left}
th{background:#f3ecdd}
blockquote{margin:10px 0;padding:8px 14px;border-left:4px solid var(--accent);background:#fbf6ea}
ul,ol{padding-left:24px}
.k{color:var(--ink2);font-size:14px}
.ok{color:#1e7a4a;font-weight:700} .no{color:#a3471f;font-weight:700}
.kon{margin:10px 0;border:1px solid var(--line);border-radius:8px;padding:8px}
a{color:#1f5fa8}
@media (max-width:600px){.doc{padding:18px 16px;margin:10px 8px}table{font-size:13px}}
@media print{
  html,body{background:#fff}.bar{display:none}
  .doc{border:0;border-radius:0;margin:0;padding:0;max-width:none}
  h2{break-after:avoid} tr,blockquote,.kon{break-inside:avoid}
  a{color:inherit;text-decoration:none} @page{size:A4;margin:14mm}
}
</style>
</head>
<body>
<div class="bar"><a href="../../dlya-uchitelya.html">← Для учителя</a><span class="t">Канва урока «Эхо-Узел»</span><a href="index.html">Открыть игру</a><button type="button" onclick="window.print()">Печать</button></div>
<main class="doc">
<h1>«Эхо-Узел»: как машина слушает и говорит</h1>
<p>ИИ и информационная безопасность · 5 класс · 40 минут · 4 пары · вводный урок блока о речевых технологиях. Опора — прошлый урок о сложностях компьютерного зрения («Где ИИ ошибается»).</p>
<blockquote>Работа в паре: на каждом экране игра пишет, кто за пультом, а кто штурман (читает задание вслух и советует); роли меняются по ходу смены. В тетради пишут оба. Варианты ответов перемешаны — верный не всегда первый.</blockquote>
<blockquote>Урок проходит без учителя-предметника: всю методику ведёт игра. Помощник Светляк задаёт вопросы к тому, что видно на экране, просит прогноз перед каждым запуском и подсказывает по лестнице из трёх ступеней. Кнопка «?» — следующая ступень подсказки. Обновление страницы прогресс не стирает. Для следующей пары на заставке есть кнопка «Новая смена».</blockquote>

<h2>Цели: что к концу урока делает каждый ребёнок</h2>
<ol>
<li>Своими словами описывает цепочки распознавания и синтеза речи.</li>
<li>Знает, какой блок за какую ошибку отвечает, и настраивает пульт под конкретную фразу.</li>
<li>Видит, как обе части собираются в голосового чат-бота.</li>
<li>Отличает «машина слушает» (звук → текст) от «машина говорит» (текст → звук).</li>
<li>Понимает, кто в речевых технологиях за что отвечает: инженер, лингвист, звукорежиссёр, дизайнер диалогов.</li>
</ol>
<p>Конспекты в тетради оформляются графически, на языке ГРАФ (ДРАКОН-ГРАФ): на тетрадных точках игра показывает готовый образец, в финале пара собирает схему сама.</p>

<h2>A. Канва урока по минутам</h2>
<table>
<thead><tr><th>Мин</th><th>Экран</th><th>Что делает пара</th><th>Когда говорит Светляк</th></tr></thead>
<tbody>
<tr><td>0–4</td><td>1. Смена началась</td><td>Читают сюжет, вписывают имена. Учатся на пробной фразе: выключают и включают микрофон, крутят ручку, жмут «Запуск».</td><td>Ведёт по шагам: каждое новое задание — одна короткая фраза.</td></tr>
<tr><td>4–8</td><td>2. Разбор машины</td><td>Фраза № 1 (чистая). Блоки загораются по очереди, в окошке каждого — его результат. Отвечают на 4 вопроса. Опыт: выключают «Словарь», дают прогноз, запускают, находят место поломки, включают обратно.</td><td>Вопрос к загоревшемуся блоку; после ошибки — сужение к окошку, после второй — сравнение из жизни.</td></tr>
<tr><td>8–12</td><td>3. Испытания слуха</td><td>Фраза № 2 под шумом вентиляции: уверенность 60–80 %. Находят шумодав, включают, ставят ручку на середину. Пейджер открыт.</td><td>Перед каждым запуском — прогноз. После 1 неудачи — подсказка 2, после 2 — подсказка 3, после 3 — предложение вернуть пульт.</td></tr>
<tr><td>12–16</td><td>3. Испытания слуха</td><td>Фраза № 3: машина колеблется «КОТ? КОД?». Чинят ручкой «Угадывание по смыслу». По желанию — звонок специалисту.</td><td>Лестница по образцу «КОТ и КОД»; медаль за чистую настройку.</td></tr>
<tr><td>16–19</td><td>4. Тетрадь № 1</td><td>Перерисовывают образец «Как машина слушает?». Каждый дописывает: «Красный флаг ставлю на …, потому что …». Оба отмечают «записал».</td><td>Одна реплика-напоминание.</td></tr>
<tr><td>19–28</td><td>5. Голос машины</td><td>Собирают ответ жителю из готовых частей по правилу «приветствие → суть → уточнение». Ставят ударение «замо́к». Настраивают темп и высоту, слушают, отправляют. Пейджер открыт.</td><td>Прогноз перед отправкой; лестница по первой найденной ошибке: части, смысл, ударение, голос.</td></tr>
<tr><td>28–30</td><td>6. Тетрадь № 2</td><td>Перерисовывают «Как машина говорит?» под первой схемой, сравнивают стрелки, дописывают главное отличие.</td><td>Одна реплика-напоминание.</td></tr>
<tr><td>30–33</td><td>7. Живой разговор</td><td>Зовут трёх жителей: станция слушает их пультом и говорит их голосом. У третьего жителя выбирают «духи́».</td><td>Реакция на каждый разговор.</td></tr>
<tr><td>33–36</td><td>7. Свой конспект</td><td>Сами заполняют таблицу «Распознавание / Синтез», программа сразу рисует схему. Переписывают её в тетрадь.</td><td>Лестница при ошибке; на третьей ступени неверные клетки подсвечиваются.</td></tr>
<tr><td>36–39</td><td>7. Отчёт специалистам</td><td>Четыре вопроса по очереди (имя над вопросом): кого позвать и зачем. Читают ответы специалистов, могут исправить.</td><td>—</td></tr>
<tr><td>39–40</td><td>7. Концовка</td><td>Одна из трёх концовок. Каждый сам дописывает в тетради пять фраз личного вывода (в спешке — три), напарнику не подсказывает, потом сверяются.</td><td>Напоминает: вывод — у каждого свой.</td></tr>
</tbody>
</table>

<h3>Развилки по часам смены</h3>
<p>Часы идут с нажатия «Принять смену» и видны в шапке игры. Запись в тетрадь остаётся у всех.</p>
<table>
<thead><tr><th>Когда</th><th>Что происходит</th></tr></thead>
<tbody>
<tr><td>Финал раньше 35-й минуты</td><td><b>Сверхурочный вызов «Эхо-2»</b> — три задания на тех же механиках: две поломки сразу (перегруз микрофона и шум), слишком смелое угадывание (машина «додумывает» слово), ответ про за́мок-музей с другим ударением и сбитым голосом. После вызова — задание в тетрадь: своя схема чат-бота. Личный вывод — сразу после концовки, до вызова.</td></tr>
<tr><td>29-я минута, пара ещё не дошла до тетради № 2</td><td><b>«Мастер на связи»</b>: подсказки сразу третьей ступени; после неудачи мастер по рации чинит сломанный блок; голос в «Голосе машины» настроен за пару; тетради — короче (цепочка без подписей-фраз, красный флаг — устно; во второй — одна строка); в своём конспекте две строки уже вписаны; отчёт — по одному вопросу на каждого; личный вывод — три фразы.</td></tr>
<tr><td>36-я минута, пара ещё не в финале</td><td><b>«Мастер вернулся»</b>: пульт и голос докручены, пара сразу зовёт жителей. Пропущенные схемы показываются в концовке — переписать после урока.</td></tr>
</tbody>
</table>

<h2>B. Полный контент игры</h2>
<p class="k">Этот раздел собирается из того же файла, что и игра (<code>tekst.js</code>), поэтому всегда совпадает с ней.</p>
<div id="content"></div>

<h2>D. Самопроверка</h2>
<table>
<thead><tr><th>Что проверяли</th><th>Итог</th></tr></thead>
<tbody>
<tr><td>Запуск с сайта и из сетевой папки</td><td><span class="ok">да</span> — нет внешних ссылок; библиотека конспектов и шрифты лежат на сайте в <code>lib/</code>. Для сетевой папки копировать сайт целиком.</td></tr>
<tr><td>Все 7 экранов</td><td><span class="ok">да</span> — пройдены от начала до конца в браузере, ошибок нет.</td></tr>
<tr><td>Каждый экран читается за 15–20 секунд</td><td><span class="ok">да</span> — сверху одна строка задания, справа одна реплика Светляка.</td></tr>
<tr><td>Реплики в лимите</td><td><span class="ok">да</span> — помощник до 106 знаков (2 строки), специалист до 115 знаков (3 строки); проверено скриптом.</td></tr>
<tr><td>Лестница подсказок и авто-подсказка после 2 неудач</td><td><span class="ok">да</span> — после 1-й неудачи ступень 2, после 2-й — ступень 3, после 3-й — предложение вернуть пульт; «?» — следующая ступень в любой момент.</td></tr>
<tr><td>Прогноз перед каждым запуском</td><td><span class="ok">да</span> — запуск после любого ответа, затем реакция «угадал / почему так».</td></tr>
<tr><td>Прогресс сохраняется</td><td><span class="ok">да</span> — в браузере компьютера; перезагрузка возвращает на тот же экран.</td></tr>
<tr><td>Без русского голоса</td><td><span class="ok">да</span> — ответ машины печатается текстом с писком: скорость печати — от темпа, высота писка — от высоты. В шапке надпись «Голос: текстом».</td></tr>
<tr><td>Ударение в голосе браузера</td><td><span class="no">проверить на школьном компьютере</span> — ударение передаётся знаком «´»; часть голосов его не слушает. Выбор ударения игра проверяет сама, так что пройти урок можно в любом случае.</td></tr>
<tr><td>Верный ответ не угадывается по месту</td><td><span class="ok">да</span> — варианты в вопросах, прогнозах и отчёте перемешаны.</td></tr>
<tr><td>Пульт по очереди</td><td><span class="ok">да</span> — за пультом и штурман меняются: обучение и фраза № 2 — первый стажёр, разбор и фраза № 3 — второй, голос и конспект — первый, разговор с жителями — второй.</td></tr>
<tr><td>Развилки по времени</td><td><span class="ok">да</span> — проверены: «мастер на связи» на 29-й минуте, «мастер вернулся» на 36-й, сверхурочный вызов при финале на 26-й минуте.</td></tr>
<tr><td>Конспекты ДРАКОН-ГРАФ</td><td><span class="ok">да</span> — три схемы проверены библиотекой, подсказок об ошибках нет.</td></tr>
</tbody>
</table>
</main>

<script src="tekst.js"></script>
<script src="../../lib/drakon-graf/drakon-graf.min.js"></script>
<script src="../../lib/drakon-graf/konspekt.js"></script>
<script>
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ul = a => '<ul>' + a.map(x => '<li>' + x + '</li>').join('') + '</ul>';
const SP = Object.fromEntries(T.specialists.map(s => [s.id, s]));
let h = '';
h += '<h3>Сюжет (экран 1)</h3>' + ul(T.story.map(esc)) + '<p>' + esc(T.namesAsk) + '</p>';
h += '<h3>Обучение пульту</h3>' + ul(T.training.map(t => esc(t.say))) + '<p>' + esc(T.trainingDone) + '</p>';
h += '<h3>Фразы жителей</h3><table><tr><th>Где</th><th>Фраза</th><th>Что ломает</th></tr>' +
  Object.entries(T.phrases).map(([k,p]) => `<tr><td>${esc(p.label)}</td><td>${esc(p.words.map(w=>w.w).join(' '))}</td><td>${p.noise?'шум':''}${p.words.some(w=>w.twin)?'слова-близнецы: '+p.words.find(w=>w.twin).twin.join(' / '):''}${k==='F3'?'омограф в ответе: ду́хи / духи́':''}</td></tr>`).join('') + '</table>';
h += '<p>Пульт распознавания: ' + T.blocks.map(b => `<b>${esc(b.name)}</b> → ${esc(b.stage)} (ручка «${esc(b.knob)}»)`).join('; ') + '.</p>';
h += '<p class="k">Уверенность: чистая запись — 96–97 %; шум без шумодава — 60–80 %; слова-близнецы без угадывания — около 87 %. Слишком сильный шумодав «съедает» тихие звуки, слишком смелое угадывание «додумывает» слова.</p>';
h += '<h3>Разбор машины (экран 2): вопросы и лестница</h3><table><tr><th>Ступень 1 (варианты, верный — первый)</th><th>Ступень 2</th><th>Ступень 3</th></tr>' +
  T.parse.map(p => `<tr><td>${esc(p.q)}<br><span class="k">${p.opts.map(esc).join(' · ')}</span></td><td>${esc(p.l2)}</td><td>${esc(p.l3)}</td></tr>`).join('') +
  `<tr><td>${esc(T.experiment.ask)}<br>${esc(T.experiment.after)}<br><span class="k">${T.experiment.afterOpts.map(esc).join(' · ')}</span></td><td>${esc(T.experiment.l2)}</td><td>${esc(T.experiment.l3)}</td></tr></table><p>${esc(T.experiment.done)}</p>`;
h += '<h3>Испытания (экран 3): лестница подсказок</h3><table><tr><th>Фраза</th><th>Ступень 1</th><th>Ступень 2</th><th>Ступень 3</th><th>Успех</th></tr>' +
  Object.entries(T.trials).map(([k,t]) => `<tr><td>${esc(t.intro)}</td><td>${esc(t.l1)}</td><td>${esc(t.l2)}</td><td>${esc(t.l3)}</td><td>${esc(t.win)}</td></tr>`).join('') + '</table>';
h += `<p>Прогноз: «${esc(T.predict.q)}» (${T.predict.opts.map(esc).join(' / ')}). После запуска: «${esc(T.predictRight)}» или «${esc(T.predictWrong)}»</p>`;
h += `<p>Откат после трёх неудач: «${esc(T.rollback)}»</p>`;
h += '<p>Капризы машины: ' + [...T.reactions.up, ...T.reactions.down].map(r => '«' + esc(r) + '»').join(', ') + '.</p>';
h += '<h3>Специалисты на пейджере</h3><table><tr><th>Кто</th><th>Характер</th><th>Речевые приметы</th></tr>' +
  T.specialists.map(s => `<tr><td><b>${esc(s.name)}</b><br><span class="k">${esc(s.who)}</span></td><td>${esc(s.look)}</td><td>${s.markers.map(esc).join(', ')}</td></tr>`).join('') + '</table>';
h += `<p>Ответ стоит ${T.cost} битрейтов, уточнение бесплатно. Специалист печатает со скоростью взрослого (~${String(T.typingSpeed).replace('.',',')} знака в секунду), в это время у пары разминка — нажать на знакомый блок. Не тот специалист: «${esc(T.redirect.replace('{who}','…'))}»</p>`;
['recog','synth'].forEach(c => {
  h += `<h3>Гипотезы ребёнка — ${c==='recog'?'распознавание':'голос машины'}</h3><table><tr><th>Гипотеза</th><th>Кому</th><th>Ответ</th><th>Уточнение</th></tr>` +
    T.hyps[c].map(x => `<tr><td>${esc(x.text)}</td><td>${esc(SP[x.to].name)}</td><td>${esc(x.a)}</td><td>${esc(x.more)}</td></tr>`).join('') + '</table>';
});
const sy = T.synth;
h += '<h3>Голос машины (экран 5)</h3><p>Житель: «' + esc(sy.request) + '»</p><p><b>' + esc(sy.rule) + '</b></p><p>' + esc(sy.honest) + '</p>';
h += '<table><tr><th>Часть</th><th>Тип</th><th>Подходит?</th></tr>' + sy.chips.map(c => `<tr><td>${esc(c.text.replace('{ZAMOK}','замо́к / за́мок'))}</td><td>${esc(c.type)}</td><td>${c.fit?'да':'нет'}</td></tr>`).join('') + '</table>';
h += '<p>Верный ответ: «Здравствуйте! (или «Добрый вечер!») Мастер починит замо́к сегодня до шести. Позвать мастера прямо сейчас?», темп 0,8–1,25, высота 0,8–1,3. В начале голос стоит на 1,8 / 1,7 — тараторит и пищит.</p>';
h += '<table><tr><th>Ошибка</th><th>Ступень 2</th><th>Ступень 3</th></tr>' + Object.keys(sy.l2).map(k => `<tr><td>${esc({order:'порядок частей',fit:'часть не по делу',stress:'ударение',voice:'голос',empty:'полка не заполнена'}[k])}</td><td>${esc(sy.l2[k])}</td><td>${esc(sy.l3[k])}</td></tr>`).join('') + `</table><p>Ступень 1: «${esc(sy.l1)}» Успех: «${esc(sy.win)}»</p>`;
h += '<h3>Тетради: образцы ДРАКОН-ГРАФ</h3>';
[T.note1, T.note2].forEach((n,i) => { h += `<p><b>${esc(n.title)}</b></p><div class="kon" id="kon${i}"></div><ol>${n.steps.map(s=>'<li>'+esc(s)+'</li>').join('')}</ol>`; });
h += '<p>Как читать схему: ' + T.legend.map(([a,b]) => `<b>${esc(a)}</b> — ${esc(b)}`).join('; ') + '.</p>';
const F = T.final;
h += '<h3>Финал (экран 7)</h3><p>' + esc(F.intro) + '</p><table><tr><th>Житель</th><th>Ответ станции</th></tr>' +
  ['F1','F2','F3'].map(k => `<tr><td>${esc(T.phrases[k].words.map(w=>w.w).join(' '))}</td><td>${esc(F.answers[k].replace('{DUHI}','Духи́'))}</td></tr>`).join('') +
  `<tr><td>если не расслышала</td><td>${esc(F.answers.fail)}</td></tr></table><p>${esc(F.duhiAsk)} Неверно: «${esc(F.duhiWrong)}»</p>`;
h += '<p><b>Свой конспект</b> — ' + esc(F.tableIntro) + '</p><div class="kon" id="kon2"></div>';
h += `<p>Лестница: «${esc(F.l1)}» → «${esc(F.l2.replace('{row}','…'))}» → «${esc(F.l3)}»</p>`;
h += '<h3>Отчёт специалистам</h3><p>' + esc(T.check.intro) + '</p><table><tr><th>Вопрос</th><th>Кого</th><th>Зачем (верный — первый)</th><th>Обратная связь</th></tr>' +
  T.check.qs.map(q => `<tr><td>${esc(q.q)}</td><td>${esc(SP[q.to].name)}</td><td>${q.why.map(esc).join(' · ')}</td><td><span class="ok">${esc(q.good)}</span><br>${esc(q.bad)}</td></tr>`).join('') + '</table>';
h += '<h3>Три концовки</h3><table><tr><th>Жителей поняли</th><th>Концовка</th></tr>' + T.endings.map(e => `<tr><td>${e.min===3?'3 из 3':e.min===2?'2 из 3':'0–1'}</td><td><b>${esc(e.title)}</b><br>${esc(e.text)}</td></tr>`).join('') + '</table>';
h += '<h3>Мастер на связи / мастер вернулся</h3><p>«' + esc(T.rush.text) + '»</p>' + ul([T.rush.trialHelp.replace('{block}','…'), T.rush.synthHelp, ...T.rush.note1, ...T.rush.note2, T.rush.table, T.rush.check].map(esc)) + '<p>«' + esc(T.late.text) + '» ' + esc(T.late.note) + '</p>';
h += '<h3>Сверхурочный вызов «Эхо-2»</h3><p>' + esc(T.bonus.call.text) + '</p><table><tr><th>Вызов</th><th>Ступень 1</th><th>Ступень 2</th><th>Ступень 3</th></tr>' +
  ['B1','B2'].map((k,i) => `<tr><td><b>${esc(T.bonus.names[i])}</b><br>${esc(T.phrases[k].words.map(w=>w.w).join(' '))}<br><span class="k">${esc(T.trials[k].intro)}</span></td><td>${esc(T.trials[k].l1)}</td><td>${esc(T.trials[k].l2)}</td><td>${esc(T.trials[k].l3)}</td></tr>`).join('') +
  `<tr><td><b>${esc(T.bonus.names[2])}</b><br>${esc(T.bonusSynth.request)}</td><td colspan="3">Верно: «Здравствуйте! За́мок на холме открыт с десяти до восемнадцати. Рассказать, как туда доехать?» Голос в начале 0,6 / 0,6 — медленно и низко. ${esc(T.bonusSynth.win)}</td></tr></table>` +
  '<p><b>' + esc(T.bonus.done.title) + '</b> ' + esc(T.bonus.done.text) + ' ' + esc(T.ending.wait) + ' ' + esc(T.ending.wait2) + '</p>';
h += '<h3>Личный вывод в тетрадь</h3><p>' + esc(T.oral.intro) + '</p><ol>' + T.oral.frames.map(f => '<li>' + esc(f) + '</li>').join('') + '</ol>';
h += '<p class="k">Ожидаемые ответы: звук → текст; текст → звук; шум и слова-близнецы; ударения и омографы; распознавание и синтез (слушает и говорит).</p>';
document.getElementById('content').innerHTML = h;
const tbl = `тема: Слушает или говорит?
связка: Распознавание | Синтез
${F.rows.map(r => `${r.q} -> ${r.a} | ${r.b}`).join('\n')}`;
try {
  Konspekt.draw(document.getElementById('kon0'), T.note1.konspekt, { class:5, width:760 });
  Konspekt.draw(document.getElementById('kon1'), T.note2.konspekt, { class:5, width:760 });
  Konspekt.draw(document.getElementById('kon2'), tbl, { class:5, width:760 });
} catch(e) {}
</script>
</body>
</html>

===== КОНЕЦ ФАЙЛА: 5-klass/ekho-uzel/kanva.html =====

===== ФАЙЛ: 5-klass/ekho-uzel/vkleyka.html =====
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Эхо-Узел: лист для вклейки</title>
<style>
  *{box-sizing:border-box}
  body{margin:0;background:#eee;font:15px/1.4 "Segoe UI",Arial,sans-serif;color:#222}
  .bar{padding:10px 16px;background:#1f2329;color:#eef1f4;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
  .bar button{font:inherit;font-weight:700;background:#f2a93b;border:0;border-radius:16px;padding:6px 14px;cursor:pointer}
  .sheet{width:210mm;min-height:297mm;margin:12px auto;background:#fff;padding:12mm 20mm}
  .cut{border-top:1.5px dashed #888;margin:6mm 0 4mm;position:relative}
  .cut span{position:absolute;top:-9px;left:0;background:#fff;padding-right:6px;font-size:12px;color:#666}
  .cap{font-size:13px;color:#555;margin:0 0 2mm}
  .kon svg{width:100%;height:auto;display:block}
  @media print{ body{background:#fff} .bar{display:none} .sheet{margin:0;padding:10mm 20mm;width:auto;min-height:auto} @page{size:A4;margin:0} }
</style>
</head>
<body>
<div class="bar"><b>Лист для вклейки в тетрадь</b><span>Одна копия — один ученик. Вырезать по пунктиру.</span><button onclick="window.print()">Печать</button></div>
<div class="sheet">
  <div class="cut"><span>✂</span></div>
  <p class="cap">Отчёт № 1 · как машина слушает</p><div class="kon" id="k1"></div>
  <div class="cut"><span>✂</span></div>
  <p class="cap">Отчёт № 2 · как машина говорит</p><div class="kon" id="k2"></div>
  <div class="cut"><span>✂</span></div>
  <p class="cap">Итог смены · слушает или говорит</p><div class="kon" id="k3"></div>
  <div class="cut"><span>✂</span></div>
</div>
<script src="tekst.js"></script>
<script src="../../lib/drakon-graf/drakon-graf.min.js"></script>
<script src="../../lib/drakon-graf/konspekt.js"></script>
<script>
const F = T.final;
const tbl = `тема: Слушает или говорит?
связка: Распознавание | Синтез
${F.rows.map(r => `${r.q} -> ${r.a} | ${r.b}`).join('\n')}`;
[['k1', T.note1.konspekt], ['k2', T.note2.konspekt], ['k3', tbl]].forEach(([id, t]) =>
  Konspekt.draw(document.getElementById(id), t, { class:5, width:640, theme:'bw' }));
</script>
</body>
</html>

===== КОНЕЦ ФАЙЛА: 5-klass/ekho-uzel/vkleyka.html =====

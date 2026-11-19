// Проверка двоичной логики на Форте (WAForth) и Прологе (swipl-wasm) — стенды drakon-graf, только чтение
// Запуск: node proverka-dvoich.cjs <drakon-graf/site/experiments/forth/lib/index.js> <drakon-graf/site/experiments/prolog/lib>
// Примеры — primery-dvoich.json (собирает dvoich.py).
const fs = require('fs');
const path = require('path');

// chitat: файл рядом с проверкой
function chitat(imya) {
  return fs.readFileSync(path.join(__dirname, imya), 'utf-8');
}

// vyvod: прогнать строку на загруженном Форте, вывод без «ok»
function vyvod(f, bajty, stroka) {
  bajty.length = 0;
  f.interpret(stroka);
  return new TextDecoder('utf-8').decode(new Uint8Array(bajty)).replace(/\s*ok\s*$/, '').trim();
}

// schet: прогнать пары [вход, ждём] через проверяющее слово; печатать только ошибки
function schet(sluchai, proverka) {
  let proshli = 0;
  for (const [vhod, zhdem] of sluchai) {
    const vyshlo = proverka(vhod);
    proshli += vyshlo === zhdem ? 1 : 0;
    if (vyshlo !== zhdem) console.log('НЕТ ' + vhod + ' → ' + vyshlo + ' (ждали ' + zhdem + ')');
  }
  return proshli;
}

// fort: загрузить слова и законы, проверить примеры и пустой стек
function fort(lib, primery) {
  const WAForth = require(path.resolve(lib)).default;
  const f = new WAForth();
  const bajty = [];
  f.onEmit = (c) => bajty.push(c);
  const sluchai = primery.concat([['DEPTH .', '0']]);
  return f.load().then(() => vyvod(f, bajty, chitat('dvoich-slova.fs') + '\n' + chitat('dvoich-zakony.fs')))
    .then(() => [schet(sluchai, (s) => vyvod(f, bajty, s)), sluchai.length]);
}

// podnyat: загрузить swipl-wasm под Node
function podnyat(lib) {
  const kod = fs.readFileSync(path.join(lib, 'swipl-web.js'), 'utf8') + ';module.exports = SWIPL;';
  const modul = { exports: {} };
  new Function('module', 'exports', 'require', '__dirname', kod)(modul, modul.exports, require, lib);
  return modul.exports({ arguments: ['-q'], locateFile: (imya) => path.join(lib, imya) });
}

// zagruzit: положить правила и данные в файловую систему Пролога и загрузить
function zagruzit(swipl) {
  for (const imya of ['dvoich-pravila.pl', 'dvoich-dannye.pl']) {
    swipl.FS.writeFile('/' + imya, chitat(imya));
    swipl.prolog.call("consult('/" + imya + "')");
  }
  return swipl;
}

// zaprosy: проверить запросы — выводится или нет, как ждали
function zaprosy(swipl, primery) {
  const proshli = schet(primery, (z) => Boolean(swipl.prolog.query(z).once().success));
  return [proshli, primery.length];
}

// prolog: поднять Пролог, загрузить, проверить
function prolog(lib, primery) {
  return podnyat(path.resolve(lib)).then(zagruzit).then((swipl) => zaprosy(swipl, primery));
}

// itog: напечатать и выставить код выхода
function itog(imya, [proshli, vsego]) {
  console.log(imya + ': ' + proshli + ' из ' + vsego);
  if (proshli !== vsego) process.exitCode = 1;
  return proshli;
}

// glavnoe: Форт, потом Пролог — по очереди
function glavnoe() {
  const dannye = JSON.parse(chitat('primery-dvoich.json'));
  return fort(process.argv[2], dannye.fort).then((r) => itog('Форт', r))
    .then(() => prolog(process.argv[3], dannye.prolog)).then((r) => itog('Пролог', r));
}

glavnoe();

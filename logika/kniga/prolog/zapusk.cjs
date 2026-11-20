// zapusk.cjs — проверка Пролог-слов части 2 на SWI-Prolog (swipl-wasm из drakon-graf, только чтение)
// Запуск: node logika/kniga/prolog/zapusk.cjs <путь к drakon-graf/site/experiments/prolog/lib>
// Файлы грузятся снизу вверх: каждый следующий пользуется словами предыдущих.
const fs = require('fs');
const path = require('path');

// PORYADOK: от простого к сложному
const PORYADOK = ['bazis.pl', 'chast2-A.pl', 'chast2-B.pl', 'chast2-V.pl', 'chast2-G.pl', 'chast2-D.pl', 'chast2-E.pl'];

// podnyat: загрузить swipl-wasm под Node
function podnyat(lib) {
  const kod = fs.readFileSync(path.join(lib, 'swipl-web.js'), 'utf8') + ';module.exports = SWIPL;';
  const modul = { exports: {} };
  new Function('module', 'exports', 'require', '__dirname', kod)(modul, modul.exports, require, lib);
  return modul.exports({ arguments: ['-q'], locateFile: (f) => path.join(lib, f) });
}

// zagruzit: положить файлы, какие есть, и загрузить по порядку
function zagruzit(swipl) {
  for (const f of PORYADOK.filter((f) => fs.existsSync(path.join(__dirname, f)))) {
    swipl.FS.writeFile('/' + f, fs.readFileSync(path.join(__dirname, f), 'utf8'));
    if (!swipl.prolog.query("consult('/" + f + "')").once().success) console.log('НЕ ЗАГРУЗИЛСЯ ' + f);
  }
  return swipl;
}

// proverit: по каждому шагу - всего и ошибки
function proverit(swipl) {
  const shagi = swipl.prolog.query('шаги(Ш)').once().Ш;
  let vsego = 0, plohih = 0;
  for (const sh of shagi) {
    const r = swipl.prolog.query('итог(' + "'" + sh + "'" + ', Н, П)').once();
    vsego += r.Н; plohih += r.П.length;
    console.log(sh + ': ' + (r.Н - r.П.length) + ' из ' + r.Н + r.П.map((p) => '\n  НЕТ ' + p).join(''));
  }
  console.log('Пролог, часть 2: ' + (vsego - plohih) + ' из ' + vsego);
  process.exitCode = plohih === 0 ? 0 : 1;
  return plohih;
}

podnyat(path.resolve(process.argv[2])).then(zagruzit).then(proverit);

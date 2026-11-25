// prolog-vektory.cjs — таблицы слов эталона на swipl-wasm из drakon-graf (Марьям, 25.11.2026; только чтение)
// Запуск (его делает proverka.py): node prolog-vektory.cjs <lib> <папка эталона> '<файлы JSON>' '<цели JSON>'
// Вывод: JSON {слово: таблица}; файл не загрузился или цель не вывелась — таблицы слова нет.
const fs = require('fs');
const path = require('path');

// podnyat: загрузить swipl-wasm под Node (как logika/kniga/prolog/zapusk.cjs)
function podnyat(lib) {
  const kod = fs.readFileSync(path.join(lib, 'swipl-web.js'), 'utf8') + ';module.exports = SWIPL;';
  const modul = { exports: {} };
  new Function('module', 'exports', 'require', '__dirname', kod)(modul, modul.exports, require, lib);
  return modul.exports({ arguments: ['-q'], locateFile: (f) => path.join(lib, f) });
}

// zagruzit: положить файлы эталона и загрузить по порядку
function zagruzit(swipl, papka, fajly) {
  for (const f of fajly) {
    swipl.FS.writeFile('/' + f, fs.readFileSync(path.join(papka, f), 'utf8'));
    swipl.prolog.query("consult('/" + f + "')").once();
  }
  return swipl;
}

// tablicy: по каждой цели [вектор, слово] — таблица слова
function tablicy(swipl, celi) {
  const otvet = {};
  for (const [v, s] of celi) {
    const r = swipl.prolog.query(v + "('" + s + "', T)").once();
    if (r && r.T) otvet[s] = r.T;
  }
  return otvet;
}

const [lib, papka, fajly, celi] = process.argv.slice(2);
podnyat(path.resolve(lib)).then((swipl) => {
  zagruzit(swipl, papka, JSON.parse(fajly));
  process.stdout.write(JSON.stringify(tablicy(swipl, JSON.parse(celi))));
});

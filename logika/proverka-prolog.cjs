// Проверка правил och-pravila.pl на SWI-Prolog (swipl-wasm из drakon-graf, только чтение)
// Запуск: node proverka-prolog.cjs <путь к drakon-graf/site/experiments/prolog/lib>
// Общие примеры — primery.json (перебор тритов по эталону proverka.py); особые — ниже.
const fs = require('fs');
const path = require('path');

// OSOBYE: запрос → должен выводиться (true) или нет (false)
const OSOBYE = [
  ['трит(0, не_знаю)', true], ['трит(2, _)', false],
  ['срабатывает(отсутствует, -1)', true], ['срабатывает(отсутствует, 1)', false],
  ['ответ(1, делаю)', true], ['ответ(0, ищу)', true], ['ответ(-1, не_делаю)', true], ['ответ(0, делаю)', false],
  ['все_проверены(урок_23, 1)', true], ['все_проверены(урок_24, 0)', true], ['все_проверены(урок_24, 1)', false],
  ['все_проверены(У, 0), У == урок_24', true],
  ['ответ_ученику(0, пока_не_знаю_проверю)', true], ['ответ_ученику(0, да)', false], ['ответ_ученику(-1, нет)', true],
];

// iz_primera: случай из primery.json → запрос «ровно этот ответ и только он»
function iz_primera(s) {
  const vhod = s.vhod.join(', ');
  return ['findall(T, ' + s.prolog + '(' + vhod + ', T), [' + s.zhdem + '])', true];
}

// podnyat: загрузить swipl-wasm под Node
function podnyat(lib) {
  const kod = fs.readFileSync(path.join(lib, 'swipl-web.js'), 'utf8') + ';module.exports = SWIPL;';
  const modul = { exports: {} };
  new Function('module', 'exports', 'require', '__dirname', kod)(modul, modul.exports, require, lib);
  return modul.exports({ arguments: ['-q'], locateFile: (f) => path.join(lib, f) });
}

// zagruzit: положить правила в файловую систему Пролога и загрузить
function zagruzit(swipl) {
  swipl.FS.writeFile('/och-pravila.pl', fs.readFileSync(path.join(__dirname, 'och-pravila.pl'), 'utf8'));
  swipl.prolog.call("consult('/och-pravila.pl')");
  return swipl;
}

// proverit: каждый запрос — выводится или нет, как ждали; печатать только ошибки
function proverit(swipl, sluchai) {
  let proshli = 0;
  for (const [zapros, zhdem] of sluchai) {
    const vyshlo = Boolean(swipl.prolog.query(zapros).once().success);
    proshli += vyshlo === zhdem ? 1 : 0;
    if (vyshlo !== zhdem) console.log('НЕТ ' + zapros + ' → ' + (vyshlo ? 'выводится' : 'нет'));
  }
  return proshli;
}

// itog: напечатать итог и выставить код выхода
function itog(proshli, vsego) {
  console.log('Пролог: ' + proshli + ' из ' + vsego);
  process.exitCode = proshli === vsego ? 0 : 1;
  return proshli;
}

// glavnoe: поднять Пролог, загрузить правила, проверить
function glavnoe() {
  const primery = JSON.parse(fs.readFileSync(path.join(__dirname, 'primery.json'), 'utf-8'));
  const sluchai = primery.map(iz_primera).concat(OSOBYE);
  return podnyat(path.resolve(process.argv[2])).then(zagruzit)
    .then((swipl) => proverit(swipl, sluchai)).then((p) => itog(p, sluchai.length));
}

glavnoe();

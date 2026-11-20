// zapusk.cjs — проверка Форт-слов части 2 на WAForth (из drakon-graf, только чтение)
// Запуск: node logika/kniga/fort/zapusk.cjs <путь к drakon-graf/site/experiments/forth/lib/index.js>
// Случаи - sluchai.txt: «шаг | строка Форта | ожидаемый вывод».
const fs = require('fs');
const path = require('path');

// vyvod: прогнать строку на загруженном Форте, вывод без «ok»
function vyvod(f, bajty, stroka) {
  bajty.length = 0;
  try { f.interpret(stroka); } catch (e) { return 'ОШИБКА ' + e; }
  return new TextDecoder('utf-8').decode(new Uint8Array(bajty)).replace(/\s*ok\s*$/, '').replace(/\s+/g, ' ').trim();
}

// sluchai: строки файла → [шаг, строка, ждём]
function sluchai() {
  return fs.readFileSync(path.join(__dirname, 'sluchai.txt'), 'utf-8').split('\n')
    .filter((s) => s.trim() && !s.startsWith('#')).map((s) => s.split('|').map((c) => c.trim()));
}

// proverit: по шагам - сколько прошло, ошибки печатать
function proverit(f, bajty) {
  const itog = {};
  for (const [shag, stroka, zhdem] of sluchai()) {
    const vyshlo = vyvod(f, bajty, stroka);
    itog[shag] = itog[shag] || [0, 0];
    itog[shag][1] += 1;
    if (vyshlo === zhdem) itog[shag][0] += 1;
    else console.log('НЕТ ' + shag + ': ' + stroka + ' → ' + vyshlo + ' (ждали ' + zhdem + ')');
  }
  let p = 0, v = 0;
  for (const [shag, [da, vse]] of Object.entries(itog)) { console.log(shag + ': ' + da + ' из ' + vse); p += da; v += vse; }
  console.log('Форт, часть 2: ' + p + ' из ' + v);
  process.exitCode = p === v ? 0 : 1;
}

const WAForth = require(path.resolve(process.argv[2])).default;
const f = new WAForth();
const bajty = [];
f.onEmit = (c) => bajty.push(c);
f.load().then(() => {
  const z = vyvod(f, bajty, fs.readFileSync(path.join(__dirname, 'chast2.fs'), 'utf-8'));
  if (/undefined|error|not supported/i.test(z)) console.log('загрузка: ' + z);
  proverit(f, bajty);
});

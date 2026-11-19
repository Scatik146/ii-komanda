// Проверка слов och-slova.fs на настоящем Форте (WAForth из drakon-graf, только чтение)
// Запуск: node proverka-fort.cjs <путь к drakon-graf/site/experiments/forth/lib/index.js>
// Общие примеры — primery.json (перебор тритов по эталону proverka.py); особые — ниже.
const fs = require('fs');
const path = require('path');

// OSOBYE: то, что перебором тритов не задать — строка Форта → ожидаемый вывод
const OSOBYE = [
  ['ДА . НЕЗНАЮ . НЕТ .', '1 0 -1'],
  ['ОТСУТСТВУЕТ срабатывает .', '-1'], ['0 срабатывает .', '1'],
  ['1 ответ', 'делаю'], ['0 ответ', 'ищу'], ['-1 ответ', 'не делаю'],
  ['DEPTH .', '0'],                       // последним: ни одно слово не оставило мусора на стеке
];

// iz_primera: случай из primery.json → строка Форта и ожидаемый вывод
function iz_primera(s) {
  return [s.vhod.join(' ') + ' ' + s.fort + ' .', String(s.zhdem)];
}

// vyvod: прогнать строку на уже загруженном Форте, вывод без «ok»
function vyvod(f, bajty, stroka) {
  bajty.length = 0;
  f.interpret(stroka);
  return new TextDecoder('utf-8').decode(new Uint8Array(bajty)).replace(/\s*ok\s*$/, '').trim();
}

// proverit: все случаи на одном Форте; печатать только ошибки
function proverit(f, bajty, sluchai) {
  let proshli = 0;
  for (const [stroka, zhdem] of sluchai) {
    const vyshlo = vyvod(f, bajty, stroka);
    proshli += vyshlo === zhdem ? 1 : 0;
    if (vyshlo !== zhdem) console.log('НЕТ ' + stroka + ' → ' + vyshlo + ' (ждали ' + zhdem + ')');
  }
  return proshli;
}

// zapustit: загрузить Форт и слова, прогнать все случаи
function zapustit(WAForth, slova, sluchai) {
  const f = new WAForth();
  const bajty = [];
  f.onEmit = (c) => bajty.push(c);
  return f.load().then(() => vyvod(f, bajty, slova)).then(() => proverit(f, bajty, sluchai));
}

// itog: напечатать итог и выставить код выхода
function itog(proshli, vsego) {
  console.log('Форт: ' + proshli + ' из ' + vsego);
  process.exitCode = proshli === vsego ? 0 : 1;
  return proshli;
}

// glavnoe: собрать случаи, проверить
function glavnoe() {
  const WAForth = require(path.resolve(process.argv[2])).default;
  const slova = fs.readFileSync(path.join(__dirname, 'och-slova.fs'), 'utf-8');
  const primery = JSON.parse(fs.readFileSync(path.join(__dirname, 'primery.json'), 'utf-8'));
  const sluchai = primery.map(iz_primera).concat(OSOBYE);
  return zapustit(WAForth, slova, sluchai).then((p) => itog(p, sluchai.length));
}

glavnoe();

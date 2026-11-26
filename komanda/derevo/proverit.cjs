// Дерево задач — запуск проверки на стенде swipl-wasm (drakon-graf site/experiments/prolog/lib).
// Вызов: node komanda/derevo/proverit.cjs <папка lib стенда> <файл фактов>
const fs = require('fs');
const path = require('path');

// загрузить: поднять SWI-Prolog из папки стенда
function загрузить(папка) {
  const старт = require(path.join(папка, 'swipl-web.js'));
  return старт({ arguments: ['-q'], locateFile: (f) => path.join(папка, f) });
}

// положить: скопировать файл в память движка
function положить(m, файл, имя) {
  m.FS.writeFile(имя, fs.readFileSync(файл, 'utf8'));
}

// список: все X, для которых верна цель
function список(m, цель) {
  const ответ = m.prolog.query(`findall(X, ${цель}(X), L)`).once();
  return ответ.L;
}

// проверить: три списка ошибок и итог; код выхода 0 — дерево верно
async function проверить(папка, факты) {
  const m = await загрузить(папка);
  положить(m, факты, '/derevo.pl');
  положить(m, path.join(__dirname, 'proverka.pl'), '/proverka.pl');
  m.prolog.query("consult('/derevo.pl'), consult('/proverka.pl')").once();
  const узлов = m.prolog.query('aggregate_all(count, узел(_,_,_), N)').once().N;
  const ошибки = ['нет_родителя', 'чужой_статус', 'в_цикле', 'чужая_опора'].map((ц) => [ц, список(m, ц)]);
  ошибки.forEach(([ц, l]) => console.log(`${ц}: ${l.length ? l.join(', ') : 'нет'}`));
  const верно = m.prolog.query('дерево_верно').once().success;
  console.log(`узлов: ${узлов}; дерево_верно: ${верно}`);
  process.exitCode = верно ? 0 : 1;
}

проверить(process.argv[2], process.argv[3]);

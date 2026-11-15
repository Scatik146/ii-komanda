// Данные: { knigi: [{id, nazvanie, avtor}], chitateli: [{id, imya}], vydachi: [{id, kniga, chitatel}] }
const POROG_MNOGO = 2;
// nazvaniya_odnoy_vydachi: названия книг, на которые указывает выдача
function nazvaniya_odnoy_vydachi(vydacha, knigi) {
  const nazvaniya = [];
  for (const kniga of knigi) {
    if (kniga.id == vydacha.kniga) nazvaniya.push(kniga.nazvanie);
  }
  return nazvaniya;
}
// nazvaniya_knig: названия книг по списку выдач, по алфавиту
function nazvaniya_knig(vydachi, knigi) {
  const nazvaniya = [];
  for (const vydacha of vydachi) {
    const chast = nazvaniya_odnoy_vydachi(vydacha, knigi);
    for (const nazvanie of chast) {
      nazvaniya.push(nazvanie);
    }
  }
  nazvaniya.sort();
  return nazvaniya;
}
// knigi_chitatelya: выдачи одного читателя
function knigi_chitatelya(chitatel, dannye) {
  const vybor = [];
  for (const vydacha of dannye.vydachi) {
    if (vydacha.chitatel == chitatel.id) vybor.push(vydacha);
  }
  return vybor;
}
// stroka_net_knig: строка «имя: ничего не взял»
function stroka_net_knig(chitatel) {
  return chitatel.imya + ': ничего не взял';
}
// stroka_est_knigi: строка «имя: книги» с пометкой «много»
function stroka_est_knigi(chitatel, nazvaniya) {
  let stroka = chitatel.imya + ': ' + nazvaniya.join(', ');
  if (nazvaniya.length >= POROG_MNOGO) {
    stroka += ' (много)';
  }
  return stroka;
}
// stroka_chitatelya: строка отчёта про одного читателя
function stroka_chitatelya(chitatel, dannye) {
  const nazvaniya = nazvaniya_knig(knigi_chitatelya(chitatel, dannye), dannye.knigi);
  let stroka;
  if (nazvaniya.length === 0) {
    stroka = stroka_net_knig(chitatel);
  } else {
    stroka = stroka_est_knigi(chitatel, nazvaniya);
  }
  return stroka;
}
// otchet: отчёт по читателям, по строке на читателя
function otchet(dannye) {
  const stroki = [];
  for (const chitatel of dannye.chitateli) {
    stroki.push(stroka_chitatelya(chitatel, dannye));
  }
  return stroki;
}
if (typeof module !== 'undefined') module.exports = { otchet };

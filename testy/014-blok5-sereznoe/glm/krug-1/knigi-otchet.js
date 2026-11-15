// порог «много»: при каком числе книг добавлять пометку
var POROG_MNOGO = 2;
// najti_knigu: возвращает книгу по id или null, если не найдена
function najti_knigu(knigi, id) {
  for (var i = 0; i < knigi.length; i++) {
    if (knigi[i].id == id) return knigi[i];
  }
  return null;
}
// vydachi_chitatelya: отбирает выдачи одного читателя по его id
function vydachi_chitatelya(dannye, id_chitatelya) {
  var s = [];
  for (var j = 0; j < dannye.vydachi.length; j++) {
    if (dannye.vydachi[j].chitatel == id_chitatelya) s.push(dannye.vydachi[j]);
  }
  return s;
}
// spisok_knig_chitatelya: собирает и сортирует названия выданных книг читателя
function spisok_knig_chitatelya(dannye, id_chitatelya) {
  var t = [];
  var vydan = vydachi_chitatelya(dannye, id_chitatelya);
  for (var j = 0; j < vydan.length; j++) {
    var kniga = najti_knigu(dannye.knigi, vydan[j].kniga);
    if (kniga !== null) t.push(kniga.nazvanie);
  }
  t.sort();
  return t;
}
// stroka_chitatelya: строит одну строку отчёта для читателя по его списку книг
function stroka_chitatelya(chitatel, spisok) {
  if (spisok.length == 0) return chitatel.imya + ": ничего не взял";
  var s = chitatel.imya + ": " + spisok.join(", ");
  if (spisok.length >= POROG_MNOGO) s += " (много)";
  return s;
}
// otchet: строит отчёт по всем читателям в порядке списка
function otchet(dannye) {
  var r = [];
  for (var i = 0; i < dannye.chitateli.length; i++) {
    var c = dannye.chitateli[i];
    var spisok = spisok_knig_chitatelya(dannye, c.id);
    r.push(stroka_chitatelya(c, spisok));
  }
  return r;
}
if (typeof module !== 'undefined') module.exports = { otchet };

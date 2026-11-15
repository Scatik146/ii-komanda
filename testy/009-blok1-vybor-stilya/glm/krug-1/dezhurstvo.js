// график: данные — кто в какой день дежурит
const GRAFIK = [
  { den: "понедельник", kto: "Тимур" },
  { den: "вторник", kto: "Глеб" },
  { den: "среда", kto: "Вера" }
];

// dezhurnyj: имя дежурного в этот день или пустая строка
function dezhurnyj(den, grafik) {
  const zapis = najtiZapis(den, grafik);
  return imjaDezhurnogo(zapis);
}

// najtiZapis: запись графика для этого дня или null
function najtiZapis(den, grafik) {
  for (let i = 0; i < grafik.length; i++) {
    if (grafik[i].den === den) {
      return grafik[i];
    }
  }
  return null;
}

// imjaDezhurnogo: имя из записи или пустая строка
function imjaDezhurnogo(zapis) {
  if (zapis === null) {
    return "";
  }
  return zapis.kto;
}

if (typeof module !== 'undefined') module.exports = { GRAFIK, dezhurnyj };

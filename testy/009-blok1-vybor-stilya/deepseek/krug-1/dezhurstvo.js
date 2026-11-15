const GRAFIK = [
  { den: 'понедельник', imya: 'Тимур' },
  { den: 'вторник', imya: 'Глеб' },
  { den: 'среда', imya: 'Вера' }
];

// dezhurnyj: возвращает имя дежурного в день или пустую строку
function dezhurnyj(den, grafik) {
  let imya = '';
  for (const zapis of grafik) {
    if (zapis.den !== den) {
      continue;
    }
    imya = zapis.imya;
  }
  return imya;
}

if (typeof module !== 'undefined') module.exports = { GRAFIK, dezhurnyj };
